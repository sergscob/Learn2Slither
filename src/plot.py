import pygame

CELL = 40
BTN_HEIGHT = 150
BTN_COLOR = (80, 80, 80)

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"


class GamePlot:
    def __init__(self, size, agent):
        pygame.init()

        self.size = size
        self.agent = agent
        self.width = self.size * CELL
        self.height = self.size * CELL + BTN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 20)
        self.paused = False
        self.pause_btn = pygame.Rect(10, self.size * CELL + 5, 120, 40)
        self.save_btn = pygame.Rect(150, self.size * CELL + 5, 120, 40)

    def checkPressButtons(self, env):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.pause_btn.collidepoint(event.pos):
                    self.paused = not self.paused
                    self.print_snake_vision(env, env.get_state())

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
                    self.screen, color,
                    (int(a["x"] * CELL + CELL/2), int(a["y"] * CELL + CELL/2)),
                    int(CELL / 2)
                )

            # SNAKE
            head = True
            for p in env.snake:
                pygame.draw.rect(
                    self.screen, (0, 0, 250) if head else (0, 0, 150),
                    (p["x"] * CELL + 1, p["y"] * CELL + 1, CELL - 2, CELL - 2))
                head = False

            pygame.draw.rect(self.screen, BTN_COLOR, self.pause_btn)
            pygame.draw.rect(self.screen, BTN_COLOR, self.save_btn)

            pause_text = "Resume" if self.paused else "Pause"

            self.screen.blit(
                self.font.render(pause_text, True, (255, 255, 255)),
                (self.pause_btn.x + 35, self.pause_btn.y + 12)
            )
            self.screen.blit(
                self.font.render("Save", True, (255, 255, 255)),
                (self.save_btn.x + 42, self.save_btn.y + 12)
            )

            self.show_telemetry(env)
            pygame.display.flip()

            if self.paused:
                self.clock.tick(30)
            else:
                self.clock.tick(8)
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

    def get_telemetry(self, env, state):
        (danger_f, danger_l, danger_r, body_far_f, body_far_l, body_far_r,
            apple_f, apple_b, apple_l, apple_r) = state

        dir_names = {
            (0, -1): "UP",
            (0, 1):  "DOWN",
            (-1, 0): "LEFT",
            (1, 0):  "RIGHT"
        }
        arrow = dir_names.get(env.direction, "??")
        stats_text = f"Len: {len(env.snake)} | Steps: {env.steps} | "
        stats_text += f"Avg Len: {env.avg_len:.0f}"
        dir_text = f"Dir: {arrow}"
        vision_1 = f"Danger(F,L,R): {danger_f},{danger_l},{danger_r}"
        vision_1 += f"  BodyFar(F,L,R): {body_far_f},{body_far_l},{body_far_r}"
        vision_2 = f"Apple(F,B,L,R): {apple_f},{apple_b},{apple_l},{apple_r}"
        state_text = f"State list: {list(state)}"

        return (stats_text, dir_text, vision_1, vision_2, state_text)

    def print_snake_vision(self, env, state):
        (stats_text, dir_text, vision_text_1, vision_text_2,
            state_text) = self.get_telemetry(env, state)

        print(f"Paused: \n{stats_text}\n{dir_text}\n"
              f"{RED}{vision_text_1}{RESET}"
              f"\n{GREEN}{vision_text_2}{RESET}\n{state_text}")

    def show_telemetry(self, env):
        (stats_text, dir_text, vision_text_1, vision_text_2,
            state_text) = self.get_telemetry(env, env.get_state())

        panel_y = self.size * CELL + 55
        pygame.draw.rect(self.screen, (0, 0, 0), (0, panel_y, self.width, 55))
        line_spacing = 18

        self.screen.blit(self.font.render(stats_text,
                         True, (255, 215, 0)), (10, panel_y))
        self.screen.blit(self.font.render(dir_text, True,
                         (255, 120, 120)), (10, panel_y + line_spacing))
        self.screen.blit(self.font.render(vision_text_1, True,
                         (255, 120, 120)), (10, panel_y + line_spacing*2))
        self.screen.blit(self.font.render(vision_text_2, True,
                         (120, 255, 120)), (10, panel_y + line_spacing*3))
        self.screen.blit(self.font.render(state_text, True,
                         (160, 160, 160)), (10, panel_y + line_spacing*4))

    def show_final(self, env, episodes, max_len, max_steps):
        panel_y = self.size * CELL + 55
        line_spacing = 18
        pygame.draw.rect(self.screen, (0, 0, 0),
                         (0, panel_y, self.width, self.height - panel_y))

        text = f"Eposodes: {episodes}"
        self.screen.blit(self.font.render(text, True,
                         (0, 255, 255)), (10, panel_y))

        text = f"Avg Len: {env.avg_len:.0f}"
        self.screen.blit(self.font.render(text, True, (0, 255, 255)),
                         (10, panel_y + line_spacing))

        text = f"Max len: {max_len}  |  Max steps: {max_steps}"
        self.screen.blit(self.font.render(text, True, (0, 255, 255)),
                         (10, panel_y + line_spacing*2))
        pygame.display.flip()
