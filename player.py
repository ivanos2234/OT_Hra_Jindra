import random

import pygame

from settings import *

class Player:
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collision = {"up": False, "down": False, "right": False, "left": False}
        self.curr_img = game.assets["player"]
        self.curr_idle_frame = 0
        self.curr_run_frame = 0
        self.frame = 0
        self.orientation = 1 # 1 = right, -1 = left

    def rect(self):
        return pygame.Rect(self.pos[0] + 5, self.pos[1] + 6, self.size[0] - 10, self.size[1] - 6)

    def update(self, tilemap, movement = (0, 0)):
        self.collision = {"up": False, "down": False, "right": False, "left": False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        self.animation(frame_movement)

        # collision detection (scanning adjacent tiles) while moving along the x-axis
        self.pos[0] += frame_movement[0] * self.game.speed_mod
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0: # moving right
                    entity_rect.right = rect.left - 5
                    self.collision["right"] = True
                if frame_movement[0] < 0: # moving left
                    entity_rect.left = rect.right - 5
                    self.collision["left"] = True
                self.pos[0] = entity_rect.x

        # collision detection (scanning adjacent tiles) while moving along the y-axis
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0: # moving (falling) down
                    entity_rect.bottom = rect.top - 6
                    self.collision["down"] = True
                if frame_movement[1] < 0: # moving up
                    entity_rect.top = rect.bottom - 6
                    self.collision["up"] = True
                self.pos[1] = entity_rect.y

        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        if self.collision["down"] or self.collision["up"]:
            self.velocity[1] = 0

        entity_rect = self.rect()
        for tile, rect in tilemap.colectibles_around(self.pos):
            if entity_rect.colliderect(rect):
                if tile["type"] == self.game.curr_fruit:
                    self.game.sfx["pickup"].play()
                    self.game.game_points = self.game.game_points + self.game.correct_fruit_points
                    self.game.curr_fruit = self.game.next_fruit
                    self.game.collected_fruits = self.game.collected_fruits + 1
                    self.game.next_fruit = random.choice(list(ALL_FRUITS))
                else:
                    self.game.sfx["wrong_pickup"].play()
                    self.game.game_points = self.game.game_points - self.game.wrong_fruit_points
                tilemap.tilemap.pop(str(tile["pos"][0]) + ";" + str(tile["pos"][1]), None)
                tilemap.fruit_amount[tile["type"]] = tilemap.fruit_amount[tile["type"]] - 1
                self.game.fruit_amount = self.game.fruit_amount - 1


    def animation(self, frame_movement, img_dur = 2):
        if self.frame == img_dur: # system for frames being on screen longer than one frame
            self.frame = (self.frame + 1) % (img_dur + 1)
            if frame_movement[1] >= 1:
                self.curr_idle_frame = 0
                self.curr_run_frame = 0
                self.curr_img = self.game.assets["player_fall"]

            elif frame_movement[1] < 0:
                self.curr_idle_frame = 0
                self.curr_run_frame = 0
                self.curr_img = self.game.assets["player_jump"]

            elif frame_movement[0] != 0:
                self.curr_idle_frame = 0
                self.curr_img = self.game.assets["player_run"][self.curr_run_frame]
                self.curr_run_frame = (self.curr_run_frame + 1) % len(self.game.assets["player_run"])

            else:
                self.curr_run_frame = 0
                self.curr_img = self.game.assets["player_idle"][self.curr_idle_frame]
                self.curr_idle_frame = (self.curr_idle_frame + 1) % len(self.game.assets["player_idle"])
        else:
            self.frame = (self.frame + 1) % (img_dur + 1)

    def render(self, surf, offset):
        if self.orientation == -1:
            surf.blit(pygame.transform.flip(self.curr_img, True, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        else:
            surf.blit(self.curr_img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))