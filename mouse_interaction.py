import math

import pyautogui
import pygame
import threading


class Mouse:
    def __init__(self, window):
        self.window = window
        self.cursor_position = pygame.mouse.get_pos()
        self.mouse_action = None
        self.cat_position = None

        pass



    def mouse_interaction(self, cat, display_width):
        # get the mouse x and y position on the screen
        cursor_position = pygame.mouse.get_pos()

        # create a collision point box with the pet's location and sprite size
        cat_rect = pygame.Rect(cat.x, cat.y, cat.width, cat.height)


        # follow the cursor if right click
        if self.mouse_action == "follow":
            cat.follow = True  # toggle following
            threading.Thread(daemon=True,
                             target=self.get_cursor_position).start()  # get the cursor location on the background


        # check if the cursor is within the sprite's image
        if cat_rect.collidepoint(cursor_position[0], cat.y):
            if cat.toggle_speech_bubble:
                cat.draw_speech_bubble(display_width) # display speech bubble when just hovering over

            # if angry walk away
            if cat.mood == "angry":
                cat.current_animation = "walk"

                if not cat_rect.collidepoint(cursor_position[0], cat.y):
                    cat.current_animation = "lay_down"

            # if a mouse button is being clicked
            if self.mouse_action:
                # reposition the pet using the mouse
                if self.mouse_action == "grab":

                    if cat.mood == "angry":
                        cat.mouse_action = "cancel"
                    else:
                        off_set = cat.width // 2 # go to the sprite's middle
                        cat.x = cursor_position[0] - off_set # clamps the sprite to the mouse

                # call function to pet and low chance to make happy
                elif self.mouse_action == "pet":
                    cat.uplift_when_pet()



                pygame.mouse.set_visible(False)  # make cursor invisible
                self.cursor_sprite(self.mouse_action)  # change cursor sprite based on the action

        else:
            cat.no_pet_time += 0.1





    def get_cursor_position(self):
        while True:
            self.cursor_position = pyautogui.position()



    def following(self, cat, cat_amount):

        if cat.follow:
            dist = math.hypot(cat.x - self.cursor_position[0])

            # if close to cursor or if colliding with other cats stop walking
            if dist <= 64:
                pass
            else:
                if self.cursor_position[0] > cat.x:
                    cat.direction = "right"
                    cat.current_animation = "walk"

                else:
                    cat.direction = "left"
                    cat.current_animation = "walk"



    def cursor_sprite(self, form):
        center = 8 # go to the cursor's middle
        distance_to_head = 32 # go to sprite's head for grab
        cursor_position = pygame.mouse.get_pos()


        # custom cursor sprites and their positions
        cursors = {
            "grab":
                {"image":pygame.image.load("Sprites/cursor/Win95DefGrab.png"),
                 "location": (cursor_position[0] - center, cursor_position[1] - distance_to_head)  # get coordinates on screen mouse
                    },
            "pet": {
                "image":pygame.image.load("Sprites/cursor/Win95DefPalm.png"),
                "location": (cursor_position[0] - center, cursor_position[1]) # get coordinates on screen mouse
                    },
            "cancel": {
                "image": pygame.image.load("Sprites/cursor/Win95Cancel.png"),
                "location": (cursor_position[0] - center, cursor_position[0]) # get coordinates on screen mouse
            },
            "follow": {
                "image": pygame.image.load("Sprites/cursor/Win95DefHand.png"),
                "location": (self.cursor_position[0] - center, self.cursor_position[1]) # get coordinates off screen mouse
            },
        }
         # print the custom cursor sprite at the right position
        self.window.blit(cursors[form]["image"], cursors[form]["location"]) # print it on the window





    def run(self, cat, cat_amount, display_width):
        self.mouse_interaction(cat, display_width)
        self.following(cat, cat_amount)
