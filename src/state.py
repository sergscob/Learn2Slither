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

    def updateApplesCoords(self):
        self.green_coords = {
            (a["x"], a["y"]) for a in self.apples if a["type"] == "green"
        }
        self.red_coords = {
            (a["x"], a["y"]) for a in self.apples if a["type"] == "red"
        }

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
        if any(part["x"] == new_head["x"] and part["y"] == new_head["y"]
               for part in self.snake):
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

        directions = {
            "forward": (dx, dy),
            "left": (dy, -dx),
            "right": (-dy, dx),
            "behind": (-dx, -dy)
        }

        dangers = {"forward": 0, "left": 0, "right": 0, "behind": 0}
        apples_found = {"forward": 0, "left": 0, "right": 0, "behind": 0}

        snake_body = {(part["x"], part["y"]) for part in self.snake}

        # 4 Directions
        for name, (cur_dx, cur_dy) in directions.items():
            x = head_x + cur_dx
            y = head_y + cur_dy
            distance = 1

            while 0 <= x < self.size and 0 <= y < self.size:
                # SELF-Collision or RED APPLE
                if (x, y) in snake_body or (x, y) in self.red_coords:
                    if distance == 1:
                        dangers[name] = 1
                    break  # on ne voit rien apres

                # GREEN APPLE
                if (x, y) in self.green_coords:
                    apples_found[name] = 1  # on voit apres

                x += cur_dx
                y += cur_dy
                distance += 1

            # WALL
            if distance == 1:
                dangers[name] = 1

        state = (
            dangers["forward"],
            dangers["left"],
            dangers["right"],
            apples_found["forward"],
            apples_found["behind"],
            apples_found["left"],
            apples_found["right"]
        )

        return state
