import pygame
from state import MapState

CELL = 40
GRID = 10

pygame.init()
screen = pygame.display.set_mode((GRID * CELL, GRID * CELL))
clock = pygame.time.Clock()

game = MapState(GRID)

running = True
while running:
    clock.tick(1)  # speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.changeDirection(-1, 0)
            if event.key == pygame.K_RIGHT:
                game.changeDirection(1, 0)
            if event.key == pygame.K_UP:
                game.changeDirection(0, -1)
            if event.key == pygame.K_DOWN:
                game.changeDirection(0, 1)

    alive = game.move()
    game.get_state()
    if not alive:
        print("GAME OVER")
        running = False

    screen.fill((0, 0, 0))

    # apples
    for a in game.apples:
        color = (0, 255, 0) if a["type"] == "green" else (255, 0, 0)
        pygame.draw.circle(
            screen,
            color,
            (a["x"] * CELL + CELL/2, a["y"] * CELL + CELL/2),
            CELL/2
        )

    # snake
    head = True
    for p in game.snake:
        pygame.draw.rect(
            screen,
            (0, 0, 250) if head else (0, 0, 150),
            (p["x"] * CELL+1, p["y"] * CELL+1, CELL-2, CELL-2)
        )
        head = False

    pygame.display.flip()

pygame.quit()
