import pygame
import random
import music
import environment
import saves
import math
import sys
pygame.init()
def checkLimits(entity):
    if (entity.x > SCREEN_WIDTH):
        entity.x = SNAKE_SIZE
    if (entity.x < 0):
        entity.x = SCREEN_WIDTH - SNAKE_SIZE
    if (entity.y > SCREEN_HEIGHT):
        entity.y = SNAKE_SIZE
    if (entity.y < 0):
        entity.y = SCREEN_HEIGHT - SNAKE_SIZE
class Food:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state
        self.color = pygame.color.Color("red")

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, APPLE_SIZE, APPLE_SIZE), 0)
class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.color = "white"
class Snake:
    state = "play"
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "play"
        self.direction = KEY["UP"]
        self.stack = []
        self.stack.append(self)
        blackBox = Segment(self.x, self.y + SEPARATION)
        blackBox.direction = KEY["UP"]
        blackBox.color = "NULL"
        self.stack.append(blackBox)
    def move(self):
        last_element = len(self.stack) - 1
        while (last_element != 0):
            self.stack[last_element].direction = self.stack[last_element - 1].direction
            self.stack[last_element].x = self.stack[last_element - 1].x
            self.stack[last_element].y = self.stack[last_element - 1].y
            last_element -= 1
        if (len(self.stack) < 2):
            last_segment = self
        else:
            last_segment = self.stack.pop(last_element)
        last_segment.direction = self.stack[0].direction
        if (self.stack[0].direction == KEY["UP"]):
            last_segment.y = self.stack[0].y - (SPEED * fps)
        elif (self.stack[0].direction == KEY["DOWN"]):
            last_segment.y = self.stack[0].y + (SPEED * fps)
        elif (self.stack[0].direction == KEY["LEFT"]):
            last_segment.x = self.stack[0].x - (SPEED * fps)
        elif (self.stack[0].direction == KEY["RIGHT"]):
            last_segment.x = self.stack[0].x + (SPEED * fps)
        self.stack.insert(0, last_segment)
    def getHead(self):
        return (self.stack[0])
    def grow(self):
        last_element = len(self.stack) - 1
        self.stack[last_element].direction = self.stack[last_element].direction
        if (self.stack[last_element].direction == KEY["UP"]):
            newSegment = Segment(self.stack[last_element].x, self.stack[last_element].y - SNAKE_SIZE)
            blackBox = Segment(newSegment.x, newSegment.y - SEPARATION)

        elif (self.stack[last_element].direction == KEY["DOWN"]):
            newSegment = Segment(self.stack[last_element].x, self.stack[last_element].y + SNAKE_SIZE)
            blackBox = Segment(newSegment.x, newSegment.y + SEPARATION)

        elif (self.stack[last_element].direction == KEY["LEFT"]):
            newSegment = Segment(self.stack[last_element].x - SNAKE_SIZE, self.stack[last_element].y)
            blackBox = Segment(newSegment.x - SEPARATION, newSegment.y)

        elif (self.stack[last_element].direction == KEY["RIGHT"]):
            newSegment = Segment(self.stack[last_element].x + SNAKE_SIZE, self.stack[last_element].y)
            blackBox = Segment(newSegment.x + SEPARATION, newSegment.y)

        blackBox.color = "NULL"
        self.stack.append(newSegment)
        self.stack.append(blackBox)
    def setDirection(self, direction):
        if (self.direction == KEY["RIGHT"] and direction == KEY["LEFT"] or self.direction == KEY[
            "LEFT"] and direction == KEY["RIGHT"]):
            pass
        elif (self.direction == KEY["UP"] and direction == KEY["DOWN"] or self.direction == KEY["DOWN"] and direction ==
              KEY["UP"]):
            pass
        else:
            self.direction = direction
    def get_rect(self):
        rect = (self.x, self.y)
        return rect
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def setX(self, x):
        self.x = x
    def setY(self, y):
        self.y = y
    def checkCrash(self):
        counter = 1
        while (counter < len(self.stack) - 1):
            if (checkCollision(self.stack[0], SNAKE_SIZE, self.stack[counter], SNAKE_SIZE) and self.stack[
                counter].color != "NULL"):
                self.state = "Gameover"
                return True
            counter += 1
        return False
    def draw(self, screen):
        pygame.draw.rect(screen, pygame.color.Color(0, 255, 0),
                         (self.stack[0].x, self.stack[0].y, SNAKE_SIZE, SNAKE_SIZE), 0)
        counter = 1
        while (counter < len(self.stack)):
            if (self.stack[counter].color == (0, 255, 0)):
                counter += 1
                continue
            pygame.draw.rect(screen, pygame.color.Color(0, 200, 0),
                             (self.stack[counter].x, self.stack[counter].y, SNAKE_SIZE, SNAKE_SIZE), 0)
            counter += 1
