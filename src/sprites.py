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
        self.Cooldown = 0
        self.direction="Right"

    def update(self):
        dt = self.game.clock.get_time() / 1000
        keys = pg.key.get_pressed()
        speed_multiplier = 1.5 if keys[pg.K_LSHIFT] else 1


        if(self.Cooldown>0):
            self.Cooldown-=1
        
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
            self.direction= "Left"
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            direction_x = 1
            self.direction= "Right"
        if keys[pg.K_SPACE]:
            self.attack()

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

    def attack(self):
        if self.Cooldown == 0:
            self.Cooldown = 30
            if(self.direction=="Right"):
                attack = MeleeAttack((self.rect.right+5, self.rect.centery))
            elif(self.direction=="Left"):
                attack = MeleeAttack((self.rect.left-5, self.rect.centery))
            self.game.attacks_group.add(attack)
            self.game.all_sprites.add(attack)



class Lady(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("assets/blob/OldLady.png")
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.y = 500
        self.rect.x = 640
        self.game=game
    def talk(self):
        print("Collided")


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("assets/blob/LightningKnight.png")
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.y = 100
        self.rect.x = 800

class MeleeAttack(pg.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pg.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=position)
        self.lifetime = 10
    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0: 
            self.kill()

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, colour):
        image = pg.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pg.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)

        return image

class CameraGrupe(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()

        self.offset = pg.math.Vector2() 

        self.ground_surf = pg.image.load('assets/verden/sheet.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))
    
    def custom_draw(self):
        self.display_surface.blit(self.ground_surf, self.ground_rect)
