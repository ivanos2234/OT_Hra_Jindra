from settings import *

NEIGHBOR_OFFSETS = []
for i in (-2, -1, 0, 1, 2):
    for j in (-2, -1, 0, 1, 2):
        NEIGHBOR_OFFSETS.append((i, j))
PHYSICS_TILES = {"terrain"}

class Tilemap:
    def __init__(self, game):
        self.game = game
        self.tilemap = {}
        self.fruit_amount = {"apple": 0, "banana": 0, "kiwi": 0, "orange": 0}
        self.spawnpoint_map = set()
        self.fruit_frames = 17
        self.frame = 0
        self.curr_frame = 0

        for i in range(50):
            self.tilemap[str(3 + i) + ";10"] = {"type": "rock", "variant": 1, "pos": (3 + i, 10)}
            self.tilemap["10;" + str(5 + i)] = {"type": "rock", "variant": 3, "pos": (10, 5 + i)}

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // TILE_SIZE), int(pos[1] // TILE_SIZE))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile["type"] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile["pos"][0] * TILE_SIZE, tile["pos"][1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return rects

    def colectibles_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile["type"] != "terrain":
                rects.append((tile, pygame.Rect(tile["pos"][0] * TILE_SIZE + TILE_SIZE / 4, tile["pos"][1] * TILE_SIZE + TILE_SIZE / 4, TILE_SIZE * 3/4, TILE_SIZE * 3/4)))
        return rects

    def render(self, surf, offset, img_dur = 3):
        if self.frame == img_dur:
            self.frame = (self.frame + 1) % (img_dur + 1)
        else:
            for loc in self.tilemap:
                tile = self.tilemap[loc]
                if tile["type"] == "terrain":
                    surf.blit(self.game.assets[tile["type"]][tile["variant"]], (tile["pos"][0] * TILE_SIZE - offset[0], tile["pos"][1] * TILE_SIZE - offset[1]))
                else:
                    surf.blit(self.game.assets[tile["type"]][self.curr_frame], (tile["pos"][0] * TILE_SIZE - offset[0], tile["pos"][1] * TILE_SIZE - offset[1]))
            self.curr_frame = (self.curr_frame + 1) % self.fruit_frames

    def load_map(self, level):
        level_map = map_to_2dArr(level)

        for x in range(len(level_map)):
            for y in range(len(level_map[x])):
                if level_map[x][y] != -1:
                    self.tilemap[str(y) + ";" + str(x)] = {"type": "terrain", "variant": level_map[x][y], "pos": (y, x)}

    def load_spawnpoints(self, level):
        spawnpoint_map = map_to_2dArr(level)

        for x in range(len(spawnpoint_map)):
            for y in range(len(spawnpoint_map[x])):
                if spawnpoint_map[x][y] != -1:
                    self.spawnpoint_map.add((y, x))

    def add_fruit(self, fruit):
        pos = random.choice(list(self.spawnpoint_map))
        for i in range(5):
            while self.tilemap.get(str(pos[0]) + ";" + str(pos[1])) is not None:
                pos = random.choice(list(self.spawnpoint_map))
            else:
                break

        self.fruit_amount[fruit] = self.fruit_amount[fruit] + 1
        self.tilemap[str(pos[0]) + ";" + str(pos[1])] = {"type": fruit, "pos": pos}

