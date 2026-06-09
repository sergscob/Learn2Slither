import random


class MapState:
    def __init__(self, size):
        self.size = size
        self.snake = []
        self.apples = []
        self.initSnake()
        self.initApples()

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
            self.apples.append(self.createApple("green"))

        for i in range(cRed):
            self.apples.append(self.createApple("red"))

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

            if all(0 <= p["x"] < self.size and 0 <= p["y"] < self.size for p in snake):
                self.snake = snake
                self.direction = (dx, dy)
                return

    def changeDirection(self, dx, dy):
            if (dx, dy) == (-self.direction[0], -self.direction[1]):
                return
            self.direction = (dx, dy)

    def move(self):
        dx, dy = self.direction
        head = self.snake[0]

        new_head = {
            "x": head["x"] + dx,
            "y": head["y"] + dy
        }

        # WALL
        if (new_head["x"] < 0 or new_head["x"] >= self.size or new_head["y"] < 0 or new_head["y"] >= self.size):
            return False

        # SELF-COLLISION
        for part in self.snake:
            if part["x"] == new_head["x"] and part["y"] == new_head["y"]:
                return False

        self.snake.insert(0, new_head)

        # APPLE
        eaten = None
        for apple in self.apples:
            if apple["x"] == new_head["x"] and apple["y"] == new_head["y"] :
                if apple["type"] == "green": 
                    eaten = apple
                if apple["type"] == "red": 
                    self.snake.pop()

                self.apples.remove(apple)
                self.apples.append(self.createApple(apple["type"]))
                break

        if eaten is None:
            self.snake.pop()

        if len(self.snake) < 1:
            return False

        return True


