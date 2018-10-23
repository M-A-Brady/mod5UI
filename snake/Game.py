import pygame
import random

class SnakeGame:

    # board[x][y][z] means board[front to back][bottom to top][right to left]
    # see https://docs.google.com/document/d/1-LGIlPrV1G8JojxiikUIvX7hAX0S8LZAeEbLJSfVa48
    # for an explanation.
    board = []

    # The score the player has (= #apples eaten)
    score = 0

    # Heading of the snake
    # Convention: x, y or z and then + or - to indicate lower or higher in the index
    heading = "x+"

    # snake body, expressed in coordinates
    # the head is the last index, the tail is the first index
    snake_body = [[0, 0, -1], [0, 0, 0]]

    # apple, expressed in coordinates
    apple = [random.randint(0, 3), random.randint(0, 3), random.randint(0, 3)]

    # game_over keeps track of when the game is over.
    game_over = False

    # [[=========]]
    # [[FUNCTIONS]]
    # [[=========]]

    def __init__(self):
        global board
        board = self.setup_board()

    # initializes the board so all values are False (meaning all LEDs should be off)
    def setup_board(self):
        surfaces = []
        left_offset = 0
        top_offset = 30
        offset = 12
        box_radius = 30

        for _z in range(0, 4):
            top = top_offset
            row_surfaces = []
            for _y in range(0, 4):
                val_surfaces = []
                left = left_offset
                for _x in range(0, 4):
                    #                    PYGAME RECT                                     DRAW AS ACTIVE
                    val_surfaces.append([pygame.Rect(left, top, box_radius, box_radius), False])
                    left += box_radius + offset
                row_surfaces.append(val_surfaces)
                top += box_radius + offset
            surfaces.append(row_surfaces)
            top_offset += 8
            left_offset += 8
        self.board = surfaces

    # clears the board: sets every square as not active.
    def clear_board(self,):
        for plane in self.board:
            for row in plane:
                for val in row:
                    val[1] = False

    # does everything necessary to update the snake.
    def update_snake(self):
        # get indices of last head
        z, y, x = self.snake_body.copy()[len(self.snake_body) - 1]

        # delete tail if apple not found
        if not [z, y, x] == self.apple:
            self.snake_body = self.snake_body[1:]
        else:
            self.score += 1
            self.apple = [random.randint(0, 3), random.randint(0, 3), random.randint(0, 3)]

        # add head
        # snake_body[z][y][x]
        if self.heading == "x+":
            x += 1
        elif self.heading == "x-":
            x -= 1
        elif self.heading == "y+":
            y += 1
        elif self.heading == "y-":
            y -= 1
        elif self.heading == "z+":
            z += 1
        elif self.heading == "z-":
            z -= 1

        if not -1 < x < 4 or not -1 < y < 4 or not -1 < z < 4:
            self.game_over = True

        self.snake_body.append([z, y, x])
        print("body: {0}".format(self.snake_body))
        print("apple: {0} \n".format(self.apple))

    # does everything necessary to correctly update the board.
    def update_board(self):
        self.clear_board()
        self.update_snake()

        # add the snake to the board
        try:
            for segment in self.snake_body:
                z, y, x = 3 - segment[0], 3 - segment[1], 3 - segment[2]
                # z, y, x and 'active' boolean
                self.board[z][y][x][1] = True
        except IndexError:
            self.game_over = True

        # add the apple to the board
        z, y, x = 3 - self.apple[0], 3 - self.apple[1], 3 - self.apple[2]
        self.board[z][y][x][1] = True

    # return the board as an array of the bits to be sent to the FPGA
    # see the protocol for what the representation means
    def get_board_as_sendable(self):
        data = []

        # chunk is 8 bits
        chunk = []
        for z in range(0, 4):
            for y in range(0, 4):
                if len(chunk) >= 8:
                    data.append(chunk)
                    chunk = []
                for x in range(0, 4):
                    chunk.append(self.board[z][y][x][1])
        return data
