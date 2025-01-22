import pygame
import os
import random

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 700
BG_SIZE = 128
TILE_SIZE = 16
SCROLL_SPEED = 1
LEVEL_SPAWN_POS = [(28 * TILE_SIZE, 54 * TILE_SIZE), (23 * TILE_SIZE, 96 * TILE_SIZE)]
ALL_FRUITS = {"apple", "banana", "kiwi", "orange"}
MAX_FRUIT = 50

BASE_IMG_PATH = 'sprites/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0)) # Make black in the image transparent
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + "/" + img_name))
    return images

def map_to_2dArr(level_name):
    level_map = []
    with open("levels/" + level_name + ".txt", "r") as f:
        for riadok in f:
            riadok = [int(i) - 1 for i in riadok.strip()[:-1].split(", ")]
            level_map.append(riadok)
    return level_map