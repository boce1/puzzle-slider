import pygame as pg
from random import shuffle
pg.init()
pg.font.init()

WIDTH = HEIGHT = 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pg.font.SysFont("Consolas", WIDTH // 6)

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
                #board[row - 1][column].number = self.number
                #print(board)
                
            elif row < len(board) - 1 and board[row + 1][column].number == 9:
                board[row][column].number, board[row + 1][column].number = board[row + 1][column].number, board[row][column].number
                #board[row - 1][column].number = self.number
                #print(board)

            elif column > 0 and board[row][column - 1].number == 9:
                board[row][column].number, board[row][column - 1].number = board[row][column - 1].number, board[row][column].number
                #board[row - 1][column].number = self.number
                #print(board)
                
            elif column < len(board) - 1 and board[row][column + 1].number == 9:
                board[row][column].number, board[row][column + 1].number = board[row][column + 1].number, board[row][column].number
                #board[row - 1][column].number = self.number
                #print(board)


window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Puzzle")

board = []

def init_board():
    global board
    values = [x for x in range(1, 10)]
    shuffle(values)

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
        
        #init_board()

def finish(window):
    global gameWon, board
    if gameWon:
        print("pusi kurac")
        for i in range(len(board)):
            for j in range(len(board[0])):
                board[i][j].draw(window)
        pg.display.update()
        pg.time.wait(1000)
        init_board()
        gameWon = False

def is_win(board):
    board_list = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            board_list.append(board[i][j].number)
    #print(board_list)
    return board_list == [x for x in range(1, 10)]

def main(win):
    win.fill(WHITE)
    draw_board(win)
    pg.display.update()

init_board()
gameWon = False
run = True
while run:
    mouse_pos = pg.mouse.get_pos()
    mouse_pressed = pg.mouse.get_pressed(num_buttons = 3)
    #print(mouse_pressed)
    main(window)
    gameWon = is_win(board)

    finish(window)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        
        change_board(board, mouse_pos[0], mouse_pos[1], event)

pg.quit()