def getKey():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                return KEY["UP"]
            elif event.key == pygame.K_DOWN:
                return KEY["DOWN"]
            elif event.key == pygame.K_LEFT:
                return KEY["LEFT"]
            elif event.key == pygame.K_RIGHT:
                return KEY["RIGHT"]
            elif event.key == pygame.K_ESCAPE:
                music.play_music(music.music_for_menu[0])
                return "exit"
            elif event.key == pygame.K_y:
                return "yes"
            elif event.key == pygame.K_n:
                return "no"
            elif event.key == pygame.K_p:
                return "pause"

        if event.type == pygame.QUIT:
            sys.exit()
def respawnApple(apples, index, sx, sy):
    radius = math.sqrt((SCREEN_WIDTH / 2 * SCREEN_WIDTH / 2 + SCREEN_HEIGHT / 2 * SCREEN_HEIGHT / 2)) / 2
    angle = 999
    while (angle > radius):
        angle = random.uniform(0, 800) * math.pi * 2
        x = SCREEN_WIDTH / 2 + radius * math.cos(angle)
        y = SCREEN_HEIGHT / 2 + radius * math.sin(angle)
        if (x == sx and y == sy):
            continue
    newApple = Food(x, y, 1)
    apples[index] = newApple
def respawnApples(apples, quantity, sx, sy):
    counter = 0
    del apples[:]
    radius = math.sqrt((SCREEN_WIDTH / 2 * SCREEN_WIDTH / 2 + SCREEN_HEIGHT / 2 * SCREEN_HEIGHT / 2)) / 2
    angle = 999
    while (counter < quantity):
        while (angle > radius):
            angle = random.uniform(0, 800) * math.pi * 2
            x = SCREEN_WIDTH / 2 + radius * math.cos(angle)
            y = SCREEN_HEIGHT / 2 + radius * math.sin(angle)
            if ((x - APPLE_SIZE == sx or x + APPLE_SIZE == sx) and (
                    y - APPLE_SIZE == sy or y + APPLE_SIZE == sy) or radius - angle <= 10):
                continue
        apples.append(Food(x, y, 1))
        angle = 999
        counter += 1
def endGame():
    message = game_over_font.render("Game Over", 1, pygame.Color("white"))
    message_play_again = play_again_font.render("Play Again? Y/N", 1, pygame.Color("green"))
    screen.blit(message, (320, 240))
    screen.blit(message_play_again, (320 + 12, 240 + 40))
    pygame.display.flip()
    pygame.display.update()
    myKey = getKey()
    while (myKey != "exit"):
        if (myKey == "yes"):
            game()
        elif (myKey == "no"):
            break
        myKey = getKey()
        clock.tick(fps)
    sys.exit()
def drawScore(score):
    score_numb = score_numb_font.render(str(score), 1, pygame.Color("red"))
    screen.blit(score_msg, (SCREEN_WIDTH - score_msg_size[0] - 60, 10))
    screen.blit(score_numb, (SCREEN_WIDTH - 45, 14))
def drawGameTime(gameTime):
    game_time = score_font.render("Time:", 1, pygame.Color("green"))
    game_time_numb = score_numb_font.render(str(gameTime / 1000), 1, pygame.Color("red"))
    screen.blit(game_time, (30, 10))
    screen.blit(game_time_numb, (105, 14))
