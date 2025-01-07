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

        self.tile_sheet = pg.image.load('assets/verden/sheet.png').convert_alpha()
        self.TILE_SIZE = 32  # Tile dimensions

        # Load tiles from tile sheet
        self.tiles = self.load_tiles(self.tile_sheet, self.TILE_SIZE, target_size=100)

        # Map layout
        self.map_layout = [
            [65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65],
            [5, 6, 7, 8, 9],
            [10, 11, 12, 13, 14],
            [15, 16, 17, 18, 19],
            [20, 21, 22, 23, 24]
        ]

        # Initialize camera
        
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.new()

    def new(self):        
        self.showdialogue=False
        self.dialoguenumb=0
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
        self.E=False
        self.timerdialogues=0
        self.timerE=0
        self.running = True
        self.run()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

        pg.quit()
    def dialogue(self):
        if self.dialoguenumb==0:
            self.dialogue_text= self.font.render("Yo wassup", True, (255,255,255,255))
        if self.dialoguenumb==1:
            self.dialogue_text= self.font.render("I'm not old, YOU ARE", True, (255,255,255,255))
        self.showdialogue=True

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

    def update(self):
        self.all_sprites.update()
        self.camera.center_on_player(self.player)
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
        if not Interact or self.showdialogue==True:
            self.E=False
        if Interact and self.showdialogue==False:
            self.interact= self.font.render("Press E", True, (255,255,0,255))
            self.E=True
        if keys[pg.K_e] and Interact:
            self.dialogue()
            self.player.notMove()
        if keys[pg.K_ESCAPE]:
            self.running=False


    def draw(self):
        self.screen.fill((50, 50, 50))

        # Draw the tile map with the camera offset
        for row_index, row in enumerate(self.map_layout):
            for col_index, tile_index in enumerate(row):
                x = col_index * 100
                y = row_index * 100
                if tile_index >= 0:  # Only draw valid tiles
                    tile_rect = pg.Rect(x, y, 100, 100)
                    tile_rect = self.camera.apply(tile_rect)
                    self.screen.blit(self.tiles[tile_index], tile_rect.topleft)

        self.all_sprites.draw(self.screen)
        if self.showdialogue==True:
            self.screen.blit(self.dialogue_text, (520, 350))
            self.timerdialogues+=1

        if self.E:
            self.screen.blit(self.interact, (520, 350))
        if(self.timerdialogues>=100):
            self.timerdialogues=0
            if not self.dialoguenumb==2:
                self.dialoguenumb+=1
            self.showdialogue=False
            if self.dialoguenumb==2:
                self.player.Move()

        pg.display.flip()

    def load_tiles(self, tile_sheet, tile_size, target_size=100):
        tiles = []
        sheet_width, sheet_height = tile_sheet.get_size()

        for y in range(0, sheet_height, tile_size):
            for x in range(0, sheet_width, tile_size):
                tile = tile_sheet.subsurface((x, y, tile_size, tile_size))

                scaled_tile = pg.transform.scale(tile, (target_size, target_size))
                tiles.append(scaled_tile)

        return tiles


if __name__ == "__main__":
    Game()
