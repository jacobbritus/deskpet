import pygame


def sprite_converter(sprite_file, sprites, sprite_width, sprite_height):
    sprite = pygame.image.load(sprite_file)

    sprite_dict = {
    "left": [],
    "right": [],
}
    x = 0
    y = 0

    for i in range(sprites):
        # get a cut based on the column (y) and the row (x)
        rect = pygame.Rect(x, y, sprite_width, sprite_height)
        image = sprite.subsurface(rect)

        # adds the different directions to a list in a dict

        sprite_dict["left"].append(image)
        right = pygame.transform.flip(image, True, False)
        sprite_dict["right"].append(right)

        x += sprite_width

    return sprite_dict


black_cat = {}
black_cat.update({"idle":sprite_converter("sprites/black_cat/Idle.png", 10, 64, 64)})
black_cat.update({"sad_idle":sprite_converter("sprites/black_cat/Sad_Idle.png", 10, 64, 64)})

black_cat.update({"walk":sprite_converter("sprites/black_cat/Walk.png", 5, 64, 64)})
black_cat.update({"dance":sprite_converter("sprites/black_cat/Dance.png", 4, 64, 64)})
black_cat.update({"sleep":sprite_converter("sprites/black_cat/Sleep.png", 4, 64, 64)})
black_cat.update({"cry":sprite_converter("sprites/black_cat/Cry.png", 4, 64, 64)})

beige_cat = {}
beige_cat.update({"idle":sprite_converter("sprites/beige_cat/Idle.png", 10, 64, 64)})
beige_cat.update({"walk":sprite_converter("sprites/beige_cat/Walk.png", 5, 64, 64)})
beige_cat.update({"dance":sprite_converter("sprites/beige_cat/Dance.png", 4, 64, 64)})
beige_cat.update({"sleep":sprite_converter("sprites/beige_cat/Sleep.png", 4, 64, 64)})
beige_cat.update({"cry":sprite_converter("sprites/beige_cat/Cry.png", 4, 64, 64)})
#new
beige_cat.update({"idle2":sprite_converter("sprites/beige_cat/Idle2.png", 10, 64, 64)})
beige_cat.update({"excited":sprite_converter("sprites/beige_cat/Excited.png", 12, 64, 64)})
beige_cat.update({"dead":sprite_converter("sprites/beige_cat/DeadCat.png", 2, 64, 64)})
beige_cat.update({"lay_down":sprite_converter("sprites/beige_cat/LayDown.png", 12, 64, 64)})
beige_cat.update({"sad":sprite_converter("sprites/beige_cat/Sad.png", 8, 64, 64)})
beige_cat.update({"sleepy":sprite_converter("sprites/beige_cat/Sleepy.png", 7, 64, 64)})
beige_cat.update({"surprised":sprite_converter("sprites/beige_cat/Surprised.png", 12, 64, 64)})
beige_cat.update({"waiting":sprite_converter("sprites/beige_cat/Waiting.png", 6, 64, 64)})
beige_cat.update({"eating":sprite_converter("sprites/beige_cat/Eating.png", 14, 64, 64)})
beige_cat.update({"sad_idle":sprite_converter("sprites/beige_cat/Sad_Idle.png", 10, 64, 64)})
beige_cat.update({"angry_idle":sprite_converter("sprites/beige_cat/Angry_Idle.png", 10, 64, 64)})
beige_cat.update({"happy_idle":sprite_converter("sprites/beige_cat/Happy_Idle.png", 10, 64, 64)})
beige_cat.update({"sleepy_idle":sprite_converter("sprites/beige_cat/Sleepy_Idle.png", 10, 64, 64)})
