import pygame
from state import MapState

CELL = 40

class GamePlot:
    def __init__(self, size):    
        pygame.init()
        self.size = size
        self.screen = pygame.display.set_mode((self.size * CELL, self.size * CELL))
        self.clock = pygame.time.Clock()


    def tick(self, state): 
   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True    
            
        self.clock.tick(10)  # speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        
        self.screen.fill((0, 0, 0))

        for a in state.apples:
            color = (0, 255, 0) if a["type"] == "green" else (255, 0, 0)
            pygame.draw.circle(
                self.screen,
                color,
                (a["x"] * CELL + CELL/2, a["y"] * CELL + CELL/2),
                CELL/2
            )

        # snake
        head = True
        for p in state.snake:
            pygame.draw.rect(
                self.screen,
                (0, 0, 250) if head else (0, 0, 150),
                (p["x"] * CELL+1, p["y"] * CELL+1, CELL-2, CELL-2)
            )
            head = False

        pygame.display.flip()
        return False

    def end(self):
        pygame.quit()
