import random
import math
import os

import pygame.mouse
from datetime import datetime

from sprites_config import cats_dictionary

class Pet:
    def __init__(self, window, color_variant, size, spawn_coordinates, speed, frame):
        self.window = window
        self.sprites = cats_dictionary[color_variant]
        self.x, self.y = spawn_coordinates
        self.floor = spawn_coordinates[1]
        self.speed = speed
        self.direction = None
        self.frame = frame
        self.cooldown = 0
        self.current_animation = None
        self.mood = None
        self.no_pet_time = 0
        self.meow_cooldown = 0
        self.mood_change = False
        self.speech_bubble_frame = 0
        self.follow = False
        self.grab = False
        self.rect = None
        self.toggle_speech_bubble = True
        self.display_mood = False

        self.size = size
        self.width, self.height = self.size[0], self.size[0]



        # dict used to get a random animation it holds all the animations  and the extra info that belongs to each
        self.all_animations = None


    def sound(self,path):
        # play sound every 60 ticks
            sound = pygame.mixer.Sound(path)
            pygame.mixer.Sound.play(sound)
            return





    # function for sounds
    def meow(self):

        moods = ["play", "don't play"]  # options
        weight = [0.001, 0.999]  # low chance to play sound
        mood = random.choices(moods, k=1, weights=weight)[0]  # pick a random option

        if mood == "play" and self.mood != "sleep":
            folder = "sounds"
            random_sound = random.choice(os.listdir(folder))
            path = os.path.join(folder, random_sound)
            sound = pygame.mixer.Sound(path)
            pygame.mixer.Sound.play(sound)


    # stay inside window
    def borders(self, display_width):

        # this could be increased in the future to make the pet bounce back which could be funny
        bounce_back = 1

        # stop moving when touching right border
        if self.x >= display_width - self.width: # minus sprite width for the right collision point
            self.x =  display_width - (self.width + bounce_back) # bounce back
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
            except (KeyError, FileNotFoundError):
                pass



            self.cooldown = 0 # reset cooldown

        self.cooldown += 0.1





    # initialize different dictionaries depending on the mood

    def update_mood(self):
        turn_angry = 100
        turn_sad = 150
        sleepy_time = (20, 7)

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
        # if self.mood_change:
        #     Pet.sound(f"sounds/{self.mood}_sound.mp3")

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
        image_size = 64


        frames = 5 # amount of speech bubble sprites
        if self.speech_bubble_frame >= frames: # reset to avoid value error with rect
            self.speech_bubble_frame = 0 # reset to avoid value error with rect

        # create rect change x cord when frame moves on the next number
        rect = pygame.Rect(0 + image_size * math.floor(self.speech_bubble_frame), 0, image_size, image_size)

        # load the image
        load_image = pygame.image.load(image)

        # send it to the draw function
        return load_image.subsurface(rect)


    def draw_speech_bubble(self, display_width):
        if not self.toggle_speech_bubble:
            return

        # it is here as this function runs constantly
        self.speech_bubble_frame += 0.2

        # speech bubble to represent the current mood
        image = self.animate_speech_bubble()
        image_size = 64

        # position it to the pet's right
        if self.direction == "right":
            x = self.x + self.width

            # makes sure it does not go offscreen (go to the opposite side)
            if x + image_size > display_width:
                x = self.x - image_size
                image = pygame.transform.flip(image, True, False)

        else:
            # position it to the pet's left and flip it
            x = self.x - image_size
            image = pygame.transform.flip(image, True, False)

            # same thing here
            if x < 0:
                x = self.x + image_size
                image = pygame.transform.flip(image, True, False)

        # position it above the pet's head
        y = self.y - (image_size - 12)

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

    # handle actions that require movement
    def moving_actions(self):
        # move when animation is mobile
        if self.current_animation in ["walk"]:
            # move left
            if self.direction == "left":
                self.x -= 1 * self.speed
            # move right
            if self.direction == "right":
                self.x += 1 * self.speed



    # handle animation frames
    def player_animations(self):
        sprite_iterate_speed = 0.2

        # increase to go to the next frame
        self.frame += sprite_iterate_speed

        # reset if no more frames
        if self.frame >= len(self.sprites[self.current_animation][self.direction]): self.frame = 0



    def get_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    @staticmethod
    def detect_collision(cats):
        # detect collisions (pure brain muscles this one lol)
        for cat_index, cat in enumerate(cats):  # go through each cat
            for other_cat_index, other in enumerate(cats):  # go through all cats per cat
                if cat_index == other_cat_index:  # skip itself
                    pass
                else:
                    # make the cat be able to pass
                    if cat.current_animation == "walk" and cat.rect.collidepoint((other.x, other.y)):
                        pass


                    elif cat.rect.collidepoint((other.x, other.y)) and not other.current_animation == "walk":
                        cat.x = cat.x - 5

    def fall(self):
        if self.y < self.floor: # fall if higher than floor
            self.y += 5
        else:
            self.y = self.floor # stop pet from going under the taskbar












    # everything that's in here gets called continuously which i didn't realize at first.
    def draw_self(self, display_width):

        self.get_rect() # for collision
        self.fall()

        # show mood if mood changes
        if self.mood_change:
            self.draw_speech_bubble(display_width) # to show the mood speech bubble


        self.meow() # to make sound


        self.borders(display_width) # to stop at the screen's x borders
        self.random_action() # to perform a random action

        self.moving_actions() # to move when the animation is mobile
        self.player_animations() # to animate the animations

        # print sprite image from the dictionary based on the current animation it is on and the direction it is facing,
        sprite = self.sprites[self.current_animation][self.direction][
            math.floor(self.frame)]  # as well as indexing the right animation frame

        sprite_small = pygame.transform.scale(sprite, self.size)
        self.window.blit(sprite_small, (self.x, self.y))





