import sys
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
import pygame


class Node:
    def __init__(self, r: int, pos: NDArray[np.float64], color: list[int]):
        self.r = r
        self.color = color
        self.pos = pos

    def mv(self, dpos: NDArray[np.float64]) -> None:
        self.pos += dpos

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, self.pos.astype(np.int64), self.r)


@dataclass
class PygameVars:
    screen: pygame.Surface
    clock: pygame.time.Clock
    FPS: int
    BG_COLOR: tuple[int, int, int]


def setup_pygame_vars(WIDTH: int, HEIGHT: int, FPS: int) -> PygameVars:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rörlig cirkel — mainloop")
    clock = pygame.time.Clock()
    return PygameVars(screen=screen, clock=clock, FPS=FPS, BG_COLOR=(20, 20, 20))


def mainloop(pygame_vars: PygameVars):
    running = True
    n1 = Node(r=30, pos=np.array([400, 300]), color=(200, 120, 70))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame_vars.screen.fill(pygame_vars.BG_COLOR)
        n1.mv(np.array((2, 4)))
        n1.draw(pygame_vars.screen)

        pygame.display.flip()
        pygame_vars.clock.tick(pygame_vars.FPS)
        pygame.display.update()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame_vars = setup_pygame_vars(WIDTH=800, HEIGHT=600, FPS=40)
    mainloop(pygame_vars)
