import pygame
import sys
import random

width = 1000
height = 1000
rows = 25


class SnakeNodes():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x = x
        self.y = y


class Snake():
    def __init__(self):
        self.x_pos = rows // 2
        self.y_pos = rows // 2
        self.x_dir = 1
        self.y_dir = 0
        self.dir_changed = False
        self.is_alive = True
        self.nodes = []

    def move(self):
        for i in range(len(self.nodes) - 1, - 1, - 1):
            if i == 0:
                self.nodes[i].move(self.x_pos, self.y_pos)
            else:
                self.nodes[i].move(self.nodes[i - 1].x, self.nodes[i - 1].y)
        self.x_pos += self.x_dir
        self.y_pos += self.y_dir
        self.dir_changed = False

    def set_dir(self, x, y):
        if (abs(self.x_dir) + abs(x) == 2 or
            abs(self.y_dir) + abs(y) == 2 or
                self.dir_changed == True):
            return
        self.x_dir = x
        self.y_dir = y
        self.dir_changed = True

    def check_is_alive(self):
        if (self.x_pos + self.x_dir < 0 or
            self.x_pos + self.x_dir >= rows or
            self.y_pos + self.y_dir < 0 or
                self.y_pos + self.y_dir >= rows):
            self.is_alive = False
        elif len(self.nodes) > 0:
            for node in self.nodes:
                if node.x == self.x_pos and node.y == self.y_pos:
                    self.is_alive = False

    def grow(self):
        nodes_len = len(self.nodes) - 1
        if nodes_len != -1:
            self.nodes.append(SnakeNodes(
                self.nodes[nodes_len].x, self.nodes[nodes_len].y))
        else:
            self.nodes.append(SnakeNodes(self.x_pos, self.y_pos))


class Apple():
    def __init__(self):
        self.x = -1
        self.y = -1
        self.spawn()

    def spawn(self):
        while self.x == -1 or self.y == -1:
            randX = random.randrange(0, rows)
            randY = random.randrange(0, rows)
            if len(snake.nodes) > 0:
                if snake.x_pos != randX and snake.y_pos != randY:
                    self.x = randX
                    self.y = randY
                for node in snake.nodes:
                    if node.x == randX and node.y == randY:
                        self.x = -1
                        self.y = -1
                        break

            else:
                if snake.x_pos != randX and snake.y_pos != randY:
                    self.x = randX
                    self.y = randY


snake = Snake()
apple = Apple()


def draw_snake(surface, x_between, y_between):
    snake_color = (0, 255, 0)
    snake_eye_color = (255, 255, 255)
    pygame.draw.rect(surface, snake_color, (x_between * snake.x_pos,
                                            y_between * snake.y_pos, x_between, y_between))

    for node in snake.nodes:
        pygame.draw.rect(surface, snake_color, (x_between *
                                                node.x, y_between * node.y, x_between, y_between))

    eye_size = x_between // 5

    if snake.x_dir == 1 and snake.y_dir == 0:
        pygame.draw.rect(surface, snake_eye_color, (x_between * snake.x_pos + (x_between -
                                                                               eye_size), y_between * snake.y_pos + (y_between - eye_size), eye_size, eye_size))
        pygame.draw.rect(surface, snake_eye_color, (x_between * snake.x_pos +
                                                    (x_between - eye_size), y_between * snake.y_pos, eye_size, eye_size))
    elif snake.x_dir == -1 and snake.y_dir == 0:
        pygame.draw.rect(surface, snake_eye_color, (x_between * snake.x_pos,
                                                    y_between * snake.y_pos + (y_between - eye_size), eye_size, eye_size))
        pygame.draw.rect(surface, snake_eye_color, (x_between *
                                                    snake.x_pos, y_between * snake.y_pos, eye_size, eye_size))
    elif snake.x_dir == 0 and snake.y_dir == 1:
        pygame.draw.rect(surface, snake_eye_color, (x_between * snake.x_pos + (x_between -
                                                                               eye_size), y_between * snake.y_pos + (y_between - eye_size), eye_size, eye_size))
        pygame.draw.rect(surface, snake_eye_color, (x_between * snake.x_pos,
                                                    y_between * snake.y_pos + (y_between - eye_size), eye_size, eye_size))
    elif snake.x_dir == 0 and snake.y_dir == -1:
        pygame.draw.rect(surface, snake_eye_color, (x_between * snake.x_pos +
                                                    (x_between - eye_size), y_between * snake.y_pos, eye_size, eye_size))
        pygame.draw.rect(surface, snake_eye_color, (x_between *
                                                    snake.x_pos, y_between * snake.y_pos, eye_size, eye_size))


