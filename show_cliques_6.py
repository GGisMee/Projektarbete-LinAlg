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
    central_acceleration: int


class Node:
    def __init__(
        self, pos: NDArray[np.float64], R: int = 30, NAME: str|None = None, COLOR: tuple[int, int, int] = (66, 123, 245)
    ):
        self.R = R
        self.COLOR = COLOR
        self.pos = pos

    def mv(self, dpos: NDArray[np.float64]) -> None:
        self.pos += dpos

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.COLOR, self.pos.tolist(), self.R)



class Nodes:
    """A class for operating on all of the nodes"""
    def __init__(self, VERTEX_MATRIX: np.ndarray, SCREEN_SIZE: tuple[int, int],NODE_NAMES: tuple[str,...], CHOSEN_NODES: tuple|None = None):
        """
        Args:
            VERTEX_MATRIX: a matrix of ones and zeros which explains which nodes are connected to which. Shape (n x n)
            CHOSEN_NODES: a vector of the indices of the chosen nodes. If None, include all
        """
        if not CHOSEN_NODES:
            CHOSEN_NODES = tuple(range(VERTEX_MATRIX.shape[0]))  # include all indices of rows in vertex_matrix
        self.nodes = self.generate_nodes(CHOSEN_NODES, SCREEN_SIZE, NODE_NAMES)
        self.VERTEX_MATRIX = VERTEX_MATRIX
        
    @staticmethod
    def generate_nodes(CHOSEN_NODES: tuple, SCREEN_SIZE: tuple[int, int], NODE_NAMES: tuple[str,...]) -> list[Node]:
        '''Simple helper method to generate the a list of type Node for indices in CHOSEN_NODES'''
        x_positions = np.random.randint(low=0,high = SCREEN_SIZE[0], size=len(CHOSEN_NODES))
        y_positions = np.random.randint(low=0,high= SCREEN_SIZE[1], size=len(CHOSEN_NODES))
        nodes = []
        for list_index, node_index in enumerate(CHOSEN_NODES):
            name = NODE_NAMES[node_index]
            x_pos = x_positions[list_index]
            y_pos = y_positions[list_index]
            
            node = Node(pos=np.array(x_pos, y_pos))
            nodes.append(node)
        return nodes

    def mv(self):
        '''Moves all the nodes, by applying forces to keep the connected once close, the disconnected once away and all of them close to center'''
        pass
    def draw(self):
        pass

def setup_pygame_vars(WIDTH: int, HEIGHT: int, FPS: int) -> PygameVars:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rörlig cirkel — mainloop")
    clock = pygame.time.Clock()
    return PygameVars(
        screen=screen,
        clock=clock,
        FPS=FPS,
        BG_COLOR=(20, 20, 20),
        SCREEN_SIZE=(WIDTH, HEIGHT),
    )

def mainloop(
    pygame_vars: PygameVars,
):
    running = True

    VERTEX_MATRIX: np.ndarray = np.array([[0,0,1], [1,0,1], [1,0,0]])
    CHOSEN_VERTICES = (0,1,2)
    NODE_NAMES = ("Sweden", "Bulgaria", "North Korea")
    nodes = Nodes(VERTEX_MATRIX, pygame_vars.SCREEN_SIZE, NODE_NAMES, CHOSEN_VERTICES)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame_vars.screen.fill(pygame_vars.BG_COLOR)
        nodes.mv()
        nodes.draw()
        pygame.display.flip()
        pygame_vars.clock.tick(pygame_vars.FPS)
        pygame.display.update()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    
    pygame_vars = setup_pygame_vars(WIDTH=800, HEIGHT=600, FPS=40)
    mainloop(pygame_vars)