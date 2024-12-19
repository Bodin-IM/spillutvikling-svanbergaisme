import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, screen, game):
        super().__init__()
        self.screen = screen
        self.game = game
        self.image = pg.image.load("assets/blob/FirstArmor.png")
        self.image = pg.transform.scale(self.image, (100, 100))  # Player size: 100x100
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.pos = pg.Vector2(self.rect.center)
        self.speed = 300
        self.gravity = 10
        self.jumping = False
        self.jump_timer = 0

    def update(self):
        dt = self.game.clock.get_time() / 1000
        keys = pg.key.get_pressed()
        speed_multiplier = 1.5 if keys[pg.K_LSHIFT] else 1

        # Direction Vector
        direction_x = 0
        direction_y = 0

        # Check Input for Movement
        if keys[pg.K_w] or keys[pg.K_UP]:
            direction_y = -1
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            direction_y = 1
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            direction_x = -1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            direction_x = 1

        # Normalize Movement
        magnitude = (direction_x ** 2 + direction_y ** 2) ** 0.5
        if magnitude > 0:
            direction_x /= magnitude
            direction_y /= magnitude

        # Apply Movement
        self.pos.x += direction_x * self.speed * dt * speed_multiplier
        self.pos.y += direction_y * self.speed * dt * speed_multiplier

        # Boundary Handling
        self.pos.x = max(0, min(SCREEN_WIDTH - self.rect.width, self.pos.x))
        self.pos.y = max(0, min(SCREEN_HEIGHT - self.rect.height, self.pos.y))

        self.rect.topleft = self.pos

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, colour):
        image = pg.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pg.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)

        return image

class Enemy(pg.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.image = pg.image.load("assets/enemy/1enemy.webp") #First enemy
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        self.pos = pg.Vector2(self.rect.center)
    
    def update(self):
        self.pos.x += 1
        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = -self.rect.width
        self.rect.topleft = self.pos