def game():
    music.play_music(music.music_for_game[0])
    score = 0
    # Snake initialization
    mySnake = Snake(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    mySnake.setDirection(KEY["UP"])
    mySnake.move()
    start_segments = 3

    while (start_segments > 0):
        mySnake.grow()
        mySnake.move()
        start_segments -= 1

    max_apples = 1
    eaten_apple = False
    apples = [Food(random.randint(60, SCREEN_WIDTH), random.randint(60, SCREEN_HEIGHT), 1)]
    respawnApples(apples, max_apples, mySnake.x, mySnake.y)

    startTime = pygame.time.get_ticks()
    endgame = 0
    pause = False
    while (endgame != 1):
        clock.tick(fps)
        # Input
        keyPress = getKey()
        if keyPress == "exit":
            endgame = 1
        # Collision check
        checkLimits(mySnake)
        if (mySnake.checkCrash() == True):
            endGame()

        for myApple in apples:
            if (myApple.state == 1):
                if (checkCollision(mySnake.getHead(), SNAKE_SIZE, myApple, APPLE_SIZE) == True):
                    music.food_sound.play()
                    mySnake.grow()
                    myApple.state = 0
                    score += 5
                    eaten_apple = True

        # Position Update
        if (keyPress):
            mySnake.setDirection(keyPress)
        mySnake.move()
        # Respawning apples
        if (eaten_apple == True):
            eaten_apple = False
            respawnApple(apples, 0, mySnake.getHead().x, mySnake.getHead().y)
        # Drawing
        screen.blit(background, (0, 0))
        for myApple in apples:
            if (myApple.state == 1):
                myApple.draw(screen)

        mySnake.draw(screen)
        drawScore(score)
        gameTime = pygame.time.get_ticks() - startTime
        drawGameTime(gameTime)

        pygame.display.flip()
        pygame.display.update()

def text_objects(text, font_edit):
    text_surface = font_edit.render(text, True, (255, 255, 255))
    return text_surface, text_surface.get_rect()
class Button:

    def __init__(self, message, x, y, width, height, inactive_color, active_color):
        self.message = message
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inactive_color = inactive_color
        self.active_color = active_color

    def print_text(self):
        text_surf, text_rect = text_objects(self.message, environment.menu_font)
        text_rect.center = ((self.x + (self.width / 2)), (self.y + (self.height / 2)))
        screen.blit(text_surf, text_rect)

    def show_button(self):
        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            pygame.draw.rect(screen, self.active_color, (self.x, self.y, self.width, self.height))
            if click[0] == 1:
                self.print_text()
                return True
        else:
            pygame.draw.rect(screen, self.inactive_color, (self.x, self.y, self.width, self.height))
        self.print_text()
        return False
def checkCollision(posA, As, posB, Bs):
    # As size of a | Bs size of B
    if (posA.x < posB.x + Bs and posA.x + As > posB.x and posA.y < posB.y + Bs and posA.y + As > posB.y):
        return True
    return False

SPEED = 0.36
SNAKE_SIZE = 9
APPLE_SIZE = SNAKE_SIZE
SEPARATION = 10
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
KEY = {"UP": 1, "DOWN": 2, "LEFT": 3, "RIGHT": 4}
score_font = pygame.font.Font(None, 38)
score_numb_font = pygame.font.Font(None, 28)
game_over_font = pygame.font.Font(None, 46)
play_again_font = score_numb_font
score_msg = score_font.render("Score:", 1, pygame.Color("green"))
score_msg_size = score_font.size("Score")
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
background = pygame.image.load("fon.png").convert()
background = pygame.transform.smoothscale(background, screen.get_size())
pygame.display.update()
pygame.display.set_caption("Змейка")

clock = pygame.time.Clock()
fps = 25
def show_menu():
    if start_button.show_button() is True:
        game()
        #menu.set_play_menu()
    if options_button.show_button() is True:
        menu.set_settings()
    if exit_button.show_button() is True:
        quit_game()
def show_settings():

    music_volume_text = environment.menu_font.render("Volume: " + str(int(round(menu.music_volume * 10, 0))), True,
                                                     environment.WHITE)
    sounds_volume_text = environment.menu_font.render("Volume: " + str(int(round(menu.sound_volume * 10, 0))), True,
                                                      environment.WHITE)
    screen.blit(music_volume_text, [275, 100])
    screen.blit(sounds_volume_text, [275, 200])
    screen.blit(environment.text_sound, [300, 155])
    screen.blit(environment.text_music, [310, 55])
    if increase_sound_button.show_button() is True:
        menu.increase_sound_volume()
    if decrease_sound_button.show_button() is True:
        menu.decrease_sound_volume()
    if increase_music_button.show_button() is True:
        menu.increase_music_volume()
    if decrease_music_button.show_button() is True:
        menu.decrease_music_volume()
    if increase_difficult_button.show_button() is True:
        menu.increase_difficult()
    if decrease_difficult_button.show_button() is True:
        menu.decrease_difficult()
    difficult_text = environment.menu_font.render("Difficulty: " + find_difficult(), True, environment.green)
    screen.blit(difficult_text, (235, 300))
    if new_game_button.show_button() is True:
        saves.set_zero_saves()
    if back_button.show_button() is True:
        menu.set_main_menu()

difficult_slovar = {0: 'Easy', 1: 'Norm', 2: 'Hard', 3: 'HELL'}

def find_difficult():
    return difficult_slovar.get(menu.difficulty)
class Menu:

    state = "main"
    lives = 3
    difficulty = 0
    music_volume = 0.5
    sound_volume = 0.5
    accepts = [
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],
    ]

    def __init__(self, state, diffuculty, lives, music_volume, sound_volume):
        self.state = state
        self.difficulty = diffuculty
        self.lives = lives
        self.music_volume = music_volume
        self.sound_volume = sound_volume
        self.set_accepts()

    def set_settings(self):
        self.state = "settings"
    def set_play_menu(self):
        self.state = "play menu"
    def set_main_menu(self):
        self.state = "main"
    def increase_difficult(self):
        if self.difficulty <= 2:
            self.difficulty += 1
    def decrease_difficult(self):
        if self.difficulty >= 1:
            self.difficulty -= 1
    def increase_music_volume(self):
        self.music_volume = music.increase_volume(self.music_volume)
        pygame.mixer.music.set_volume(self.music_volume)
    def decrease_music_volume(self):
        self.music_volume = music.decrease_volume(self.music_volume)
        pygame.mixer.music.set_volume(self.music_volume)
    def increase_sound_volume(self):
        self.sound_volume = music.increase_volume(self.sound_volume)
        music.new_sound_volume(self.sound_volume)
    def decrease_sound_volume(self):
        self.sound_volume = music.decrease_volume(self.sound_volume)
        music.new_sound_volume(self.sound_volume)
    def set_accepts(self):
        self.accepts = saves.set_saves(self.accepts)
