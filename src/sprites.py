import pygame as pg
from settings import *

class Camera:
    def __init__(self, width, height):
        self.offset = pg.Vector2(0, 0)
        self.target_offset = pg.Vector2(0, 0)
        self.width = width
        self.height = height
        self.smoothness = 0.1

    def center_on_player(self, player):
        self.target_offset.x = player.pos.x + player.rect.width // 2 - SCREEN_WIDTH // 2
        self.target_offset.y = player.pos.y + player.rect.height // 2 - SCREEN_HEIGHT // 2
        self.offset.x += (self.target_offset.x - self.offset.x) * self.smoothness
        self.offset.y += (self.target_offset.y - self.offset.y) * self.smoothness

    def apply(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)


class Player(pg.sprite.Sprite):
    def __init__(self, screen, game):
        super().__init__()
        self.screen = screen
        self.game = game
        self.image = pg.image.load("assets/blob/FirstArmor.png")
        self.Right1 = pg.image.load("assets/blob/PlayerWalk (1).png")
        self.Right2 = pg.image.load("assets/blob/PlayerWalk (2).png")
        self.Right3 = pg.image.load("assets/blob/PlayerWalk (3).png")
        self.Left1 = pg.image.load("assets/blob/PlayerWalkLeft (1).png")
        self.Left2 = pg.image.load("assets/blob/PlayerWalkLeft (2).png")
        self.Left3 = pg.image.load("assets/blob/PlayerWalkLeft (3).png")
        self.image = pg.transform.scale(self.image, (100, 100))
        self.Right1 = pg.transform.scale(self.Right1, (100, 100))
        self.Right2 = pg.transform.scale(self.Right2, (100, 100))
        self.Right3 = pg.transform.scale(self.Right3, (100, 100))
        self.Left1 = pg.transform.scale(self.Left1, (100, 100))
        self.Left2 = pg.transform.scale(self.Left2, (100, 100))
        self.Left3 = pg.transform.scale(self.Left3, (100, 100))
        self.current_frame = 0
        self.last_update = 0
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.pos = pg.Vector2(self.rect.center)
        self.canMove = True
        self.speed = 300
        self.Cooldown = 0
        self.direction = "Right"
        self.standing = True
        self.rightframes= [self.Right1, self.Right2, self.Right3]
        self.leftframes= [self.Left1, self.Left2, self.Left3]

    def update(self):
        dt = self.game.clock.get_time() / 1000
        keys = pg.key.get_pressed()
        speed_multiplier = 1.5 if keys[pg.K_LSHIFT] else 1
        self.standing = True

        if self.Cooldown > 0:
            self.Cooldown -= 1

        direction_x, direction_y = 0, 0
        if keys[pg.K_w]  and self.canMove:
            direction_y = -1
        if keys[pg.K_s]  and self.canMove:
            direction_y = 1
        if keys[pg.K_a] and self.canMove:
            direction_x = -1
            self.direction = "Left"
            self.standing=False
            self.Animate()
        if keys[pg.K_d] and self.canMove:
            direction_x = 1
            self.direction = "Right"
            self.standing=False
            self.Animate()

        magnitude = (direction_x ** 2 + direction_y ** 2) ** 0.5
        if magnitude > 0:
            direction_x /= magnitude
            direction_y /= magnitude

        self.pos.x += direction_x * self.speed * dt * speed_multiplier
        self.pos.y += direction_y * self.speed * dt * speed_multiplier
        self.rect.topleft = self.pos

    def Animate(self):
        now=pg.time.get_ticks()
        if not self.standing:
            if now - self.last_update > 150:
                self.last_update = now
                if self.direction == "Right":
                    self.current_frame = (self.current_frame + 1) % len(self.rightframes)
                elif self.direction == "Left":
                    self.current_frame = (self.current_frame + 1) % len(self.leftframes)
                self.image = self.rightframes[self.current_frame]
                self.rect = self.image.get_rect()
           
    def attack(self):
        if self.Cooldown == 0:
            self.Cooldown = 30
            position = (self.rect.right + 5, self.rect.centery) if self.direction == "Right" else (self.rect.left - 5, self.rect.centery)
            attack = MeleeAttack(position)
            self.game.attacks_group.add(attack)
            self.game.all_sprites.add(attack)

    def notMove(self):
        self.canMove = False

    def Move(self):
        self.canMove = True


class Lady(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.image = pg.image.load("assets/blob/OldLady.png")
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.y, self.rect.x = 500, 640
        self.game = game


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("assets/blob/LightningKnight.png")
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.y, self.rect.x = 100, 800


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
