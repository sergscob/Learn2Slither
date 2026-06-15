import random

class MapState:
    def __init__(self, size):
        self.size = size
        self.reset()

    def reset(self):
        self.snake = []
        self.apples = []
        self.initSnake()
        self.initApples()
        self.steps_without_food = 0
        return self.get_state()

    def createApple(self, appleType):
        occupied = set()
        for item in self.snake:
            occupied.add((item["x"], item["y"]))
        for item in self.apples:
            occupied.add((item["x"], item["y"]))

        free_cells = [
            (x, y)
            for x in range(self.size)
            for y in range(self.size)
            if (x, y) not in occupied
        ]

        if not free_cells:
            return None

        x, y = random.choice(free_cells)

        return {
            "x": x,
            "y": y,
            "type": appleType,
        }

    def initApples(self, cGreen=2, cRed=1):
        for i in range(cGreen):
            apple = self.createApple("green")
            if apple is not None:
                self.apples.append(apple)

        for i in range(cRed):
            apple = self.createApple("red")
            if apple is not None:
                self.apples.append(apple)
        self.updateApplesCoords()

    def updateApplesCoords(self) :
        self.green_coords = {(a["x"], a["y"]) for a in self.apples if a["type"] == "green"}
        self.red_coords = {(a["x"], a["y"]) for a in self.apples if a["type"] == "red"}


    def initSnake(self, startLen=3):
        while True:
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

            head_x = random.randint(startLen, self.size - startLen - 1)
            head_y = random.randint(startLen, self.size - startLen - 1)
            snake = []

            for i in range(startLen):
                x = head_x - dx * i
                y = head_y - dy * i
                snake.append({"x": x, "y": y})

            if all(0 <= p["x"] < self.size
                   and 0 <= p["y"] < self.size for p in snake):
                self.snake = snake
                self.direction = (dx, dy)
                return

    def changeDirection(self, dx, dy):
        if (dx, dy) == (-self.direction[0], -self.direction[1]):
            return
        self.direction = (dx, dy)

    def move(self):
        reward = -0.1 
        self.steps_without_food += 1
        dx, dy = self.direction
        head = self.snake[0]

        new_head = {
            "x": head["x"] + dx,
            "y": head["y"] + dy
        }

        if self.steps_without_food > 200:
            return self.get_state(), -50, True

        # WALLS
        if (new_head["x"] < 0 or new_head["x"] >= self.size
                or new_head["y"] < 0 or new_head["y"] >= self.size):
            return self.get_state(), -50, True

        # SELF-EAT
        if any(part["x"] == new_head["x"] and part["y"] == new_head["y"] for part in self.snake):
            return self.get_state(), -50, True

        # ok, go
        self.snake.insert(0, new_head)

        eaten = None
        for apple in self.apples:
            if apple["x"] == new_head["x"] and apple["y"] == new_head["y"]:
                if apple["type"] == "green":
                    eaten = apple
                    reward += 10.0  
                    self.steps_without_food = 0
                elif apple["type"] == "red":
                    reward -= 10.0  

                self.apples.remove(apple)
                new_apple = self.createApple(apple["type"])
                if new_apple is not None:
                    self.apples.append(new_apple)
                    self.updateApplesCoords()
                break

        if eaten is None:
            self.snake.pop()

        if len(self.snake) < 1:
            return self.get_state(), -50, True
        return self.get_state(), reward, False


    def get_state(self):
        head = self.snake[0]
        head_x = head["x"]
        head_y = head["y"]
        dx, dy = self.direction
        
        dir_forward = (dx, dy)
        dir_left = (dy, -dx)
        dir_right = (-dy, dx)
        dir_behind = (-dx, -dy)

        directions = {
            "forward": dir_forward,
            "left": dir_left,
            "right": dir_right,
            "behind": dir_behind
        }

        apple_forward = 0
        apple_left = 0
        apple_right = 0
        apple_behind = 0
        danger_forward = 0
        danger_left = 0
        danger_right = 0

        # 4 directions
        for name, (cur_dx, cur_dy) in directions.items():
            x = head_x + cur_dx
            y = head_y + cur_dy
            distance = 1

            while 0 <= x < self.size and 0 <= y < self.size:
                # BODY
                if any(part["x"] == x and part["y"] == y for part in self.snake):
                    if distance == 1 and name != "behind":
                        if name == "forward": danger_forward = 1
                        if name == "left": danger_left = 1
                        if name == "right": danger_right = 1
                    break

                # RED APPLE
                if (x, y) in self.red_coords:
                    if distance == 1 and name != "behind":
                        if name == "forward": danger_forward = 1
                        if name == "left": danger_left = 1
                        if name == "right": danger_right = 1
                    break  # RED APPLE blocks vision

                # В) ЗЕЛЕНОЕ ЯБЛОКО
                if (x, y) in self.green_coords:
                    if name == "forward": apple_forward = 1
                    if name == "left": apple_left = 1
                    if name == "right": apple_right = 1
                    if name == "behind": apple_behind = 1
                    # RED APPLE doesn't blocks vision

                x += cur_dx
                y += cur_dy
                distance += 1

            # Если вышли за карту — это стена в конце луча
            if distance == 1:
                if name == "forward": danger_forward = 1
                if name == "left": danger_left = 1
                if name == "right": danger_right = 1

        state = (
            danger_forward,
            danger_left,
            danger_right,
            apple_forward,
            apple_behind,
            apple_left,
            apple_right
        )

        return state