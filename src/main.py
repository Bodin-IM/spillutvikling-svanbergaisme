import pygame as pg
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption('The Rune to The Future')
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("Comic Sans MS", 30)
        
        # Load sprite sheet image and create SpriteSheet object
        self.sprite_sheet_image = pg.image.load('assets/verden/sheet.png').convert_alpha()
        self.sprite_sheet = SpriteSheet(self.sprite_sheet_image)

        # Load a specific frame from the sprite sheet
        self.frame_0 = self.sprite_sheet.get_image(0, 32, 32, 1, (0, 0, 0))  # Example frame (0th frame)
        
        self.new()

    def new(self):        
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self.screen, self)
        self.all_sprites.add(self.player)
        self.lady = Lady(self)
        self.enemy = Enemy()
        self.enemies=pg.sprite.Group()
        self.npcs=pg.sprite.Group()
        self.npcs.add(self.lady)
        self.enemies.add(self.enemy)
        self.all_sprites.add(self.lady)
        self.all_sprites.add(self.enemy)
        self.attacks_group = pg.sprite.Group()
        self.running = True
        self.run()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

        pg.quit()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def update(self):
        self.all_sprites.update()
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            attack = self.player.attack()
            if attack:
                self.all_sprites.add(attack)
        collider = pg.sprite.groupcollide(self.attacks_group, self.enemies, False, False)
        Interact = pg.sprite.spritecollide(self.player, self.npcs, False)
        if collider:
            self.enemy.kill()
        keys = pg.key.get_pressed()
        if keys[pg.K_e] and Interact:
            self.lady.talk()


    def draw(self):
        self.screen.fill((50, 50, 50))

        self.screen.blit(self.frame_0, (100, 100))

        self.all_sprites.draw(self.screen)

        pg.display.flip()

if __name__ == "__main__":
    Game()
