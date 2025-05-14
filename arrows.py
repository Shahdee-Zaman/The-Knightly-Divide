import pygame

"""
    The Arrows class is responsible for drawing objects passed through the image parameter.
    It drops an object corresponding to how many times it is called.
    the image parameter takes a list of images that can be cycled through to create an animation.
    The x parameter is the starting x-coordinate and the y parameter is the starting y-coordinate in the grid.
"""
class Arrows(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.sprite = image
        # We start at the first animation
        self.current_sprite = 0
        self.image = self.sprite[self.current_sprite]
        # The variable stores the properties of image for later use
        self.rect = self.image.get_rect()
        self.rect.topleft = [x,y]


    # Speed parameter controls how fast the object is falling.
    # The sprite animation speed is set .307 for each frame loop.
    def update(self, speed):
        self.rect.y += speed
        self.current_sprite += .307
        if self.current_sprite >= len(self.sprite):
            self.current_sprite = 0
        self.image = self.sprite[int(self.current_sprite)]


