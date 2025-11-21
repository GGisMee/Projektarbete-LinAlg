import sys
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
import pygame

@dataclass
class PygameVars:
    """A dataclass for storing pygame info"""
    screen: pygame.Surface
    clock: pygame.time.Clock
    FPS: int
    BG_COLOR: tuple[int, int, int]
    SCREEN_SIZE: tuple[int, int]

@dataclass
class MvVars:
    central_multiplier: np.float32
    node_distance: int
    node_multiplier: np.float32

@dataclass
class NodeVars:
    radius: int
    node_color: tuple[int,int,int]
    line_width:int
    arrow_color: tuple[int,int,int]


class Node:
    def __init__(
        self, pos: NDArray[np.float32], R: int = 12, NAME: str|None = None, COLOR: tuple[int, int, int] = (66, 123, 245), ARROW_COLOR: tuple[int,int,int] = (200,200,200)
    ):
        self.R = R
        self.COLOR = COLOR
        self.pos = pos
        self.NAME =NAME
        self.ARROW_COLOR = ARROW_COLOR

    def mv(self, dpos: NDArray[np.float32]) -> None:
        self.pos += dpos

    def draw_node(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.COLOR, self.pos.tolist(), self.R)
    
    def draw_arrow_head(self, node_edge_pos: np.ndarray, reangle_vector: np.ndarray):
        rx, ry = reangle_vector


        transform_vec = np.array([[rx, -ry], [ry, rx]])
        arrow_head_mat = np.array(((node_vars.line_width*4, -node_vars.line_width*2), (node_vars.line_width*4,node_vars.line_width*2)))
        arrow_head_mat = (transform_vec @ arrow_head_mat.T).T # Having to since the operations are done rowwise instead of columnwise...
        pygame.draw.polygon(pygame_vars.screen, color=self.ARROW_COLOR, points=(node_edge_pos.tolist(), (node_edge_pos+arrow_head_mat[0]).tolist(), (node_edge_pos+arrow_head_mat[1]).tolist()))

    def draw_arrow(self, screen: pygame.Surface, vectors_to_connected_nodes: np.ndarray, normalized_vectors_to_connected_nodes: np.ndarray) -> None:
        for i, vec in enumerate(vectors_to_connected_nodes):
            norm_vec = normalized_vectors_to_connected_nodes[i]
            node_edge_pos = self.pos+norm_vec*self.R
            other_node_edge_pos = vec+self.pos-norm_vec*self.R
            pygame.draw.line(screen, color=self.ARROW_COLOR, start_pos=node_edge_pos.tolist(), end_pos=other_node_edge_pos.tolist())
            self.draw_arrow_head(node_edge_pos, norm_vec)

