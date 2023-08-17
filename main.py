import pygame as pg
from random import choice
pg.init()
pg.font.init()

WIDTH = HEIGHT = 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pg.font.SysFont("Consolas", WIDTH // 6)
small_font = pg.font.SysFont("Consolas", WIDTH // 12)

class Block:
    def __init__(self, number):
        self.number = number
        self.width = WIDTH // 3
        self.x = 0
        self.y = 0
        self.txt = font.render(f"{self.number}", 1, BLACK)
        self.txt_width = self.txt.get_width()
        self.txt_height = self.txt.get_height()

    def __repr__(self):
        return str(self.number)

    def draw(self, win):
        self.txt = font.render(f"{self.number}", 1, BLACK)
        x = self.x + self.width // 2 - self.txt_width // 2
        y = self.y + self.width // 2 - self.txt_height // 2
        pg.draw.rect(win, BLACK, (self.x, self.y, self.width, self.width), 1)
        win.blit(self.txt, (x, y))

    def is_mouse_in(self, mouse_x, mouse_y):
        return self.x < mouse_x < self.x + self.width and \
                self.y < mouse_y < self.y + self.width  
            
    def move(self, mouse_x, mouse_y, event, board):
        global moves
        row = None
        column = None
        for i in range(len(board)):
            for j in range(len(board[0])):
                if self.number == board[i][j].number:
                    row = i
                    column = j


        if self.is_mouse_in(mouse_x, mouse_y) and event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            #print(row, column)
            if row > 0 and board[row - 1][column].number == 9:
                board[row][column].number, board[row - 1][column].number = board[row - 1][column].number, board[row][column].number
                moves += 1
                
            elif row < len(board) - 1 and board[row + 1][column].number == 9:
                board[row][column].number, board[row + 1][column].number = board[row + 1][column].number, board[row][column].number
                moves += 1

            elif column > 0 and board[row][column - 1].number == 9:
                board[row][column].number, board[row][column - 1].number = board[row][column - 1].number, board[row][column].number
                moves += 1
                
            elif column < len(board) - 1 and board[row][column + 1].number == 9:
                board[row][column].number, board[row][column + 1].number = board[row][column + 1].number, board[row][column].number
                moves += 1


window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Puzzle")

board = []

def init_board():
    global board
    possible_values = [
        [4, 8, 6, 2, 7, 3, 1, 5, 9],
        [1, 8, 6, 7, 4, 5, 2, 3, 9],
        [6, 7, 2, 3, 8, 5, 4, 1, 9],
        [3, 7, 6, 2, 8, 4, 1, 5, 9],
        [4, 6, 1, 8, 7, 5, 2, 3, 9]
    ]
    values = choice(possible_values)

    board = [
    [Block(values[0]), Block(values[1]), Block(values[2])],
    [Block(values[3]), Block(values[4]), Block(values[5])],
    [Block(values[6]), Block(values[7]), Block(values[8])]
    ]

    for i in range(len(board)):
        for i in range(len(board)):
            for j in range(len(board[0])):
                board[i][j].x = j * board[i][j].width
                board[i][j].y = i * board[i][j].width


def change_board(board, x, y, press):
    global gameWon
    if not gameWon:
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j].number != 9:
                    board[i][j].move(x, y, press, board)


def draw_board(win):
    global gameWon
    if not gameWon:
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j].number != 9:
                    board[i][j].draw(win)


def finish(window):
    global gameWon, board, seconds, moves
    if gameWon:
        for i in range(len(board)):
            for j in range(len(board[0])):
                board[i][j].draw(window)
        pg.display.update()
        pg.time.wait(1000)

        msg = small_font.render(f"Seconds: {int(seconds)}",True, BLACK)
        msg2 = small_font.render(f"Moves: {moves}", True, BLACK)
        window.fill(WHITE)
        window.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2))
        window.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2 + msg.get_height() // 2))
        pg.display.update()
        pg.time.wait(2500)

        init_board()
        gameWon = False
        seconds = 0
        moves = 0

def is_win(board):
    board_list = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            board_list.append(board[i][j].number)
    return board_list == [x for x in range(1, 10)]

def main(win):
    win.fill(WHITE)
    draw_board(win)
    pg.display.update()

init_board()
gameWon = False
run = True
clock = pg.time.Clock()
FPS = 60
seconds = 0
moves = 0
while run:
    clock.tick(FPS)
    mouse_pos = pg.mouse.get_pos()
    mouse_pressed = pg.mouse.get_pressed(num_buttons = 3)
    

    main(window)
    gameWon = is_win(board)

    finish(window)
    if not gameWon:
        seconds += 1 / FPS

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        
        change_board(board, mouse_pos[0], mouse_pos[1], event)

pg.quit()