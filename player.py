# coding: utf-8
""" This module contains the Player class and related methods.
    It is used by the main game loop, to generate the player character. """
import os

import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT


class Player(pygame.sprite.Sprite):
    """ Player class docstring"""
    def __init__(self, level):
        super().__init__()
        self.x, self.y = level.get_start_tile()
        self.bag = []
        absolute_path = os.path.join(os.path.dirname(__file__), "assets", "MacGyver.png")
        self.image = pygame.image.load(absolute_path)
        self.surf = pygame.Surface((50, 50))
        self.rect = self.surf.get_rect(topleft=(50 * self.x, 50 * self.y))

    def draw(self, surface):
        """Draws the player on the grid"""
        surface.blit(self.image, self.rect)
    
    def draw_bag(self, surface):
        try:
            for index, value in enumerate(self.bag):
                surf = pygame.Surface((50, 50))
                rect = surf.get_rect(topleft=(150 + 50 * index, 750))
                img_filename = value.content + ".png"
                absolute_path = os.path.join(os.path.dirname(__file__), "assets", img_filename)
                image = pygame.image.load(absolute_path)
                surface.blit(image, rect)
        except AttributeError:
            pass

    def update(self, level, screen_width, screen_height):
        """Updates MacGyver's position on the grid,
        according to the direction given by the player.
        Move is not allowed if the target tile is blocked by something
        (wall or map boundary)"""
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0 and pressed_keys[K_UP]and level.can_move(self.x, self.y - 1):
            self.rect.move_ip(0, -50)
            self.y -= 1
        if self.rect.bottom < screen_height and pressed_keys[K_DOWN] and level.can_move(self.x, self.y + 1):
            self.rect.move_ip(0, 50)
            self.y += 1
        if self.rect.left > 0 and pressed_keys[K_LEFT] and level.can_move(self.x - 1, self.y):
            self.rect.move_ip(-50, 0)
            self.x -= 1
        if self.rect.right < screen_width and pressed_keys[K_RIGHT] and level.can_move(self.x + 1, self.y):
            self.rect.move_ip(50, 0)
            self.x += 1
        self.pick_item(level)

    def has_found_exit(self, level):
        """Returns True if the player reached the exit tile"""
        return level.is_exit_tile(self.x, self.y)

    def pick_item(self, level):
        """ If there is an item on the tile,
            picks it and put in MacGyver's bag """
        try:
            if level.get_tile_element(self.x, self.y) and level.get_tile_element(self.x, self.y) not in self.bag:
                self.bag.append(level.get_tile_element(self.x, self.y))
                level.get_tile_element(self.x, self.y).is_picked = True
                print("Picked", level.get_tile_element(self.x, self.y).content)
        except AttributeError:
            pass

    def has_picked_all_items(self):
        """Checks if Player has picked all 3 items"""
        return len(self.bag) == 3
