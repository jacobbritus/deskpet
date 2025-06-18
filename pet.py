import random
import math
import threading

import pygame.mouse
from datetime import datetime
import pyautogui

class Pet:
    def __init__(self, window, display_width, sprite_dict, spawn_coordinates, speed, frame):
        self.window = window
        self.display_width = display_width

        self.sprite_dict = sprite_dict
        self.x, self.y = spawn_coordinates
        self.speed = speed
        self.direction = None
        self.frame = frame
        self.cooldown = 0
        self.current_animation = None
        self.mood = None
        self.mouse_action = None
        self.width = self.height = 64
        self.no_pet_time = 0
        self.meow_cooldown = 0
        self.mood_change = False
        self.speech_bubble_frame = 0
        self.follow = False
        self.mouse = None
        self.rect = None


        # dict used to get a random animation it holds all the animations  and the extra info that belongs to each
        self.all_animations = None

    @staticmethod
    def sound(file):

        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

    # function for sounds
    def meow(self):

        # different cat sound variations
        meows = ["meow6"]

        # play sound every 60 ticks
        if self.meow_cooldown >= 60 and self.mood != "sleepy":
            # initializing the sound
            file = "sounds/" + random.choice(meows) + ".mp3"
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()

            # reset cooldown
            self.meow_cooldown = 0

        self.meow_cooldown += 0.1


    # stay inside window
    def borders(self):

        # this could be increased in the future to make the pet bounce back which could be funny
        bounce_back = 1

        # stop moving when touching right border
        if self.x >= self.display_width - self.width: # minus sprite width for the right collision point
            self.x =  self.display_width - (self.width + bounce_back) # bounce back
            self.direction = "left" # turn left

        # stop moving when touching left border
        if self.x <= 0 : # already collides as the collision point starts at the sprite's upper left corner
            self.x = bounce_back # bounce back
            self.direction = "right" # turn right

    # perform random actions
    def random_action(self):
        # list used to get a random direction
        directions = ["left", "right"]
        animation_rarity = ["mood", "common", "uncommon"]
        weights = [0.7, 0.2, 0.1]

        # initialize
        # this is going to change in the future as i'll save and load all information
        if self.current_animation is None:
            self.update_mood() # set up mood
            random_rarity = random.choices(animation_rarity, k=1, weights=weights)[0] # pick a random rarity
            possible_animations = [key for key in self.all_animations.keys() if self.all_animations[key]["weight"] == random_rarity]

            self.current_animation = random.choice(possible_animations) # choose a random animation matching random rarity
            self.direction = random.choice(directions) # choose a random direction
            self.cooldown = 0  # reset cooldown


        # do something random when the cooldown is up
        elif self.cooldown > self.all_animations[self.current_animation]["cooldown"]:
            self.update_mood() # update mood
            # pick a random rarity
            random_rarity = random.choices(animation_rarity, k=1, weights=weights)[0]

            # add the animations to a list which weight match the random weight
            possible_animations = [key for key in self.all_animations.keys() if self.all_animations[key]["weight"] == random_rarity]
            self.current_animation = random.choice(possible_animations) # choose a random animation matching random rarity
            self.direction = random.choice(directions) # choose a random direction

            # play sound IF sound
            try:
                track_name = self.all_animations[self.current_animation]["sound"]
                self.sound(f"sounds/{track_name}.mp3")
            except KeyError:
                pass



            self.cooldown = 0 # reset cooldown

        self.cooldown += 0.1





    # initialize different dictionaries depending on the mood

    def update_mood(self):
        turn_angry = 25
        turn_sad = 100
        sleepy_time = (20, 5)

        current_hour = datetime.now().hour

        # change mood if sleepy within a certain time frame
        if self.mood != "sleepy" and sleepy_time[0] <= current_hour or self.mood != "sleepy" and current_hour <= sleepy_time[1]:
            self.mood = "sleepy"
            self.mood_change = True

        elif self.mood != "happy" and self.no_pet_time < turn_angry and self.mood != "sleepy":
            self.mood = "happy"
            self.speed = 1.5
            self.mood_change = True


        # change mood to angry if not pet and not angry already
        elif not self.mood == "angry" and turn_sad > self.no_pet_time > turn_angry and self.mood != "sleepy":
            self.mood = "angry"
            self.mood_change = True

        # change mood to sad if not pet and not sad already
        elif not self.mood == "sad" and self.no_pet_time > turn_sad and self.mood != "sleepy":
            self.mood = "sad"
            self.speed = 0.3
            self.mood_change = True

        else:
            self.mood_change = False

        # play sound if mood change for clarity
        if self.mood_change:
            Pet.sound(f"sounds/{self.mood}_sound.mp3")

        # call function to match current mood with its unique animations
        self.animations()

    def animations(self):
        base_cooldown = 50
        longer_cooldown = 70
        sleep_cooldown = 1000

        # base animations
        self.all_animations = {
                "waiting": {"cooldown": base_cooldown, "weight": "common"},
                "lay_down": {"cooldown": base_cooldown, "weight": "common"},
                "walk": {"cooldown": longer_cooldown, "weight": "common"},
                "eating": {"cooldown": base_cooldown, "weight": "uncommon"},
                "idle2": {"cooldown": base_cooldown, "weight": "uncommon"},
            }
        if self.mood == "happy":
            self.all_animations.update({
                "happy_idle": {"cooldown": base_cooldown, "weight": "mood"},
                "dance": {"cooldown": base_cooldown, "weight": "mood"},
                "excited": {"cooldown": base_cooldown, "weight": "mood"},
                "surprised": {"cooldown": base_cooldown, "weight": "mood"},
            })
        elif self.mood == "sleepy":
            self.all_animations.update({
                "sleepy_idle": {"cooldown": base_cooldown, "weight": "mood"},
                "sleep": {"cooldown": sleep_cooldown, "weight": "mood", "sound": "sleep_sound"},
                "sleepy": {"cooldown": base_cooldown, "weight": "mood"},
            })
        elif self.mood == "sad":
            self.all_animations.update({
                "cry": {"cooldown": base_cooldown, "weight": "mood"},
                "sad_idle": {"cooldown": base_cooldown, "weight": "mood"},
                "sad": {"cooldown": base_cooldown, "weight": "mood"}})
        elif self.mood == "angry":
            self.all_animations.update({
                "angry_idle": {"cooldown": base_cooldown, "weight": "mood"},
            })


    def animate_speech_bubble(self):
        # get the right file for the current mood
        image = "sprites/" + "speech_bubbles/" + self.mood + ".png"

        frames = 5 # amount of speech bubble sprites
        if self.speech_bubble_frame >= frames: # reset to avoid value error with rect
            self.speech_bubble_frame = 0 # reset to avoid value error with rect

        # create rect change x cord when frame moves on the next number
        rect = pygame.Rect(0 + 64 * math.floor(self.speech_bubble_frame), 0, 64, 64)

        # load the image
        load_image = pygame.image.load(image)

        # send it to the draw function
        return load_image.subsurface(rect)


    def draw_speech_bubble(self):
        # it is here as this function runs constantly
        self.speech_bubble_frame += 0.13

        # speech bubble to represent the current mood
        image = self.animate_speech_bubble()
        image_size = 64

        # position it to the pet's right
        if self.direction == "right":
            x = self.x + image_size

            # makes sure it does not go offscreen (go to the opposite side)
            if x + image_size > self.display_width:
                x = self.x - 64
                image = pygame.transform.flip(image, True, False)

        else:
            # position it to the pet's left and flip it
            x = self.x - image_size
            image = pygame.transform.flip(image, True, False)

            # same thing here
            if x < 0:
                x = self.x + 64
                image = pygame.transform.flip(image, True, False)

        # position it above the pet's head
        y = self.y - 48

        # print on screen
        self.window.blit(image, (x, y))

    # chance to change mood to happy when petting
    def uplift_when_pet(self):
        moods = ["happy", self.mood] # turn happy or keep the same mood
        weight = [0.01, 0.99] # low chance for happy to stimulate putting in effort
        mood = random.choices(moods, k=1, weights=weight)[0] # pick a random mood

        if mood == "happy" and self.mood != "happy":
            self.no_pet_time = 0 # pet has been petted
            self.update_mood() # update the mood and mood animations
            self.cooldown = 0 # peform an animation
        else:
            pass

        self.current_animation = self.mood + "_idle"  # set animation to the mood-unique idle animation

    # im thinking of making this a separate class
    def mouse_interaction(self):
        # get the mouse x and y position on the screen
        cursor_position = pygame.mouse.get_pos()

        # create a collision point box with the pet's location and sprite size
        rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # follow the cursor if right click
        if self.mouse_action == "follow":
            self.follow = True  # toggle following
            threading.Thread(daemon=True,
                             target=self.get_mouse_position).start()  # get the cursor location on the background

        # check if the cursor is within the sprite's image
        if rect.collidepoint(cursor_position):
            self.draw_speech_bubble() # display speech bubble when just hovering over

            # if angry walk away
            if self.mood == "angry":
                self.current_animation = "walk"


            # if a mouse button is being clicked
            if self.mouse_action:
                # reposition the pet using the mouse
                if self.mouse_action == "grab":

                    if self.mood == "angry":
                        self.mouse_action = "cancel"
                    else:
                        off_set = self.width // 2 # go to the sprite's middle
                        self.x = cursor_position[0] - off_set # clamps the sprite to the mouse

                # call function to pet and low chance to make happy
                elif self.mouse_action == "pet":
                    self.uplift_when_pet()



                pygame.mouse.set_visible(False)  # make cursor invisible
                self.cursor(self.mouse_action)  # change cursor sprite based on the action

        else:
            self.no_pet_time += 0.1

    def get_mouse_position(self):
        while True:
            self.mouse = pyautogui.position()

    def following(self):

        if self.follow:

            cursor_position = self.mouse

            dist = math.hypot(self.x - cursor_position[0])

            if dist <= 100:
                self.current_animation = f"{self.mood}_idle"
            else:


                if cursor_position[0] > self.x:
                    self.direction = "right"
                    self.current_animation = "walk"

                else:
                    self.direction = "left"
                    self.current_animation = "walk"



    def cursor(self, form):
        cursor_position = pygame.mouse.get_pos() # grab the cursors position
        center = 8 # go to the cursor's middle
        distance_to_head = 32 # go to sprite's head for grab

        # custom cursor sprites and their positions
        cursors = {
            "grab":
                {"image":pygame.image.load("Sprites/cursor/Win95DefGrab.png"),
                 "location": (cursor_position[0] - center, cursor_position[1] - distance_to_head)
                    },
            "pet": {
                "image":pygame.image.load("Sprites/cursor/Win95DefPalm.png"),
                "location": (cursor_position[0] - center, cursor_position[1])
                    },
            "cancel": {
                "image": pygame.image.load("Sprites/cursor/Win95Cancel.png"),
                "location": (cursor_position[0] - center, cursor_position[1])
            },
            "follow": {
                "image": pygame.image.load("Sprites/cursor/Win95DefHand.png"),
                "location": (cursor_position[0] - center, cursor_position[1])
            },
        }
         # print the custom cursor sprite at the right position
        self.window.blit(cursors[form]["image"], cursors[form]["location"]) # print it on the window


    # handle actions that require movement
    def moving_actions(self):
        # move when animation is mobile
        if self.current_animation in ["walk"]:
            # move left
            if self.direction == "left":
                self.x -= 1
            # move right
            if self.direction == "right":
                self.x += 1



    # handle animation frames
    def player_animations(self):
        sprite_iterate_speed = 0.13

        # increase to go to the next frame
        self.frame += sprite_iterate_speed

        # reset if no more frames
        if self.frame >= len(self.sprite_dict[self.current_animation][self.direction]): self.frame = 0



    def get_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    # everything that's in here gets called continuously which i didn't realize at first.
    def draw_self(self):
        self.get_rect()

        if self.mood_change:
            self.draw_speech_bubble()


        self.meow()
        self.borders()
        self.random_action()
        self.following()

        self.moving_actions()
        self.player_animations()

        # print sprite image from the dictionary based on the current animation it is on and the direction it is facing,
        sprite = self.sprite_dict[self.current_animation][self.direction][
            math.floor(self.frame)]  # as well as indexing the right animation frame
        self.window.blit(sprite, (self.x, self.y))
        self.mouse_interaction()