def quit_game():
    pygame.quit()
    quit()

start_button = Button("Play!", 300, 150, 200, 50, environment.BLACK, environment.green)
exit_button = Button("Quit", 300, 350, 200, 50, environment.BLACK, environment.green)
options_button = Button("Options", 300, 250, 200, 50, environment.BLACK, environment.green)
increase_music_button = Button("+", 575, 100, 50, 50, environment.BLACK, environment.green)
decrease_music_button = Button("-", 175, 100, 50, 50, environment.BLACK, environment.red)
increase_sound_button = Button("+", 575, 200, 50, 50, environment.BLACK, environment.green)
decrease_sound_button = Button("-", 175, 200, 50, 50, environment.BLACK, environment.red)
increase_difficult_button = Button("+", 575, 300, 50, 50, environment.BLACK, environment.green)
decrease_difficult_button = Button("-", 175, 300, 50, 50, environment.BLACK, environment.red)
back_button = Button("Back", 300, 500, 200, 50, environment.BLACK, environment.red)
new_game_button = Button("New game", 275, 400, 250, 55, environment.BLACK, environment.green)

menu = Menu("main", 0, 3, 0.5, 0.5)
pygame.mixer.music.set_volume(menu.music_volume)
play = False

number_of_music_menu = music.random_music_for_menu()

while not play:
    screen.blit(background, (0, 0))
    if pygame.mixer.music.get_busy() is False:
        number_of_music_menu = music.random_music_for_menu()
    screen.blit(environment.text_play, [220, 600])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = True
        if menu.lives == 0:
            saves.set_zero_saves()
            menu.accepts = saves.set_saves(menu.accepts)
            menu.lives = 3
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()

        if menu.state == "main":
            show_menu()
        elif menu.state == "settings":
            show_settings()
            menu.accepts = saves.set_saves(menu.accepts)
        pygame.display.update()
