import pygame
import os
import random
import datetime

pygame.init()

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chrome DINO in Python")
Icon = pygame.image.load("assets/DinoWallpaper.png")
pygame.display.set_icon(Icon)

RUNNING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoRun1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoRun2.png")),
]
JUMPING = pygame.image.load(os.path.join("assets/Dino", "DinoJump.png"))
DUCKING = [
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck1.png")),
    pygame.image.load(os.path.join("assets/Dino", "DinoDuck2.png")),
]
SMALL_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "SmallCactus3.png")),
]
LARGE_CACTUS = [
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus1.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("assets/Cactus", "LargeCactus3.png")),
]
BIRD = [
    pygame.image.load(os.path.join("assets/Bird", "Bird1.png")),
    pygame.image.load(os.path.join("assets/Bird", "Bird2.png")),
]
CLOUD = pygame.image.load(os.path.join("assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("assets/Other", "Track.png"))
FONT_COLOR = (0, 0, 0)

if not os.path.exists("score.txt"):
    with open("score.txt", "w") as f:
        f.write("0 ")

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0
        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not self.dino_jump:
            self.dino_duck = False
            self.dino_run = True

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        self.dino_rect.y -= self.jump_vel * 4
        self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.remove(self)

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    BIRD_HEIGHTS = [250, 290, 320]
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(self.BIRD_HEIGHTS)
        self.index = 0

    def draw(self, screen):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index // 5], self.rect)
        self.index += 1

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, FONT_COLOR
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacles = []
    death_count = 0
    pause = False

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        with open("score.txt", "r") as f:
            try:
                score_ints = [int(x) for x in f.read().split()]
            except:
                score_ints = [0]
        highscore = max(score_ints)
        if points > highscore:
            highscore = points
        text = font.render("Points: " + str(points), True, FONT_COLOR)
        text_rect = text.get_rect()
        text_rect.topright = (SCREEN_WIDTH - 20, 20)
        SCREEN.blit(text, text_rect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def paused():
        nonlocal pause, run
        pause = True
        font = pygame.font.Font("freesansbold.ttf", 30)
        text = font.render("Game Paused. Press 'u' to Unpause", True, FONT_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        SCREEN.blit(text, text_rect)
        pygame.display.update()
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    pause = False
                    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused()

        current_time = datetime.datetime.now().hour
        is_day = 7 < current_time < 19
        
        if is_day:
            SCREEN.fill((255, 255, 255))
            FONT_COLOR = (0, 0, 0)
        else:
            SCREEN.fill((0, 0, 0))
            FONT_COLOR = (255, 255, 255)

        userInput = pygame.key.get_pressed()
        player.update(userInput)
        player.draw(SCREEN)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            else:
                obstacles.append(Bird(BIRD))

        for obstacle in list(obstacles):
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(1000)
                with open("score.txt", "a") as f:
                    f.write(str(points) + " ")
                death_count += 1
                menu(death_count)

        background()
        cloud.draw(SCREEN)
        cloud.update()
        score()

        clock.tick(30)
        pygame.display.update()
    
    pygame.quit()
    quit()

def menu(death_count):
    global points, FONT_COLOR
    run = True
    font = pygame.font.Font("freesansbold.ttf", 30)
    while run:
        current_time = datetime.datetime.now().hour
        is_day = 7 < current_time < 19
        
        if is_day:
            SCREEN.fill((255, 255, 255))
            FONT_COLOR = (0, 0, 0)
        else:
            SCREEN.fill((0, 0, 0))
            FONT_COLOR = (255, 255, 255)

        if death_count == 0:
            message = "Press any key to Start"
        else:
            message = "Press any key to Restart"
        
        text = font.render(message, True, FONT_COLOR)
        SCREEN.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                main()

menu(death_count=0)