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
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.pos = pg.Vector2(self.rect.center)
        self.canMove = True
        self.speed = 300
        self.Cooldown = 0
        self.direction = "Right"

        self.health_bar = HealthBar(self)

    def update(self):
        dt = self.game.clock.get_time() / 1000
        keys = pg.key.get_pressed()
        speed_multiplier = 1.5 if keys[pg.K_LSHIFT] else 1

        if self.Cooldown > 0:
            self.Cooldown -= 1

        direction_x, direction_y = 0, 0
        if keys[pg.K_w] and self.canMove:
            direction_y = -1
        if keys[pg.K_s] and self.canMove:
            direction_y = 1
        if keys[pg.K_a] and self.canMove:
            direction_x = -1
            self.direction = "Left"
        if keys[pg.K_d] and self.canMove:
            direction_x = 1
            self.direction = "Right"

        magnitude = (direction_x ** 2 + direction_y ** 2) ** 0.5
        if magnitude > 0:
            direction_x /= magnitude
            direction_y /= magnitude

        self.pos.x += direction_x * self.speed * dt * speed_multiplier
        self.pos.y += direction_y * self.speed * dt * speed_multiplier
        self.rect.topleft = self.pos

    def draw_health_bar(self, screen):
        self.health_bar.draw(screen)

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

class HealthBar:
    def __init__(self, player, width=200, height=20, x_offset=10, y_offset=10):
        self.player = player
        self.max_health = 100  # Max health value
        self.current_health = 100  # Current health value
        self.width = width
        self.height = height
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.font = pg.font.SysFont("Comic Sans MS", 14, bold=True)  # Bold font

    def take_damage(self, amount):
        self.current_health = max(0, self.current_health - amount)

    def heal(self, amount):
        self.current_health = min(self.max_health, self.current_health + amount)

    def draw(self, screen):
        # Positioning the health bar at the bottom left corner
        screen_width, screen_height = screen.get_size()
        x_pos = self.x_offset
        y_pos = screen_height - self.height - self.y_offset

        # Background bar (red)
        bar_rect = pg.Rect(x_pos, y_pos, self.width, self.height)
        pg.draw.rect(screen, (255, 0, 0), bar_rect)

        # Foreground (current health) bar (green)
        health_ratio = self.current_health / self.max_health
        current_health_rect = pg.Rect(
            x_pos, y_pos, int(self.width * health_ratio), self.height
        )
        pg.draw.rect(screen, (0, 255, 0), current_health_rect)

        # Draw current health number inside the bar
        health_text = f"{self.current_health}"
        text_surface = self.font.render(health_text, True, (0, 0, 0))  # Black text
        text_rect = text_surface.get_rect(center=(x_pos + self.width // 2, y_pos + self.height // 2))
        screen.blit(text_surface, text_rect)
