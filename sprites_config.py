import pygame


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



# beige_cat = {}
# beige_cat.update({"idle":sprite_converter("sprites/beige_cat/Idle.png", 11, 64, 64)})
#
# test = len(beige_cat["idle"]["right"])
# print(test)
#
# beige_cat.update({"walk":sprite_converter("sprites/beige_cat/Walk.png", 5, 64, 64)})
# beige_cat.update({"dance":sprite_converter("sprites/beige_cat/Dance.png", 4, 64, 64)})
# beige_cat.update({"sleep":sprite_converter("sprites/beige_cat/Sleep.png", 4, 64, 64)})
# beige_cat.update({"cry":sprite_converter("sprites/beige_cat/Cry.png", 4, 64, 64)})
# #new
# beige_cat.update({"idle2":sprite_converter("sprites/beige_cat/Idle2.png", 10, 64, 64)})
# beige_cat.update({"excited":sprite_converter("sprites/beige_cat/Excited.png", 12, 64, 64)})
# beige_cat.update({"lay_down":sprite_converter("sprites/beige_cat/LayDown.png", 12, 64, 64)})
# beige_cat.update({"sad":sprite_converter("sprites/beige_cat/Sad.png", 8, 64, 64)})
# beige_cat.update({"sleepy":sprite_converter("sprites/beige_cat/Sleepy.png", 7, 64, 64)})
# beige_cat.update({"surprised":sprite_converter("sprites/beige_cat/Surprised.png", 12, 64, 64)})
# beige_cat.update({"waiting":sprite_converter("sprites/beige_cat/Waiting.png", 6, 64, 64)})
# beige_cat.update({"eating":sprite_converter("sprites/beige_cat/Eating.png", 14, 64, 64)})
# beige_cat.update({"sad_idle":sprite_converter("sprites/beige_cat/Sad_Idle.png", 10, 64, 64)})
# beige_cat.update({"angry_idle":sprite_converter("sprites/beige_cat/Angry_Idle.png", 10, 64, 64)})
# beige_cat.update({"happy_idle":sprite_converter("sprites/beige_cat/Happy_Idle.png", 10, 64, 64)})
# beige_cat.update({"sleepy_idle":sprite_converter("sprites/beige_cat/Sleepy_Idle.png", 10, 64, 64)})
#
# black_cat = {}
# black_cat.update({"walk":sprite_converter("sprites/black_cat/Walk.png", 5, 64, 64)})
# black_cat.update({"dance":sprite_converter("sprites/black_cat/Dance.png", 4, 64, 64)})
# black_cat.update({"sleep":sprite_converter("sprites/black_cat/Sleep.png", 4, 64, 64)})
# black_cat.update({"cry":sprite_converter("sprites/black_cat/Cry.png", 4, 64, 64)})
# #new
# black_cat.update({"idle2":sprite_converter("sprites/black_cat/Idle2.png", 10, 64, 64)})
# black_cat.update({"excited":sprite_converter("sprites/black_cat/Excited.png", 12, 64, 64)})
# black_cat.update({"lay_down":sprite_converter("sprites/black_cat/LayDown.png", 12, 64, 64)})
# black_cat.update({"sad":sprite_converter("sprites/black_cat/Sad.png", 8, 64, 64)})
# black_cat.update({"sleepy":sprite_converter("sprites/black_cat/Sleepy.png", 7, 64, 64)})
# black_cat.update({"surprised":sprite_converter("sprites/black_cat/Surprised.png", 12, 64, 64)})
# black_cat.update({"waiting":sprite_converter("sprites/black_cat/Waiting.png", 6, 64, 64)})
# black_cat.update({"eating":sprite_converter("sprites/black_cat/Eating.png", 14, 64, 64)})
# black_cat.update({"sad_idle":sprite_converter("sprites/black_cat/Sad_Idle.png", 10, 64, 64)})
# black_cat.update({"angry_idle":sprite_converter("sprites/black_cat/Angry_Idle.png", 10, 64, 64)})
# black_cat.update({"happy_idle":sprite_converter("sprites/black_cat/Happy_Idle.png", 10, 64, 64)})
# black_cat.update({"sleepy_idle":sprite_converter("sprites/black_cat/Sleepy_Idle.png", 10, 64, 64)})


import os

color_variants = ["beige_cat", "black_cat", "white_cat"]

cats_dictionary = {}

folder = "sprites"


for color_variant in color_variants: # go through each color variant
    folder_path = os.path.join(folder,color_variant) #sprites/color_variant
    cats_dictionary[color_variant] = {} # create a dictionary for the color variant

    for sprite in os.listdir(folder_path): # go through each sprite
        sprite_path = os.path.join(folder_path, sprite) # get the correct path to the sprite

        animation_name = sprite[:-4]  # create the name

        cats_dictionary[color_variant].update({animation_name: sprite_converter(sprite_path, 64, 64)}) # seperate the sprites

        if "lay_down" in sprite_path: print(sprite_path)

