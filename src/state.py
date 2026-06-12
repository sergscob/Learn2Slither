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
        reward = -0.01
        self.steps_without_food += 1
        dx, dy = self.direction
        head = self.snake[0]

        new_head = {
            "x": head["x"] + dx,
            "y": head["y"] + dy
        }

        # WALL
        if (new_head["x"] < 0 or new_head["x"] >= self.size or new_head["y"] < 0 or new_head["y"] >= self.size):
            return self.get_state(), -50, True

        # SELF-COLLISION
        for part in self.snake:
            if part["x"] == new_head["x"] and part["y"] == new_head["y"]:
                return self.get_state(), -50, True

        self.snake.insert(0, new_head)

        # APPLE
        eaten = None
        for apple in self.apples:
            if apple["x"] == new_head["x"] and apple["y"] == new_head["y"] :
                if apple["type"] == "green": 
                    eaten = apple
                    reward += 5
                    self.steps_without_food = 0
                if apple["type"] == "red": 
                    reward -= 5

                self.apples.remove(apple)
                self.apples.append(self.createApple(apple["type"]))
                break

        if eaten is None:
            self.snake.pop()

        if len(self.snake) < 1:
            return self.get_state(), -50, True
        
        if self.steps_without_food > 100:
            return self.get_state(), -50, True        

        return self.get_state(), reward, False


    def normParam(self, distance):
        # return round((self.size - distance) / self.size, 1)
        if distance <= 2: val = 3
        elif distance <= 4: val = 2
        elif distance <= 6: val = 1
        else: val = 0
        return val

    # def get_state(self):
    #     head_x = self.snake[0]["x"]
    #     head_y = self.snake[0]["y"]

    #     directions = {
    #         "UP": (0, -1),
    #         "DOWN": (0, 1),
    #         "LEFT": (-1, 0),
    #         "RIGHT": (1, 0)
    #     }

    #     state = []
        
    #     for dx, dy in directions.values():

    #         wall_dist = 0
    #         body_dist = 0
    #         green_dist = 0
    #         red_dist = 0

    #         distance = 1

    #         x = head_x + dx
    #         y = head_y + dy

    #         while (0 <= x < self.size and 0 <= y < self.size):

    #             if body_dist == 0 and {"x": x, "y": y} in self.snake[1:]:
    #                 body_dist = self.normParam(distance)

    #             if green_dist == 0 and {"x": x, "y": y, "type":"green"} in self.apples:
    #                 green_dist = self.normParam(distance)

    #             if red_dist == 0 and {"x": x, "y": y, "type":"red"} in self.apples:
    #                 red_dist = self.normParam(distance)

    #             x += dx
    #             y += dy
    #             distance += 1

    #         wall_dist = self.normParam(distance)

    #         state.extend([
    #             wall_dist,
    #             body_dist,
    #             green_dist,
    #             red_dist
    #         ])

    #     # direction (one-hot)
    #     # state.extend([
    #     #     1 if self.direction == (0, -1) else 0,
    #     #     1 if self.direction == (0, 1) else 0,
    #     #     1 if self.direction == (-1, 0) else 0,
    #     #     1 if self.direction == (1, 0) else 0
    #     # ])

    #     # print (repr(state))

    #     return tuple(state)

    def get_state(self):

        head_x = self.snake[0]["x"]
        head_y = self.snake[0]["y"]

        directions = [
            (0, -1),  # UP
            (0, 1),   # DOWN
            (-1, 0),  # LEFT
            (1, 0)    # RIGHT
        ]

        state = []

        for dx, dy in directions:

            x = head_x + dx
            y = head_y + dy

            danger = 0
            food = 0

            # смотрим вдоль луча
            while 0 <= x < self.size and 0 <= y < self.size:

                # тело = опасность
                if {"x": x, "y": y} in self.snake[1:]:
                    danger = 1

                # стена = опасность (если сразу или позже)
                # если мы вообще вышли — значит уже опасно
                # (обрабатывается через границу)

                # зелёное яблоко
                if {"x": x, "y": y, "type": "green"} in self.apples:
                    food = 1

                x += dx
                y += dy

            # если следующий шаг сразу в стену → danger
            nx = head_x + dx
            ny = head_y + dy

            if not (0 <= nx < self.size and 0 <= ny < self.size):
                danger = 1

            state.extend([danger, food])

        # текущее направление (важно для избегания разворота)
        state.extend([
            1 if self.direction == (0, -1) else 0,
            1 if self.direction == (0, 1) else 0,
            1 if self.direction == (-1, 0) else 0,
            1 if self.direction == (1, 0) else 0
        ])

        return tuple(state)    