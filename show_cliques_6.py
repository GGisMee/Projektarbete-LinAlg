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



class Node:
    def __init__(
        self, pos: NDArray[np.float32], R: int = 8, NAME: str|None = None, COLOR: tuple[int, int, int] = (66, 123, 245)
    ):
        self.R = R
        self.COLOR = COLOR
        self.pos = pos

    def mv(self, dpos: NDArray[np.float32]) -> None:
        self.pos += dpos

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.COLOR, self.pos.tolist(), self.R)
    
    def draw_arrow(self, screen: pygame.Surface, end_pos: np.ndarray) -> None:
        pygame.draw.line(screen, color= (200,200,200), start_pos=self.pos.tolist(), end_pos=end_pos.tolist())


class Nodes:
    """A class for operating on all of the nodes"""
    def __init__(self, mv_vars: MvVars, CENTRUM_POINT:np.ndarray, VERTEX_MATRIX: np.ndarray, SCREEN_SIZE: tuple[int, int],NODE_NAMES: tuple[str,...], CHOSEN_NODES: tuple|None = None):
        """
        Args:
            VERTEX_MATRIX: a matrix of ones and zeros which explains which nodes are connected to which. Shape (n x n)
            CHOSEN_NODES: a vector of the indices of the chosen nodes. If None, include all
        """
        if not CHOSEN_NODES:
            CHOSEN_NODES = tuple(range(VERTEX_MATRIX.shape[0]))  # include all indices of rows in vertex_matrix
        self.nodes = self.generate_nodes(CHOSEN_NODES, SCREEN_SIZE, NODE_NAMES)
        self.VERTEX_MATRIX = VERTEX_MATRIX
        self.mv_vars = mv_vars
        self.CENTRUM_PONT = CENTRUM_POINT
        self.positions: np.ndarray = np.array([])

    @staticmethod
    def generate_nodes(CHOSEN_NODES: tuple, SCREEN_SIZE: tuple[int, int], NODE_NAMES: tuple[str,...]) -> list[Node]:
        '''Simple helper method to generate the a list of type Node for indices in CHOSEN_NODES'''
        x_positions = np.random.randint(low=0,high = SCREEN_SIZE[0], size=len(CHOSEN_NODES)).astype(np.float32)
        y_positions = np.random.randint(low=0,high= SCREEN_SIZE[1], size=len(CHOSEN_NODES)).astype(np.float32)
        nodes = []
        for list_index, node_index in enumerate(CHOSEN_NODES):
            name = NODE_NAMES[node_index]
            x_pos = x_positions[list_index]
            y_pos = y_positions[list_index]
            
            node = Node(pos=np.array([x_pos, y_pos]), NAME=name)
            nodes.append(node)
        return nodes

    def mv_distance(self, multiplier:np.float32, distances:np.ndarray) -> np.ndarray:
        ds = multiplier*(distances-self.mv_vars.node_distance)
        return ds

    @staticmethod
    def calculate_movement_vec(vectors: np.ndarray, multiplier:np.float32, prefered_distance: np.float32 | float) -> np.ndarray:
        '''Given some vectors in different directions, calculate '''
        length_of_vectors = np.linalg.norm(vectors, axis=-1)
        normalized_vectors = vectors / length_of_vectors[:, np.newaxis]
        distances = multiplier* ( length_of_vectors - prefered_distance)
        vectorized_distances = distances* normalized_vectors
        return np.sum(vectorized_distances, axis=0)
         

    def mv(self):
        '''Moves all the nodes, by applying forces to keep the connected once close, the disconnected once away and all of them close to center'''
        self.positions = np.array([node.pos for node in self.nodes])
        for i, node in enumerate(self.nodes):

            # Force to center
            centrum_vec = self.CENTRUM_PONT-node.pos
            movement_centrum = self.calculate_movement_vec(centrum_vec[None, ...], self.mv_vars.central_multiplier, prefered_distance=0)

            # Forces between nodes
            connected_to = self.VERTEX_MATRIX[i]
            vec_to_connected_nodes = (self.positions-node.pos)[np.where(connected_to)]
            movement_to_nodes = self.calculate_movement_vec(vec_to_connected_nodes, self.mv_vars.node_multiplier, prefered_distance=self.mv_vars.node_distance)

            node.mv(movement_to_nodes+movement_centrum)

    def _draw_arrows(self, node: Node, i:int):
        connected_to = self.VERTEX_MATRIX[i]
        vec_to_connected_nodes = (self.positions-node.pos)[np.where(connected_to)]
        #* add a static method to 1. get vec_to_connected_nodes and connected to matrix.
        #* a static method to get length of vec and normalized vecs outside of calculate movement vec, maybe put this in another empty class?

    def draw(self, screen: pygame.Surface):
        '''Draws the nodes, the arrow lines and the arrow heads.'''
        for i, node in enumerate(self.nodes):
            node.draw(screen)
            self._draw_arrows(node, i) 

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
    central_multiplier = np.float32(0.5/FPS) # 3 pixels per second
    node_distance = 40 # pixels
    node_multiplier = np.float32(1/FPS) # 5 pixels per second

    mv_vars = MvVars(central_multiplier=central_multiplier, node_distance=node_distance, node_multiplier=node_multiplier)
    return mv_vars



def mainloop(
    pygame_vars: PygameVars,
    mv_vars: MvVars
):
    running = True

    VERTEX_MATRIX: np.ndarray = np.array([[0,1,1], [1,0,1], [1,1,0]])
    CHOSEN_VERTICES = (0,1,2)
    NODE_NAMES = ("Sweden", "Bulgaria", "North Korea")
    CENTRUM_POINT = np.array([pygame_vars.SCREEN_SIZE[0]/2, pygame_vars.SCREEN_SIZE[1]/2])
    nodes = Nodes(mv_vars, CENTRUM_POINT, VERTEX_MATRIX, pygame_vars.SCREEN_SIZE, NODE_NAMES, CHOSEN_VERTICES)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame_vars.screen.fill(pygame_vars.BG_COLOR)
        nodes.mv()
        nodes.draw(pygame_vars.screen)
        pygame.display.flip()
        pygame_vars.clock.tick(pygame_vars.FPS)
        pygame.display.update()
        pass
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame_vars = setup_pygame_vars(WIDTH=800, HEIGHT=600, FPS=40)
    mv_vars = setup_movement_vars(pygame_vars.FPS)
    mainloop(pygame_vars, mv_vars)