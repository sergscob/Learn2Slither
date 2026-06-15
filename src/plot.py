import pygame

CELL = 40
BTN_HEIGHT = 50
BTN_COLOR = (80, 80, 80)

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"


def print_snake_vision(state, current_direction_vector):
    danger_f, danger_l, danger_r, apple_f, apple_b, apple_l, apple_r = state

    dir_arrows = {
        (0, -1): "↑",
        (0, 1):  "↓",
        (-1, 0): "←",
        (1, 0):  "→"
    }
    arrow = dir_arrows.get(current_direction_vector, "??")

    print(f"Dir: {arrow} {RED}Danger: forward={danger_f},"
          f" left={danger_l}, right={danger_r}{RESET} "
          f"{GREEN}Apple: forward={apple_f}, back={apple_b}, "
          f" left={apple_l}, right={apple_r}{RESET}")
    print(f"State {state}")


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
        # Кнопки
        self.pause_btn = pygame.Rect(10, self.size * CELL + 5, 120, 40)
        self.save_btn = pygame.Rect(150, self.size * CELL + 5, 120, 40)

    def checkPressButtons(self, env):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.pause_btn.collidepoint(event.pos):
                    self.paused = not self.paused
                    print_snake_vision(env.get_state(), env.direction)

                elif self.save_btn.collidepoint(event.pos):
                    self.agent.save_model()
        return False

    def tick(self, env, state):
        while True:
            if self.checkPressButtons(env):
                return True

            self.screen.fill((0, 0, 0))

            for a in env.apples:
                color = (0, 255, 0) if a["type"] == "green" else (255, 0, 0)
                pygame.draw.circle(
                    self.screen,
                    color,
                    (int(a["x"] * CELL + CELL/2), int(a["y"] * CELL + CELL/2)),
                    int(CELL / 2)
                )

            head = True
            for p in env.snake:
                pygame.draw.rect(
                    self.screen,
                    (0, 0, 250) if head else (0, 0, 150),
                    (p["x"] * CELL + 1, p["y"] * CELL + 1, CELL - 2, CELL - 2)
                )
                head = False

            pygame.draw.rect(self.screen, BTN_COLOR, self.pause_btn)
            pygame.draw.rect(self.screen, BTN_COLOR, self.save_btn)

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

            if self.paused:
                self.clock.tick(30)
            else:
                self.clock.tick(10)
                break

        return False

    def wait_until_close(self, isFinished):
        if isFinished:
            text = self.font.render("Training finished", True, (255, 255, 255))
            self.screen.blit(text, (20, 20))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.save_btn.collidepoint(event.pos):
                        self.agent.save_model()
                    if self.pause_btn.collidepoint(event.pos):
                        self.paused = not self.paused
                        if not isFinished:
                            return False
            self.clock.tick(30)
