import sys


from settings import *
from player import Player
from tilemap import Tilemap
from button import Button

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Pick The Right Fruit")

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.display = pygame.Surface((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        self.clock = pygame.time.Clock()

        self.assets = {
            "terrain": load_images("terrain/solid_blocks"),
            "player": load_image("player/player.png"),
            "player_idle": load_images("player/idle"),
            "player_jump": load_image("player/player_jump.png"),
            "player_fall": load_image("player/player_fall.png"),
            "player_run": load_images("player/run"),
            "background": load_image("Background.png"),
            "apple": load_images("fruits/apple"),
            "banana": load_images("fruits/banana"),
            "kiwi": load_images("fruits/kiwi"),
            "orange": load_images("fruits/orange"),
            "circle": load_image("Circle.png"),
            "start1": load_image("button/start1.png"),
            "start2": load_image("button/start2.png"),
            "quit": load_image("button/quit.png"),
            "menu": load_image("button/menu.png")
        }

        self.sfx = {
            "jump": pygame.mixer.Sound("sound/jump.mp3"),
            "pickup": pygame.mixer.Sound("sound/pickup.wav"),
            "wrong_pickup": pygame.mixer.Sound("sound/wrong_pickup.mp3")
        }

        for item in self.sfx.values():
            item.set_volume(0.05)

        # Background shenanigans
        self.bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT)) # New Surface on which I repeated my background image
        self.background()
        self.background_positions = [[0, 0], [0, -WINDOW_HEIGHT + BG_SIZE / 2]]

        # defining all variables
        self.curr_fruit = None
        self.next_fruit = None
        self.game_points = None
        self.collected_fruits = None
        self.difficulty = None

        # Player shenanigans
        self.movement = None
        self.player = None

        # loading the level
        self.tilemap = None

        self.fruit_amount = None
        self.current_max_fruit = None
        self.correct_fruit_points = None
        self.wrong_fruit_points = None

        self.SPAWN_FRUIT = None

        self.TIME_AMOUNT = None
        self.speed_mod = None
        self.decrement = None

        self.curr_time = None
        self.TIMER = None

        self.scroll = None

        pygame.mixer.music.load("sound/background_music.wav")
        pygame.mixer.music.set_volume(0.02)
        pygame.mixer.music.play(-1)

    def run(self, level):

        menu_button = Button(96, self.screen.get_height() / 2 - 42, self.assets["menu"], 3, self.display)
        self.load_game(level)

        while True:

            if self.game_points <= 0:
                self.menu(self.collected_fruits)
                break

            # Background projection
            self.background_animation()

            # camera movement
            self.scroll[0] += int((self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 10)
            self.scroll[1] += int((self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 10)

            self.tilemap.render(self.display, offset = self.scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset = self.scroll)

            self.display.blit(pygame.transform.scale(self.assets["circle"], (48, 48)),  (0, 0))
            self.display.blit(pygame.transform.scale(self.assets[self.curr_fruit][0], (48, 48)),  (0, 0))

            self.display.blit(pygame.transform.scale(self.assets[self.next_fruit][0], (32, 32)),  (48, 8))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Movement
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                        self.player.orientation = -1
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                        self.player.orientation = 1
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3.3
                        self.sfx["jump"].play()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                if event.type == self.SPAWN_FRUIT:
                    if self.fruit_amount < self.current_max_fruit:
                        self.spawn_fruit()
                        self.fruit_amount = self.fruit_amount + 1
                if event.type == self.TIMER:
                    self.curr_time = self.curr_time - 1
                    if self.curr_time == -1:
                        self.curr_time = self.TIME_AMOUNT
                        self.ramp_up()

            self.display_timer()
            self.display_points()

            if menu_button.draw():
                self.menu(-1)
                break

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def menu(self, collected_fruits = -1):

        start1_button = Button(WINDOW_WIDTH / 4, 40, self.assets["start1"], 3, self.display)
        start2_button = Button(WINDOW_WIDTH / 4, 80, self.assets["start2"], 3, self.display)
        quit_button = Button(WINDOW_WIDTH / 4, 220, self.assets["quit"], 3, self.display)

        while True:

            self.background_animation()

            if collected_fruits != -1:
                score = f"Fruits last game: {collected_fruits}"
                text_surface = pygame.font.Font(None, 64).render(score, True, (255, 255, 255))
                self.display.blit(text_surface, (self.screen.get_width() / 4 - text_surface.get_width() / 2, 140))


            if start1_button.draw():
                self.run("1")
                break

            if start2_button.draw():
                self.run("2")
                break

            if quit_button.draw():
                pygame.quit()
                sys.exit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def spawn_fruit(self):
        if self.tilemap.fruit_amount[self.curr_fruit] == 0:
            self.tilemap.add_fruit(self.curr_fruit)
        else:
            self.tilemap.add_fruit(random.choice(list(ALL_FRUITS)))


    def background(self):
        bg_img = pygame.transform.scale(self.assets["background"], (BG_SIZE, BG_SIZE))
        for i in range(0, WINDOW_WIDTH, BG_SIZE):
            for j in range (0, WINDOW_HEIGHT, BG_SIZE):
                self.bg.blit(bg_img, (i, j))

    def background_animation(self):
        for pos in self.background_positions:
            pos[1] += SCROLL_SPEED

            if pos[1] >= WINDOW_HEIGHT - BG_SIZE / 2:
                pos[1] = - WINDOW_HEIGHT + BG_SIZE / 2

        # Blit the background
        for pos in self.background_positions:
            self.display.blit(self.bg, pos)

    def ramp_up(self):
        if self.current_max_fruit <= MAX_FRUIT:
            self.current_max_fruit += 1
        if self.difficulty >= 5:
            self.speed_mod += 0.1 / self.difficulty
        else:
            self.speed_mod += 0.1
        self.game_points -= self.decrement
        self.decrement = int(1.4 * self.decrement + 10 + 3 * self.difficulty)
        self.correct_fruit_points += self.difficulty + 1
        self.wrong_fruit_points += self.difficulty + 1
        self.difficulty += 1

    def display_timer(self):
        timer_text = f"Difficulty: {self.difficulty}   Time left: {self.curr_time}"
        text_surface = pygame.font.Font(None, 16).render(timer_text, True, (255, 255, 255))
        self.display.blit(text_surface, (self.screen.get_width() / 2 - text_surface.get_width() - 14, 7))

    def display_points(self):
        point_text = f"Points: {self.game_points} (next decrement: {self.decrement})"
        text_surface = pygame.font.Font(None, 16).render(point_text, True, (255, 255, 255))
        self.display.blit(text_surface, (self.screen.get_width() / 2 - text_surface.get_width() - 14, 21))

    def load_game(self, level):
        self.curr_fruit = random.choice(list(ALL_FRUITS))
        self.next_fruit = random.choice(list(ALL_FRUITS))
        self.game_points = 10
        self.collected_fruits = 0
        self.difficulty = 1

        # Player shenanigans
        self.movement = [False, False]

        self.player = Player(self, LEVEL_SPAWN_POS[int(level) - 1], (32, 32))

        # loading the level
        self.tilemap = Tilemap(self)
        self.tilemap.load_map("level_" + level)

        self.tilemap.load_spawnpoints("level_" + level + "_spawnpoints")
        self.fruit_amount = 0
        self.current_max_fruit = 30
        self.correct_fruit_points = 2
        self.wrong_fruit_points = 1

        self.SPAWN_FRUIT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_FRUIT, 2000)

        self.TIME_AMOUNT = 45
        self.speed_mod = 1.5
        self.decrement = 20

        self.curr_time = self.TIME_AMOUNT
        self.TIMER = pygame.USEREVENT + 3
        pygame.time.set_timer(self.TIMER, 1000)

        self.scroll = [self.player.rect().centerx - self.display.get_width() / 2, self.player.rect().centery - self.display.get_height() / 2]



game = Game()
game.menu() # display the start screen