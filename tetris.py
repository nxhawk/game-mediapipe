import random
import sys
import pygame

pygame.init()
score_font = pygame.font.SysFont("comicsansms", 25)
WIDTH_SQUARE = 10
HEIGHT_SQUARE = 20
FPS = 200
RED = (155, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WIDTH_SCREEN = 800
HEIGHT_SCREEN = 700
BLOCK_SIZE = 30
TIMEWAIT = 500
clock = pygame.time.Clock()
X_STAR = (WIDTH_SCREEN - WIDTH_SQUARE*BLOCK_SIZE)//2
Y_STAR = (HEIGHT_SCREEN - HEIGHT_SQUARE*BLOCK_SIZE)//2
screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption("TETRIS")
#
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255,
                                                          255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128), (0, 0, 0)]

addOP = pygame.USEREVENT
pygame.time.set_timer(addOP, TIMEWAIT)
# []


def drawScreen():
    global table
    for i in range(HEIGHT_SQUARE):
        for j in range(WIDTH_SQUARE):
            if table[i][j] != 7:
                pygame.draw.rect(screen, shape_colors[table[i][j]], [
                                 X_STAR+j*BLOCK_SIZE, Y_STAR+i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])
            pygame.draw.rect(screen, WHITE, [
                             X_STAR+j*BLOCK_SIZE, Y_STAR+i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE], 1)
    pygame.draw.rect(screen, RED, [
                     X_STAR, Y_STAR, BLOCK_SIZE*WIDTH_SQUARE, HEIGHT_SQUARE*BLOCK_SIZE], 4)


def drawBlock(x, y, current, k):
    for i in range(5):
        for j in range(5):
            if current[k][i][j] == '0' and y >= Y_STAR-BLOCK_SIZE:
                pygame.draw.rect(screen, shape_colors[shapes.index(current)], [
                                 x+i*BLOCK_SIZE, y+j*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE])


def constTable(table):
    new_table = []
    for i in range(HEIGHT_SQUARE + 1):
        new_table.append([7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7])
    return new_table


table = []
table = constTable(table)


def check_table(x, y, current, k):
    global table
    for i in range(5):
        for j in range(5):
            if current[k][i][j] == '0':
                if table[j+y+1][x+i] != 7 or y + 1 + j >= 20:

                    for u in range(5):
                        for v in range(5):
                            if current[k][u][v] == '0':
                                table[y+v][x+u] = shapes.index(current)
                    return True
    return False


def check_left(x, y, current, k):
    global table
    for i in range(5):
        for j in range(5):
            if current[k][i][j] == '0':
                if table[j+y][x+i-1] != 7 or x+i-1 < 0:
                    return False
    return True


def check_left_next(x, y, current, k):
    global table
    for i in range(5):
        for j in range(5):
            if current[k][i][j] == '0':
                if table[j+y][x+i] != 7 or x+i < 0:
                    return False
    return True


def check_right_next(x, y, current, k):
    global table
    for i in range(5):
        for j in range(5):
            if current[k][i][j] == '0':
                if table[j+y][x+i] != 7 or x+i > 9:
                    return False
    return True


def check_right(x, y, current, k):
    global table
    for i in range(5):
        for j in range(5):
            if current[k][i][j] == '0':
                if table[j+y][x+i+1] != 7 or x+i+1 > 9:
                    return False
    return True


def checkScore():
    global table
    for i in range(HEIGHT_SQUARE):
        kout = 0
        for j in range(WIDTH_SQUARE):
            if table[i][j] != 7:
                kout += 1
        if kout == WIDTH_SQUARE:
            global score
            score += 10
            for u in range(i, -1, -1):
                for j in range(WIDTH_SQUARE):
                    table[u][j] = table[u-1][j]


def check_over():
    global table
    for i in range(WIDTH_SQUARE):
        if table[1][i] != 7:
            return False
    return True


def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, WHITE)
    screen.blit(value, [WIDTH_SCREEN/6 - 100, HEIGHT_SCREEN//4])


next_ok = False
current = random.choice(shapes)
next_current = random.choice(shapes)
x = X_STAR
y = Y_STAR
k = 0
xx = 0
yy = 0
score = 0

game_play = True
while game_play:
    screen.fill(BLACK)
    if check_table(xx, yy, current, k):
        x = X_STAR
        y = Y_STAR
        k = 0
        xx = 0
        yy = 0
        current = next_current
        next_current = random.choice(shapes)
    Your_score(score)
    drawBlock(x, y, current, k)
    drawScreen()
    checkScore()

    game_play = check_over()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and check_left(xx, yy, current, k):
                x -= BLOCK_SIZE
                xx -= 1
                screen.fill(BLACK)
                Your_score(score)
                drawBlock(x, y, current, k)
                drawScreen()
            elif event.key == pygame.K_RIGHT and check_right(xx, yy, current, k):
                x += BLOCK_SIZE
                xx += 1
                screen.fill(BLACK)
                Your_score(score)
                drawBlock(x, y, current, k)
                drawScreen()
            elif event.key == pygame.K_DOWN:
                y += BLOCK_SIZE
                yy += 1
            elif event.key == pygame.K_UP and check_left_next(xx, yy, current, (k+1) % (len(current))) and check_right_next(xx, yy, current, (k+1) % (len(current))):
                k = (k+1) % (len(current))

        if event.type == addOP:
            y += BLOCK_SIZE
            yy += 1
    pygame.display.update()
    clock.tick(FPS)
