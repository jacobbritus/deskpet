import math

import pyautogui
import pygame
import threading


class Mouse:
    def __init__(self, window):
        self.window = window
        self.cursor_position = pygame.mouse.get_pos()
        self.mouse_action = None
        self.selected_cat = None
        self.grabbing = False


    def mouse_interaction(self, display_width, cats):
        # get the mouse x and y position on the screen
        cursor_position = pygame.mouse.get_pos()

        for index, cat in enumerate(cats):
            # create a collision point box with the pet's location and sprite size
            cat_rect = pygame.Rect(cat.x, cat.y, cat.width, cat.height)


            # check if the cursor is within a cat's rectangle
            if cat_rect.collidepoint(cursor_position[0], cursor_position[1]) and not self.grabbing:
                self.selected_cat = cats[index] # select the cat the cursor is on

                if self.selected_cat.toggle_speech_bubble and cat.mood:
                    self.selected_cat.draw_speech_bubble(display_width) # display speech bubble when just hovering over

                # if angry walk away
                if self.selected_cat.mood == "angry":
                    self.selected_cat.current_animation = "walk"

                # if a mouse button is being clicked
                if self.mouse_action:

                    # follow the cursor if right click
                    if self.mouse_action == "follow":
                        self.selected_cat.follow = True  # toggle following
                        self.selected_cat = self.selected_cat
                        threading.Thread(daemon=True,
                                         target=self.get_cursor_position).start()  # get the cursor location on the background


                    # reposition the pet using the mouse
                    if self.mouse_action == "grab" and not self.grabbing:

                        if self.selected_cat.mood == "angry":
                            self.selected_cat.mouse_action = "cancel"
                        else:
                            self.grabbing = True


                    # call function to pet and low chance to make happy
                    elif self.mouse_action == "pet":
                        self.selected_cat.uplift_when_pet()


                    pygame.mouse.set_visible(False)  # make cursor invisible
                    self.cursor_sprite(self.mouse_action)  # change cursor sprite based on the action

                else:
                    pass

            else:
                cat.no_pet_time += 0.1


    def grab(self):
        cursor_position = pygame.mouse.get_pos()

        off_set = self.selected_cat.width // 2  # go to the sprite's middle
        self.selected_cat.x = cursor_position[0] - off_set  # clamps the sprite to the mouse

        self.selected_cat.y = cursor_position[1] - off_set  # clamps the sprite to the mouse

        if self.selected_cat.mood == "angry":
            self.selected_cat.mouse_action = "cancel"

        pygame.mouse.set_visible(False)  # make cursor invisible
        self.cursor_sprite(self.mouse_action)  # change cursor sprite based on the action


    def get_cursor_position(self):
        while True:
            self.cursor_position = pyautogui.position()


    def following(self):
        if self.selected_cat.follow:
            dist = math.hypot(self.selected_cat.x - self.cursor_position[0])

            # if close to cursor or if colliding with other cats stop walking
            if dist <= 64:
                pass
            else:
                if self.cursor_position[0] > self.selected_cat.x:
                    self.selected_cat.direction = "right"
                    self.selected_cat.current_animation = "walk"

                else:
                    self.selected_cat.direction = "left"
                    self.selected_cat.current_animation = "walk"



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





    def run(self, display_width, cats):
        self.mouse_interaction( display_width, cats)

        if self.selected_cat.follow: self.following()
        if self.grabbing: self.grab()
