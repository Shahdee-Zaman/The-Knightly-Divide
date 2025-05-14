import pygame
"""
This class is responsible for spliting a sprite sheet to list and as well as combining multiple images into a list.
The 'split_sprite' method takes a sprite sheet as input and splits it into multiple frames and returns it as a list.
The 'combine_sprite' method takes a file_name as input and combines the incrementing files and returns them as a list.
The 'crop_bg' method removes the transparent background from the individual frames.(This may cause issues when transforming it aftwerwards.)
To resolve issue where your sprite may strech, you can remove the crop_bg method from being called automatically.
"""


# The Animate class takes 5 parameters.
# The character_image parameter is the file name where your sprite is held
# The num_of_frames allows split_sprite and combine_sprite to loop that amount of time to receive the whole image.
# Width and Height is the new size you would like your sprite to have.
# Offset is defaulted to 0 as it is only required for combine_sprite.
class Animate:
    def __init__(self, character_image, num_of_frames = 0, width = 25, height = 25, offset = 0,):
        self.character_image = character_image
        self.sprite = []
        self.num_of_frames = num_of_frames
        self.offset = offset
        self.width = width
        self.height = height

# split_sprite uses the num_of_frames to divide the sprite sheet that amount of times to get the complete animation.
# The width and height of sprites are then transformed to the value you inputed
    def split_sprite(self):
        self.frame_width = self.character_image.get_width() // self.num_of_frames
        for i in range(self.num_of_frames):
            frame = self.character_image.subsurface((i * self.frame_width, 0, self.frame_width, self.character_image.get_height()))
            frame_changed = self.crop_bg(frame)
            frame_changed = pygame.transform.scale(frame_changed, (int(self.width), int(self.height)))
            self.sprite.append(frame_changed)
        return self.get_sprite()

# To use combine_sprite ensure that your file names are in incremetal values. Such as: sprite_0, sprite_1,...,sprite_10.
# Do not have value itself when passing it through the parameter. Use "sprite_" when trying to pass "sprite_0.png"
# Use the offset parameter when you file name starts at a different value than 0.
    def combine_sprite(self):
        for i in range(self.num_of_frames):
            picture = pygame.image.load(f"{self.character_image}{i+self.offset}.png").convert_alpha()
            changed_picture = self.crop_bg(picture)
            changed_picture = pygame.transform.scale(changed_picture, (int(self.width), int(self.height)))
            self.sprite.append(changed_picture)
        return self.get_sprite()

    # The crop_bg removes the transparent background of the frames.
    # It may cause issues when the frames are different sizes without the transparent background.
    # crop_bg is automatically called by both split_sprite and combine_sprite.
    # You may remove it if it is causing some frames to be streched and instead change the hitbox of the sprite manually.
    def crop_bg(self, sprite):
        cropped_sprite = sprite.subsurface(sprite.get_bounding_rect())
        return cropped_sprite


    def get_sprite(self):

        return self.sprite