class Nodes:
    """A class for operating on all of the nodes"""
    def __init__(self, mv_vars: MvVars,node_vars:NodeVars, CENTRUM_POINT:np.ndarray, VERTEX_MATRIX: np.ndarray, SCREEN_SIZE: tuple[int, int],NODE_NAMES: tuple[str,...], CHOSEN_NODES: tuple|None = None):
        """
        Args:
            VERTEX_MATRIX: a matrix of ones and zeros which explains which nodes are connected to which. Shape (n x n)
            CHOSEN_NODES: a vector of the indices of the chosen nodes. If None, include all
        """
        if not CHOSEN_NODES:
            CHOSEN_NODES = tuple(range(VERTEX_MATRIX.shape[0]))  # include all indices of rows in vertex_matrix
        self.nodes = self.generate_nodes(CHOSEN_NODES, SCREEN_SIZE, NODE_NAMES, node_vars)
        self.VERTEX_MATRIX = VERTEX_MATRIX
        self.mv_vars = mv_vars
        self.CENTRUM_PONT = CENTRUM_POINT
        self.positions: np.ndarray = np.array([])

    @staticmethod
    def generate_nodes(CHOSEN_NODES: tuple, SCREEN_SIZE: tuple[int, int], NODE_NAMES: tuple[str,...], node_vars:NodeVars) -> list[Node]:
        '''Simple helper method to generate the a list of type Node for indices in CHOSEN_NODES'''
        x_positions = np.random.randint(low=0,high = SCREEN_SIZE[0], size=len(CHOSEN_NODES)).astype(np.float32)
        y_positions = np.random.randint(low=0,high= SCREEN_SIZE[1], size=len(CHOSEN_NODES)).astype(np.float32)
        nodes = []
        for list_index, node_index in enumerate(CHOSEN_NODES):
            name = NODE_NAMES[node_index]
            x_pos = x_positions[list_index]
            y_pos = y_positions[list_index]
            
            node = Node(pos=np.array([x_pos, y_pos]), NAME=name, R=node_vars.radius, COLOR=node_vars.node_color, ARROW_COLOR= node_vars.arrow_color)
            nodes.append(node)
        return nodes

    def mv_distance(self, multiplier:np.float32, distances:np.ndarray) -> np.ndarray:
        ds = multiplier*(distances-self.mv_vars.node_distance)
        return ds

    @staticmethod
    def calculate_movement_vec(vectors: np.ndarray, multiplier:np.float32, prefered_distance: np.float32 | float) -> tuple[np.ndarray, np.ndarray]:
        '''Given some vectors in different directions, calculate '''
        length_of_vectors = np.linalg.norm(vectors, axis=-1)
        normalized_vectors = vectors / length_of_vectors[:, np.newaxis]
        distances = multiplier * (length_of_vectors - prefered_distance)
        vectorized_distances = distances* normalized_vectors
        return np.sum(vectorized_distances, axis=0), normalized_vectors
         
    def get_output_movement_vector(self, node:Node, vectors_to_connected_nodes:np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        '''Creates the different vectors and adds them together to get a finalized movement vector for the node'''
        centrum_vec = self.CENTRUM_PONT-node.pos
        vec_to_center, _ = self.calculate_movement_vec(centrum_vec[None, ...], self.mv_vars.central_multiplier, prefered_distance=0)
        summed_vec_to_connected_nodes, normalized_vecs_to_connected_nodes = self.calculate_movement_vec(vectors_to_connected_nodes, self.mv_vars.node_multiplier, prefered_distance=self.mv_vars.node_distance)
        return vec_to_center+summed_vec_to_connected_nodes, normalized_vecs_to_connected_nodes

    def mv_and_draw(self, screen: pygame.Surface):
        '''A function which iterates through the nodes. 
        Doing so it draws the nodes arrow lines between the nodes and the arrow heads
        And after that it applies the forces to keep the connected once close, the disconnected once away and all of them close to center
        '''
        self.positions = np.array([node.pos for node in self.nodes])
        for i, node in enumerate(self.nodes):
            # Get all the vectors to the connected_nodes
            connected_to = self.VERTEX_MATRIX[i]
            vectors_to_connected_nodes = (self.positions-node.pos)[np.where(connected_to)]

            movement_vector, normalized_vecs_to_connected_nodes = self.get_output_movement_vector(node, vectors_to_connected_nodes)
            node.draw_arrow(screen, vectors_to_connected_nodes, normalized_vecs_to_connected_nodes)
            node.draw_node(screen)
            node.mv(movement_vector)
            
def setup_pygame_vars(WIDTH: int, HEIGHT: int, FPS: int) -> PygameVars:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Nodvisning")
    clock = pygame.time.Clock()
    return PygameVars(
        screen=screen,
        clock=clock,
        FPS=FPS,
        BG_COLOR=(35, 35, 35),
        SCREEN_SIZE=(WIDTH, HEIGHT),
    )

def setup_movement_vars(FPS: int) -> MvVars:
    central_multiplier = np.float32(0.1/FPS) # 3 pixels per second
    node_distance = 60 # pixels
    node_multiplier = np.float32(0.2/FPS) # 5 pixels per second

    mv_vars = MvVars(central_multiplier=central_multiplier, node_distance=node_distance, node_multiplier=node_multiplier)
    return mv_vars



def mainloop(
    pygame_vars: PygameVars,
    mv_vars: MvVars,
    node_vars: NodeVars
):
    running = True

    VERTEX_MATRIX: np.ndarray = np.array([[0,1,1], [1,0,1], [1,1,0]])
    CHOSEN_VERTICES = (0,1,2)
    NODE_NAMES = ("Sweden", "Bulgaria", "North Korea")
    CENTRUM_POINT = np.array([pygame_vars.SCREEN_SIZE[0]/2, pygame_vars.SCREEN_SIZE[1]/2])
    nodes = Nodes(mv_vars,node_vars, CENTRUM_POINT, VERTEX_MATRIX, pygame_vars.SCREEN_SIZE, NODE_NAMES, CHOSEN_VERTICES)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame_vars.screen.fill(pygame_vars.BG_COLOR)
        nodes.mv_and_draw(pygame_vars.screen)


        
        pygame.display.flip()

        pygame_vars.clock.tick(pygame_vars.FPS)
        pygame.display.update()
        pass
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame_vars = setup_pygame_vars(WIDTH=800, HEIGHT=600, FPS=40)
    mv_vars = setup_movement_vars(pygame_vars.FPS)
    node_vars = NodeVars(12,(66, 123, 245), 2, (150,150,150))
    mainloop(pygame_vars, mv_vars,node_vars)