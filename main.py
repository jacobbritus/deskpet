import pygame
import win32api
import win32con
import win32gui
import os
from win32api import GetSystemMetrics


from sprites_config import beige_cat
from pet import Pet

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
window_width = GetSystemMetrics(0)
window = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)

# make pygame background invisible
fuchsia = (255, 0, 128)  # Transparency color
# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

# Set windows always on top
win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)


display_text = False


cat = Pet(
    window = window,
    display_width = window_width,
    sprite_dict = beige_cat,
    spawn_coordinates = (320, 80),
    speed = 0.1,
    frame = 0,
)

while True:
    window.fill((255, 255, 255))
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # make the pet draggable if left mouse button is held down
        # event.button represents left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                cat.mouse_action = "grab"
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cat.meow()
                cat.mouse_action = "pet"
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            ...
            # chat.get_position(cat.x)
            # chat.open_chat()
        elif event.type == pygame.MOUSEBUTTONUP and event.button in [1, 2, 3]:
                cat.mouse_action = None
                pygame.mouse.set_visible(True) # make cursor visible again

    window.fill(fuchsia)


    cat.draw_self()
    clock.tick(120)


    pygame.display.update()

