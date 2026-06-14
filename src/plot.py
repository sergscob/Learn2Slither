import pygame

CELL = 40
BTN_HEIGHT = 50


class GamePlot:
    def __init__(self, size, agent):
        pygame.init()

        self.size = size
        self.agent = agent
        self.width = self.size * CELL
        self.height = self.size * CELL + BTN_HEIGHT

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 28)

        self.paused = False
        # boutons
        self.pause_btn = pygame.Rect(10, self.size * CELL + 5, 120, 40)
        self.save_btn = pygame.Rect(150, self.size * CELL + 5, 120, 40)

    def tick(self, state):

        self.save_requested = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.pause_btn.collidepoint(event.pos):
                    self.paused = not self.paused
                    pygame.Rect(10, self.size * CELL + 5, 120, 40)
                    self.screen.blit(
                        self.font.render("Resume", True, (255, 255, 255)),
                        (self.pause_btn.x + 25, self.pause_btn.y + 10)
                    )
                    pygame.display.flip()

                    while self.paused:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                return True
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if self.pause_btn.collidepoint(event.pos):
                                    self.paused = not self.paused
                        print ("paused")
                        self.clock.tick(130)

                elif self.save_btn.collidepoint(event.pos):
                    self.agent.save_model()

        self.clock.tick(10)

        self.screen.fill((0, 0, 0))

        # pommes
        for a in state.apples:
            color = (0, 255, 0) if a["type"] == "green" else (255, 0, 0)

            pygame.draw.circle(
                self.screen,
                color,
                (a["x"] * CELL + CELL / 2,
                 a["y"] * CELL + CELL / 2),
                CELL / 2
            )

        # snake
        head = True
        for p in state.snake:
            pygame.draw.rect(
                self.screen,
                (0, 0, 250) if head else (0, 0, 150),
                (p["x"] * CELL + 1,
                 p["y"] * CELL + 1,
                 CELL - 2,
                 CELL - 2)
            )
            head = False

        pygame.draw.rect(self.screen, (80, 80, 80), self.pause_btn)
        pygame.draw.rect(self.screen, (80, 80, 80), self.save_btn)

        pause_text = "Resume" if self.paused else "Pause"

        self.screen.blit(
            self.font.render(pause_text, True, (255, 255, 255)),
            (self.pause_btn.x + 25, self.pause_btn.y + 10)
        )

        self.screen.blit(
            self.font.render("Save", True, (255, 255, 255)),
            (self.save_btn.x + 35, self.save_btn.y + 10)
        )

        pygame.display.flip()

        return False

    def end(self):
        pygame.quit()

    def wait_until_close(self):

        text = self.font.render("Training finished", True, (255, 255, 255))
        self.screen.blit(text, (20, 20))
        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.save_btn.collidepoint(event.pos):
                        self.agent.save_model()
            self.clock.tick(30)

        pygame.quit()
