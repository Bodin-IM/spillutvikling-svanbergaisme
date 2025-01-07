import pygame as pg
from settings import *
from sprites import *

class Camera:
    def __init__(self, width, height):
        self.offset = pg.Vector2(0, 0)
        self.width = width
        self.height = height

    def center_on_player(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH // 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT // 2

    def apply(self, rect):
        return rect.move(-self.offset.x, -self.offset.y)

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
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self.screen, self)
        self.all_sprites.add(self.player)
        self.lady = Lady(self)
        self.enemy = Enemy()
        self.enemies = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
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

        # Draw all sprites with the camera offset
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))

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
