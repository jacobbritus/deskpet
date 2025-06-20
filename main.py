import random

import pygame
import win32api
import win32con
import win32gui
import os
from win32api import GetSystemMetrics

from mouse_interaction import Mouse
from pet import Pet
from sprites_config import color_variants

# initialize pygame
pygame.init()
pygame.font.init() # initialize displaying text
clock = pygame.time.Clock()

# move window position down to have pet on top of taskbar
window_height = 150

display_height = GetSystemMetrics(1)
taskbar_height = 40  # estimate
y = display_height - window_height - taskbar_height

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(0, y)

# set window width to display width
display_width = GetSystemMetrics(0)
window = pygame.display.set_mode((display_width, window_height), pygame.NOFRAME)

# make pygame background invisible
fuchsia = (255, 0, 128)  # Transparency color
# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

# Set windows always on top
win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)


sizes = ["small", "medium"]
sizes_dict = {"small": {"size": (32, 32), "y": 32 + 80},
              "medium": {"size": (64, 64), "y": 80}}


mouse = Mouse(window)

cats = [Pet(window=window,
            color_variant= "beige_cat",
            size= sizes_dict["medium"]["size"],
            spawn_coordinates=(random.randint(0, display_width), sizes_dict["medium"]["y"]),
            speed=0.1,
            frame=0, )]


while True:
    window.fill((255, 255, 255))
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


        # click "a" to spawn more cats
        if event.type == pygame.KEYDOWN:
            # add a new cat if a pressed
            if event.key == pygame.K_a:
                color = random.choice(color_variants)
                size = random.choice(sizes)
                size_num = sizes_dict[size]["size"]
                spawn = (random.randint(0, display_width), sizes_dict[size]["y"])
                cats.append(Pet(window=window,
                                color_variant=color,
                                size = size_num,
                                spawn_coordinates=(random.randint(0, display_width), sizes_dict[size]["y"]),
                                speed=0.1,
                                frame=0, ))

            # click "s" to toggle speech bubble
            if event.key == pygame.K_s:
                for cat in cats:
                    if cat.toggle_speech_bubble:
                        cat.toggle_speech_bubble = False
                    else:
                        cat.toggle_speech_bubble = True
                        cat.mood_change = False

        # make the pet draggable if left mouse button is held down
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                mouse.mouse_action = "grab"

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse.mouse_action = "pet"

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            for cat in cats:
                if cat.follow:
                    cat.follow = False
                else:
                    mouse.mouse_action = "follow"


        elif event.type == pygame.MOUSEBUTTONUP and event.button in [1, 2, 3]:
                mouse.mouse_action = None
                pygame.mouse.set_visible(True) # make cursor visible again




    window.fill(fuchsia)

    for cat in cats:
        cat.draw_self(display_width)
        mouse.run(cat, len(cats), display_width)

    # detect collisions (pure brain muscles this one lol)
    Pet.detect_collision(cats)

    clock.tick(120)


    pygame.display.update()