def draw_apple(surface, x_between, y_between):
    pygame.draw.rect(surface, (255, 0, 0), (x_between * apple.x,
                                            y_between * apple.y, x_between, y_between))


def draw_map(surface):
    global width, height, rows, snake
    x_between = width // rows
    y_between = height // rows
    draw_apple(surface, x_between, y_between)
    draw_snake(surface, x_between, y_between)

    for i in range(rows):
        x = i * x_between
        y = i * y_between
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, height))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (width, y))


def update_screen(surface):
    surface.fill((0, 0, 0))
    draw_map(surface)
    pygame.display.update()


def start_timer_done(seconds) -> bool:
    if seconds <= 0:
        return True
    return False


def draw_start_screen(surface, seconds):
    surface.fill((0, 0, 0))
    pygame.font.init()
    start_font = pygame.font.SysFont("Arial", width // 5)
    start_msg = start_font.render(
        str(int(seconds)), True, (0, 0, 0), (255, 255, 255))
    start_msg_rect = start_msg.get_rect()
    start_msg_rect.center = (width // 2, height // 2)
    surface.blit(start_msg, start_msg_rect)
    pygame.display.update()


def draw_lose_screen(surface):
    pygame.font.init()
    lose_font = pygame.font.SysFont("Arial", width // 5)
    lose_msg = lose_font.render(
        "Retry? [y/n]", True, (0, 0, 0), (255, 255, 255))
    lose_msg_rect = lose_msg.get_rect()
    lose_msg_rect.center = (width // 2, height // 2)
    surface.blit(lose_msg,  lose_msg_rect)
    pygame.display.update()


def draw_win_screen(surface):
    pygame.font.init()
    win_font = pygame.font.SysFont("Arial", width // 10)
    win_msg = win_font.render(
        "You won! Retry? [y/n]", True, (0, 0, 0), (255, 255, 255))
    win_msg_rect = win_msg.get_rect()
    win_msg_rect.center = (width // 2, height // 2)
    surface.blit(win_msg,  win_msg_rect)
    pygame.display.update()


def main():
    global width, height, snake, apple
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    game_won = False
    game_over = False
    game_started = False
    timer = 2
    while game_over == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN and game_started == True:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    snake.set_dir(1, 0)
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    snake.set_dir(-1, 0)
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    snake.set_dir(0, -1)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    snake.set_dir(0, 1)
                elif (snake.is_alive == False or game_won == True) and event.key == pygame.K_y:
                    game_started = False
                    snake = Snake()
                    game_won = False
                elif (snake.is_alive == False or game_won == True) and event.key == pygame.K_n:
                    game_over = True

        if game_started == True:
            snake.check_is_alive()
            if game_won == True:
                draw_win_screen(screen)
            elif snake.is_alive == True:
                if snake.x_pos == apple.x and snake.y_pos == apple.y:
                    if len(snake.nodes) == rows ** 2 - 2:
                        game_won = True
                    else:
                        snake.grow()
                        apple = Apple()
                snake.move()
                update_screen(screen)
            elif snake.is_alive == False:
                draw_lose_screen(screen)

        else:
            timer -= clock.get_time() / 1000
            draw_start_screen(screen, timer)
            if start_timer_done(timer) == True:
                timer = 4
                game_started = True
        clock.tick(10)
    pygame.quit()
    sys.exit(0)


main()
