import pygame
import os


def sprite_converter(sprite_file, sprite_width, sprite_height):
    sprite_file = pygame.image.load(sprite_file)

    sprite_dict = {
    "left": [],
    "right": [],
}
    x = 0
    y = 0

    for i in range(15):
        # get a cut based on the column (y) and the row (x)
        rect = pygame.Rect(x, y, sprite_width, sprite_height)
        try:
            image = sprite_file.subsurface(rect)
        except ValueError:
            return sprite_dict

        # adds the different directions to a list in a dict

        sprite_dict["left"].append(image)
        right = pygame.transform.flip(image, True, False)
        sprite_dict["right"].append(right)

        x += sprite_width

    return sprite_dict

color_variants = ["beige_cat", "black_cat", "white_cat", "grey_cat", "orange_cat", "brown_cat"]

cats_dictionary = {}

folder = "sprites"


for color_variant in color_variants: # go through each color variant
    folder_path = os.path.join(folder,color_variant) #sprites/color_variant
    cats_dictionary[color_variant] = {} # create a dictionary for the color variant

    for sprite in os.listdir(folder_path): # go through each sprite
        sprite_path = os.path.join(folder_path, sprite) # get the correct path to the sprite

        animation_name = sprite[:-4].lower()  # create the name

        cats_dictionary[color_variant].update({animation_name: sprite_converter(sprite_path, 64, 64)}) # seperate the sprites


