import os
import pygame
import time
import pickle           # Load/Save Game
import random
import pygame.locals as pl
import os.path
import sys

pygame.init()
FPS = 60
clock = pygame.time.Clock()

# Title
Project_Title = "Serenity Dawn"
pygame.display.set_caption(Project_Title)

# Screen Size
Screen_Size = display_width, display_height = 1280, 720
gameDisplay = pygame.display.set_mode((display_width, display_height))

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)


# Miscellaneous
def file_len(file):
    with open(file) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def load_file(path, image=False):
    """
    Load    : All texts/images in directory. The directory must only contain texts/images.
    Path    : The relative or absolute path to the directory to load texts/images from.
    Image   : Load and convert image in the direcoty path.
    Return  : List of files.
    """
    file = []
    for file_name in os.listdir(path):
        if image == False:
            file.append(path + os.sep + file_name)
        if image == True:
            file.append(pygame.image.load(path + os.sep + file_name).convert())
    return file

    
# Gallery Music
def Music_Play(Selection):
    pygame.mixer.music.load(Selection)
    pygame.mixer.music.play(-1)

# Text
def Text_Title_Screen():
    font = pygame.font.Font("freesansbold.ttf",  100)
    color = Color_Title_Screen
    return font, color

def Text_Button():
    font = pygame.font.Font("freesansbold.ttf",  40)
    color = Color_Blue
    return font, color

def Text_Interface():
    font = pygame.font.Font("freesansbold.ttf",  35)
    color = Color_Black
    return font, color


"""
Copyright 2017, Silas Gyger, silasgyger@gmail.com, All rights reserved.
"""


class TextInput:
    """
    This class lets the user input a piece of text, e.g. a name or a message.

    This class let's the user input a short, one-lines piece of text at a blinking cursor
    that can be moved using the arrow-keys. Delete, home and end work as well.
    """
    def __init__(self,  initial_string="",
                        font_family = "",
                        font_size = 35,
                        antialias=True,
                        text_color=(0, 0, 0),
                        cursor_color=(0, 0, 1),
                        repeat_keys_initial_ms=400,
                        repeat_keys_interval_ms=35):
        """
        Args:
            initial_input: Initial input text value. Default is empty string
            font_family: Name or path of the font that should be used. Default is pygame-font
            font_size: Size of the font in pixels
            antialias: (bool) Determines if antialias is used on fonts or not
            text_color: Color of the text
            cursor_color: Color of the cursor
            repeat_keys_initial_ms: ms until the keydowns get repeated when a key is not released
            repeat_keys_interval_ms: ms between to keydown-repeats if key is not released
        """

        # Text related vars:
        self.antialias = antialias
        self.text_color = text_color
        self.font_size = font_size
        self.input_string = initial_string # Inputted text
        if not os.path.isfile(font_family): font_family = pygame.font.match_font(font_family)
        self.font_object = pygame.font.Font(font_family, font_size)

        # Text-surface will be created during the first update call:
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {} # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size/20+1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(initial_string)  # Inside text
        self.cursor_visible = True # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500 # /|\
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.cursor_visible = True # So the user sees where he writes

                # If none exist, create counter for that key:
                if not event.key in self.keyrepeat_counters:
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pl.K_BACKSPACE: # FIXME: Delete at beginning of line?
                    self.input_string = self.input_string[:max(self.cursor_position - 1, 0)] + \
                                        self.input_string[self.cursor_position:]

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == pl.K_DELETE:
                    self.input_string = self.input_string[:self.cursor_position] + \
                                        self.input_string[self.cursor_position + 1:]

                elif event.key == pl.K_RETURN:
                    return True

                elif event.key == pl.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                elif event.key == pl.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pl.K_END:
                    self.cursor_position = len(self.input_string)

                elif event.key == pl.K_HOME:
                    self.cursor_position = 0

                else:
                    # If no special key is pressed, add unicode of key to input_string
                    self.input_string = self.input_string[:self.cursor_position] + \
                                        event.unicode + \
                                        self.input_string[self.cursor_position:]
                    self.cursor_position += len(event.unicode) # Some are empty, e.g. K_UP

            elif event.type == pl.KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

        # Update key counters:
        for key in self.keyrepeat_counters :
            self.keyrepeat_counters[key][0] += self.clock.get_time() # Update clock
            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = self.keyrepeat_intial_interval_ms - \
                                                    self.keyrepeat_interval_ms

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pygame.event.post(pygame.event.Event(pl.KEYDOWN, key=event_key, unicode=event_unicode))

        # Rerender text surface:
        self.surface = self.font_object.render(self.input_string, self.antialias, self.text_color)

        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            cursor_y_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if self.cursor_position > 0:
                cursor_y_pos -= self.cursor_surface.get_width()
            self.surface.blit(self.cursor_surface, (cursor_y_pos, 0))

        self.clock.tick()
        return False

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self.input_string=""
        self.cursor_position=0
        
     

# Colors
Color_Red           = 255, 20,  0
Color_Green         = 60,  210, 120
Color_Blue          = 0,   160, 230
Color_Black         = 0,   0,   0
Color_Grey          = 150, 170, 210
Color_White         = 255, 255, 255

Color_Button        = 140, 205, 245
Color_Title_Screen  = 210, 100, 240
    
# Backgrounds
Background_Title_Screen_1   = pygame.image.load("Data\Background\Background_Title_Screen_1.png")
Background_Title_Screen_2   = pygame.image.load("Data\Background\Background_Title_Screen_2.png")
Background_Prologue_1       = pygame.image.load("Data\Background\Background_Altar.png")
Background_Prologue_2       = pygame.image.load("Data\Background\Background_House.png")



# UIs
Interface_Main_Menu         = pygame.image.load("Data\Interface\Interface_Main_Menu.png")
Interface_Cutscene          = pygame.image.load("Data\Interface\Interface_Cutscene.png")
Interface_Fight             = pygame.image.load("Data\Interface\Interface_Fight.png")
Interface_Inventory         = pygame.image.load("Data\Interface\Interface_Inventory.png")
Interface_Result            = pygame.image.load("Data\Interface\Interface_Result.png")



# Icons
Icon_Ellesia        = pygame.image.load("Data\Icon\Icon_Ellesia.png")
Icon_Status_Ellesia = pygame.image.load("Data\Icon\Icon_Status_Ellesia.png")
Icon_Iris           = pygame.image.load("Data\Icon\Icon_Iris.png")
Icon_Status_Iris    = pygame.image.load("Data\Icon\Icon_Status_Iris.png")
Icon_Gyrei          = pygame.image.load("Data\Icon\Icon_Gyrei.png")
Icon_Status_Gyrei   = pygame.image.load("Data\Icon\Icon_Status_Gyrei.png")

Icon_Direwolf       = pygame.image.load("Data\Icon\Icon_Direwolf.png")
Icon_Ghoul          = pygame.image.load("Data\Icon\Icon_Ghoul.png")
Icon_Shadow_Red     = pygame.image.load("Data\Icon\Icon_Shadow_Red.png")
Icon_Shadow_Blue    = pygame.image.load("Data\Icon\Icon_Shadow_Blue.png")
Icon_Wolf           = pygame.image.load("Data\Icon\Icon_Wolf.png")
Icon_Zombie         = pygame.image.load("Data\Icon\Icon_Zombie.png")

Icon_World_Map_ac   = pygame.image.load("Data\Icon\Icon_World_Map_ac.png")
Icon_World_Map_ic   = pygame.image.load("Data\Icon\Icon_World_Map_ic.png")
Icon_Exit           = pygame.image.load("Data\Icon\Icon_Exit.png")

Icon_Arrow_A = pygame.image.load("Data\Icon\Icon_Arrow_A.png")
Icon_Arrow_B = pygame.image.load("Data\Icon\Icon_Arrow_B.png")
Arrow_A_Rect = Icon_Arrow_A.get_rect()
Arrow_B_Rect = Icon_Arrow_B.get_rect()



# Sprites
Sprite_Ellesia      = pygame.image.load("Data\Sprite\Sprite_Ellesia.png")
Sprite_Iris         = pygame.image.load("Data\Sprite\Sprite_Iris.png")
Sprite_Gyrei        = pygame.image.load("Data\Sprite\Sprite_Gyrei.png")

Sprite_Direwolf     = pygame.image.load("Data\Sprite\Sprite_Direwolf.png")
Sprite_Ghoul        = pygame.image.load("Data\Sprite\Sprite_Ghoul.png")
Sprite_Shadow_Red   = pygame.image.load("Data\Sprite\Sprite_Shadow_Red.png")
Sprite_Shadow_Blue  = pygame.image.load("Data\Sprite\Sprite_Shadow_Blue.png")
Sprite_Zombie       = pygame.image.load("Data\Sprite\Sprite_Zombie.png")
Sprite_Wolf         = pygame.image.load("Data\Sprite\Sprite_Wolf.png")



# Sound Effects
List_SFX = load_file("Data/SFX")

SFX_Bow, SFX_Hit, SFX_Metal, SFX_Slash, SFX_Stab = [], [], [], [], []
[SFX_Bow.append(SFX)    for SFX in List_SFX if "Bow"    in SFX]
[SFX_Hit.append(SFX)    for SFX in List_SFX if "Hit"    in SFX]
[SFX_Metal.append(SFX)  for SFX in List_SFX if "Metal"  in SFX]
[SFX_Slash.append(SFX)  for SFX in List_SFX if "Slash"  in SFX]
[SFX_Stab.append(SFX)   for SFX in List_SFX if "Stab"   in SFX]

SFX_Battle_Bow_battle16	         = pygame.mixer.Sound("Data\SFX\Battle_Bow_battle16.wav")
SFX_Battle_Bow_battle18	         = pygame.mixer.Sound("Data\SFX\Battle_Bow_battle18.wav")
SFX_Battle_Hit_battle06	         = pygame.mixer.Sound("Data\SFX\Battle_Hit_battle06.wav")
SFX_Battle_Hit_battle12	         = pygame.mixer.Sound("Data\SFX\Battle_Hit_battle12.wav")
SFX_Battle_Metal_battle05	 = pygame.mixer.Sound("Data\SFX\Battle_Metal_battle05.wav")
SFX_Battle_Metal_battle10	 = pygame.mixer.Sound("Data\SFX\Battle_Metal_battle10.wav")
SFX_Battle_Slash_battle17	 = pygame.mixer.Sound("Data\SFX\Battle_Slash_battle17.wav")
SFX_Battle_Stab_battle01	 = pygame.mixer.Sound("Data\SFX\Battle_Stab_battle01.wav")
SFX_Battle_Stab_battle03	 = pygame.mixer.Sound("Data\SFX\Battle_Stab_battle03.wav")

SFX_Battle_Debuff_system04       = pygame.mixer.Sound("Data\SFX\Battle_Debuff_system04.wav")
SFX_Battle_Debuff_system09	 = pygame.mixer.Sound("Data\SFX\Battle_Debuff_system09.wav")
SFX_Battle_Fire_element_fire01	 = pygame.mixer.Sound("Data\SFX\Battle_Fire_element_fire01.wav")
SFX_Battle_Fire_explosion06	 = pygame.mixer.Sound("Data\SFX\Battle_Fire_explosion06.wav")
SFX_Battle_Heal_magical25	 = pygame.mixer.Sound("Data\SFX\Battle_Heal_magical25.wav")
SFX_Battle_Water_element_water06 = pygame.mixer.Sound("Data\SFX\Battle_Water_element_water06.wav")
SFX_Battle_Water_element_water08 = pygame.mixer.Sound("Data\SFX\Battle_Water_element_water08.wav")
SFX_Battle_Water_element_water14 = pygame.mixer.Sound("Data\SFX\Battle_Water_element_water14.wav")
SFX_Battle_Wind_magical16	 = pygame.mixer.Sound("Data\SFX\Battle_Wind_magical16.wav")

SFX_Battle_Defeated_battle02	 = pygame.mixer.Sound("Data\SFX\Battle_Defeated_battle02.wav")
SFX_Battle_Escape_battle19	 = pygame.mixer.Sound("Data\SFX\Battle_Escape_battle19.wav")
SFX_Battle_Miss_battle14	 = pygame.mixer.Sound("Data\SFX\Battle_Miss_battle14.wav")

SFX_Event_Bell_chime07	         = pygame.mixer.Sound("Data\SFX\Event_Bell_chime07.wav")
SFX_Event_Bell_chime08	         = pygame.mixer.Sound("Data\SFX\Event_Bell_chime08.wav")
SFX_Event_Bell_chime09	         = pygame.mixer.Sound("Data\SFX\Event_Bell_chime09.wav")
SFX_Event_Creepy_effect07	 = pygame.mixer.Sound("Data\SFX\Event_Creepy_effect07.wav")
SFX_Event_Creepy_effect12	 = pygame.mixer.Sound("Data\SFX\Event_Creepy_effect12.wav")
SFX_Event_Creepy_effect13	 = pygame.mixer.Sound("Data\SFX\Event_Creepy_effect13.wav")
SFX_Event_Creepy_magical13	 = pygame.mixer.Sound("Data\SFX\Event_Creepy_magical13.wav")
SFX_Event_Creepy_magical14	 = pygame.mixer.Sound("Data\SFX\Event_Creepy_magical14.wav")
SFX_Event_Future_effect04	 = pygame.mixer.Sound("Data\SFX\Event_Future_effect04.wav")
SFX_Event_se_door01	         = pygame.mixer.Sound("Data\SFX\Event_se_door01.wav")
SFX_Event_se_door05	         = pygame.mixer.Sound("Data\SFX\Event_se_door05.wav")
SFX_Event_se_footstep01	         = pygame.mixer.Sound("Data\SFX\Event_se_footstep01.wav")
SFX_Event_se_footstep02	         = pygame.mixer.Sound("Data\SFX\Event_se_footstep02.wav")
SFX_Event_se_stairs	         = pygame.mixer.Sound("Data\SFX\Event_se_stairs.wav")
SFX_Event_Summon_magical10	 = pygame.mixer.Sound("Data\SFX\Event_Summon_magical10.wav")
SFX_Map_element_fire12	         = pygame.mixer.Sound("Data\SFX\Map_element_fire12.wav")
SFX_Map_element_thunder01	 = pygame.mixer.Sound("Data\SFX\Map_element_thunder01.wav")
SFX_Map_element_wind03	         = pygame.mixer.Sound("Data\SFX\Map_element_wind03.wav")
SFX_Map_se_car02	         = pygame.mixer.Sound("Data\SFX\Map_se_car02.wav")
SFX_Map_se_car04	         = pygame.mixer.Sound("Data\SFX\Map_se_car04.wav")
SFX_Map_se_car07	         = pygame.mixer.Sound("Data\SFX\Map_se_car07.wav")
SFX_Map_se_vehicle02	         = pygame.mixer.Sound("Data\SFX\Map_se_vehicle02.wav")
SFX_System_Cancel_system10	 = pygame.mixer.Sound("Data\SFX\System_Cancel_system10.wav")
SFX_System_Cancel_system42	 = pygame.mixer.Sound("Data\SFX\System_Cancel_system42.wav")
SFX_System_Cancel_system43	 = pygame.mixer.Sound("Data\SFX\System_Cancel_system43.wav")
SFX_System_Complete_jingle05	 = pygame.mixer.Sound("Data\SFX\System_Complete_jingle05.wav")
SFX_System_Confirm_system23	 = pygame.mixer.Sound("Data\SFX\System_Confirm_system23.wav")
SFX_System_Confirm_system46	 = pygame.mixer.Sound("Data\SFX\System_Confirm_system46.wav")
SFX_System_Error_onepoint14	 = pygame.mixer.Sound("Data\SFX\System_Error_onepoint14.wav")
SFX_System_Game_Over_jingle01	 = pygame.mixer.Sound("Data\SFX\System_Game_Over_jingle01.wav")
SFX_System_Hint_onepoint09	 = pygame.mixer.Sound("Data\SFX\System_Hint_onepoint09.wav")
SFX_System_Hint_onepoint12	 = pygame.mixer.Sound("Data\SFX\System_Hint_onepoint12.wav")
SFX_System_Hint_onepoint16	 = pygame.mixer.Sound("Data\SFX\System_Hint_onepoint16.wav")
SFX_System_Navigation_system48	 = pygame.mixer.Sound("Data\SFX\System_Navigation_system48.wav")
SFX_System_Navigationse_sound15	 = pygame.mixer.Sound("Data\SFX\System_Navigationse_sound15.wav")
SFX_System_Story_End_jingle02	 = pygame.mixer.Sound("Data\SFX\System_Story_End_jingle02.wav")
SFX_System_Tutorial_onepoint10	 = pygame.mixer.Sound("Data\SFX\System_Tutorial_onepoint10.wav")
SFX_Voice_element_darkness01	 = pygame.mixer.Sound("Data\SFX\Voice_element_darkness01.wav")
SFX_Voice_element_darkness02	 = pygame.mixer.Sound("Data\SFX\Voice_element_darkness02.wav")
SFX_Voice_element_darkness03	 = pygame.mixer.Sound("Data\SFX\Voice_element_darkness03.wav")
SFX_Voice_element_darkness04	 = pygame.mixer.Sound("Data\SFX\Voice_element_darkness04.wav")
SFX_Voice_voice_human01          = pygame.mixer.Sound("Data\SFX\Voice_voice_human01.wav")
SFX_Voice_voice_monster01	 = pygame.mixer.Sound("Data\SFX\Voice_voice_monster01.wav")
SFX_Voice_voice_monster02	 = pygame.mixer.Sound("Data\SFX\Voice_voice_monster02.wav")
SFX_Voice_voice_monster03	 = pygame.mixer.Sound("Data\SFX\Voice_voice_monster03.wav")
SFX_Voice_voice_tiger01	         = pygame.mixer.Sound("Data\SFX\Voice_voice_tiger01.wav")


# BGM
List_BGM = load_file("Data/BGM")

BGM_Event_0_1_1 = "Data/BGM/Event_0_1_1_Serenity.mp3"
BGM_Event_0_1_2 = "Data/BGM/Event_0_1_2_Around_a_Campfire.mp3"
BGM_Event_1_1   = "Data/BGM/Event_1_1_Exploring_the_Danger.mp3"
BGM_Event_1_2_1 = "Data/BGM/Event_1_2_1_Time_of_Crisis.mp3"
BGM_Event_1_2_2 = "Data/BGM/Event_1_2_2_Time_of_Crisis_Piano.mp3"
BGM_Event_1_3   = "Data/BGM/Event_1_3_Danger_to_our_Lives.mp3"
BGM_Event_1_4   = "Data/BGM/Event_1_4_Behind_the_Curtains.mp3"
BGM_Event_1_5   = "Data/BGM/Event_1_5_Departure.mp3"

BGM_Fight_0_1   = "Data/BGM/Fight_0_1_Fierce_Assault.mp3"
BGM_Fight_1_1   = "Data/BGM/Fight_1_1_Ruler_of_the_Hills.mp3"
BGM_Fight_1_2   = "Data/BGM/Fight_1_2_Desperate_Situation.mp3"
BGM_Fight_1_3   = "Data/BGM/Fight_1_3_Facing_the_Danger.mp3"
BGM_Fight_1_4   = "Data/BGM/Fight_1_4_Intimidating_Foe.mp3"

BGM_Menu_1      = "Data/BGM/Menu_1_The_Soul_of_the_Adventurer.mp3"
BGM_Menu_2      = "Data/BGM/Menu_2_Calm_Before_the_Storm.mp3"
BGM_Shop        = "Data/BGM/Shop_Shopping_in_Town.mp3"
BGM_Title_Screen = "Data/BGM/Title_Screen_Undisturbed_Place.mp3"
BGM_Victory_1   = "Data/BGM/Victory_1_Resting_Around_the_Campfire.mp3"
BGM_Victory_2   = "Data/BGM/Victory_2_Glory_Ride.mp3"




        # Player
class Player:
    def __init__(self, name, level=1):
        self.name           = name
        self.Icon           = Icon_Ellesia
        self.Icon_Status    = Icon_Status_Ellesia
        self.Sprite         = Sprite_Ellesia
        self.SFX_Attack     = SFX_Stab
        self.Action_Point   = 0
        self.Gold           = 0
        
        self.Class          = "Lancer"
        self.level          = level
        self.Experience     = 0

        self.update_level()

    def update_level(self):
        while self.Experience >= 100:
            self.level += 1
            self.Experience -= 100
        
        self.Maxhealth      = 40    + 8.0 * (self.level-1)
        self.Strength       = 8     + 1.1 * (self.level-1)
        self.speed          = 10    + 1.2 * (self.level-1)
        self.Defense        = 4     + 1.3 * (self.level-1)
        self.Health         = self.Maxhealth
        
        self.Magic          = 0
        self.Resistance     = 0
        

PlayerIG = Player("NightFore")



class Iris:
    def __init__(self, name, level=1):
        self.name           = name
        self.Icon           = Icon_Iris
        self.Icon_Status    = Icon_Status_Iris
        self.Sprite         = Sprite_Iris
        self.SFX_Attack     = SFX_Bow
        self.Action_Point   = 0
        
        self.Class          = "Archer"
        self.level          = level
        self.Experience     = 0

        self.update_level()

    def update_level(self):
        while self.Experience >= 100:
            self.level += 1
            self.Experience -= 100
        
        self.Maxhealth      = 26    + 5.0 * (self.level-1)
        self.Strength       = 9     + 1.4 * (self.level-1)
        self.speed          = 8     + 0.9 * (self.level-1)
        self.Defense        = 1     + 0.7 * (self.level-1)
        self.Health         = self.Maxhealth
        
        self.Magic          = 0
        self.Resistance     = 0
IrisIG = Iris("Iris")



class Gyrei:
    def __init__(self, name, level=1):
        self.name           = name
        self.Icon           = Icon_Gyrei
        self.Icon_Status    = Icon_Status_Gyrei
        self.Sprite         = Sprite_Gyrei
        self.SFX_Attack     = SFX_Slash
        self.Action_Point   = 0
        
        self.Class          = "Dual Wielder"
        self.level          = level
        self.Experience     = 0

        self.update_level()

    def update_level(self):
        while self.Experience >= 100:
            self.level += 1
            self.Experience -= 100
        
        self.Maxhealth      = 35    + 7.0 * (self.level-1)
        self.Strength       = 6     + 0.8 * (self.level-1)
        self.speed          = 12    + 1.5 * (self.level-1)
        self.Defense        = 2     + 1.0 * (self.level-1)
        self.Health         = self.Maxhealth
        
        self.Magic          = 0
        self.Resistance     = 0
GyreiIG = Gyrei("Gyrei")





        # Enemy
class Wolf:
    def __init__(self, name, level=1):
        self.name           = name
        self.Icon           = Icon_Wolf
        self.Sprite         = Sprite_Wolf
        self.SFX_Attack     = SFX_Hit
        
        self.level      = level
        self.EXP_Gain   = 100
        self.Gold_Gain  = 10
        self.Action_Point = 0
        
        self.Maxhealth  = 1 + 1 * (self.level - 1)
        self.Health     = self.Maxhealth
        self.Strength   = 4 + 1 * (self.level - 1)
        self.Magic      = 0
        self.speed      = 4 + 1 * (self.level - 1)
        self.Defense    = 1 + 0.5 * (self.level - 1)
        self.Resistance = 0 + 0.5 * (self.level - 1)
WolfIG = Wolf("Wolf")


class Direwolf:
    def __init__(self, name, level=1):
        self.name           = name
        self.Icon           = Icon_Direwolf
        self.Sprite         = Sprite_Direwolf
        self.SFX_Attack     = SFX_Hit
        
        self.level          = level
        self.EXP_Gain   = 10
        self.Gold_Gain  = 10
        self.Action_Point = 0
        
        self.Maxhealth  = 40 + 6 * (self.level - 1)
        self.Health     = self.Maxhealth
        self.Strength   = 4 + 1 * (self.level - 1)
        self.Magic      = 0
        self.speed      = 6 + 1 * (self.level - 1)
        self.Defense    = 1 + 0.5 * (self.level - 1)
        self.Resistance = 0 + 0.5 * (self.level - 1)
DirewolfIG = Direwolf("Direwolf")


class Ghoul:
    def __init__(self, name, level=1):
        self.name           = name
        self.Icon           = Icon_Ghoul
        self.Sprite         = Sprite_Ghoul
        self.SFX_Attack     = SFX_Hit

        self.level          = level
        self.EXP_Gain   = 10
        self.Gold_Gain  = 10
        self.Action_Point = 0
        
        self.Maxhealth  = 40 + 6 * (self.level - 1)
        self.Health     = self.Maxhealth
        self.Strength   = 4 + 1 * (self.level - 1)
        self.Magic      = 0
        self.speed      = 3 + 1 * (self.level - 1)
        self.Defense    = 1 + 0.5 * (self.level - 1)
        self.Resistance = 0 + 0.5 * (self.level - 1)
GhoulIG = Ghoul("Ghoul")


class Zombie:
    def __init__(self, name, level=1):
        self.name           = name
        self.Icon           = Icon_Zombie
        self.Sprite         = Sprite_Zombie
        self.SFX_Attack     = SFX_Hit

        self.level          = level
        self.EXP_Gain   = 10
        self.Gold_Gain  = 10
        self.Action_Point = 0

        self.Maxhealth  = 40 + 6 * (self.level - 1)
        self.Health     = self.Maxhealth
        self.Strength   = 4 + 1 * (self.level - 1)
        self.Magic      = 0
        self.speed      = 3 + 1 * (self.level - 1)
        self.Defense    = 1 + 0.5 * (self.level - 1)
        self.Resistance = 0 + 0.5 * (self.level - 1)
ZombieIG = Zombie("Zombie")


class Shadow_Red:
    def __init__(self, name, level=1):
        self.name           = name
        self.Icon           = Icon_Shadow_Red
        self.Sprite         = Sprite_Shadow_Red
        self.SFX_Attack     = SFX_Hit

        self.level          = level
        self.EXP_Gain   = 10
        self.Gold_Gain  = 10
        self.Action_Point = 0
        
        self.Maxhealth  = 40 + 6 * (self.level - 1)
        self.Health     = self.Maxhealth
        self.Strength   = 4 + 1 * (self.level - 1)
        self.Magic      = 0
        self.speed      = 3 + 1 * (self.level - 1)
        self.Defense    = 1 + 0.5 * (self.level - 1)
        self.Resistance = 0 + 0.5 * (self.level - 1)
Shadow_RedIG = Shadow_Red("Shadow_Red")


class Shadow_Blue:
    def __init__(self, name, level=1):
        self.name           = name
        self.Icon           = Icon_Shadow_Blue
        self.Sprite         = Sprite_Shadow_Blue
        self.SFX_Attack     = SFX_Hit

        self.level          = level
        self.EXP_Gain   = 10
        self.Gold_Gain  = 10
        self.Action_Point = 0
        
        self.Maxhealth  = 40 + 6 * (self.level - 1)
        self.Health     = self.Maxhealth
        self.Strength   = 4 + 1 * (self.level - 1)
        self.Magic      = 0
        self.speed      = 3 + 1 * (self.level - 1)
        self.Defense    = 1 + 0.5 * (self.level - 1)
        self.Resistance = 0 + 0.5 * (self.level - 1)
Shadow_BlueIG = Shadow_Blue("Shadow_Blue")


list_enemy = [Wolf, Direwolf, Ghoul, Zombie, Shadow_Red, Shadow_Blue]

class Tools():
    def __init__(self):
        self.event          = ""    # Button
        self.events         = ""    # Text
Tools = Tools()


class Combat():
    def __init__(self):
        # State
        self.Button_Action  = False
        self.Button_Turn    = False
        self.Button_Fight   = []
        self.End_Turn       = False
        
        self.Attack         = False
        self.Skill          = False
        
        self.Turn           = [False,False,False,False,False,False]
        self.Turn_Phase     = ""
        self.Turn_Order     = 0
        
        self.Active_Time    = 0
        self.Action_Point   = [0,0,0,0,0,0]  # All Characters Action_Point
Combat = Combat()


class GameState():
    def __init__(self):
        # Progress
        self.Zone   = 0
        self.Stage  = 0
GameState = GameState()


class Progress():
    def __init__(self):
        self.story = 0
        self.fight = 0
Progress = Progress()


############################################################


class Setup():
    def __init__(self):
        # Background
        self.background = False

        # Music
        self.music = False

        # State
        self.button = False
        self.sprite = False
        self.fight  = False
        self.story  = False
        self.text   = False

        # Interface
        self.inventory  = False
        self.result     = False

        # State Update
        self.list_button        = []
        self.list_button_image  = []
        self.list_sprite        = []    # AnimatedSprite()
        self.all_sprites        = []    # Creates a sprite group and adds 'player' to it.
        self.list_text          = []

    def update_music(self, music):
        """
        Playing Music
        """
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)

    def update_init(self, background=False, music=False, button=False, sprite=False,  fight=False, text=False, story=False):
        """
        Background
        """
        self.background = background

        """
        Playing Music
        """
        self.music = music
        if self.music != False: 
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(-1)
        
        """
        Activate state functions
        """
        # State
        self.button = button
        self.sprite = sprite
        self.fight  = fight
        self.story  = story
        self.text   = text

        # Interface
        self.inventory  = False
        self.status     = None
        
        self.result     = False
        
        """
        Reset all lists when updating states
        """
        self.list_button        = []
        self.list_button_image  = []
        self.list_sprite        = []    # AnimatedSprite()
        self.all_sprites        = []    # Creates a sprite group and adds 'player' to it.
        self.list_text          = []

    def update(self):
        # Tools
        pygame.display.update()
        Tools.events = pygame.event.get()

        if self.background != False:
            gameDisplay.blit(self.background, (0,0))

        for event in Tools.events:
            Tools.event = event

        self.update_state()

    def update_state(self):
        if self.inventory == True:
            self.update_inventory()
        """
        Display interface menu
        """
        # Result
        if self.result == True:
            gameDisplay.blit(Interface_Result, (0, 0))
            
            for index in range(3):
                # Player
                if Fight.slot[index] == True:
                    gameDisplay.blit(Fight.character[index].Icon_Status, (300,70+150*index))

                if Fight.slot[3+index] == True:
                    gameDisplay.blit(Fight.character[3+index].Icon, (660, 115+95*index))
            
        


        """
        Display buttons from the list and check for mouse position.
        Call function action() if clicking on it
        """
        # Button
        if self.button == True:
            # Display Button
            for index in range(len(self.list_button)):
                self.list_button[index].update(index)
            for index in range(len(self.list_button_image)):
                self.list_button_image[index].update(index)

            # Check Mouse Position
            for event in Tools.events:
                for index in range(len(self.list_button)):
                    self.list_button[index].check(index)
                for index in range(len(self.list_button_image)):
                    self.list_button_image[index].check(index)

                

        """
        Display sprites from the list and check for mouse position.
        Call function action() if clicking on it.
        """
        # Sprite
        if self.sprite == True:
            # Display Sprite
            for index in range(len(self.list_sprite)):
                self.list_sprite[index].dt = clock.tick(FPS)
                self.all_sprites[index].update()
                self.all_sprites[index].draw(gameDisplay)

            # Check Mouse Position & Action
            for event in Tools.events:
                for index in range(len(self.list_sprite)):
                    if callable(self.list_sprite[index].action) == True:
                        self.list_sprite[index].button()

                    

        """
        Game_ui_Fight()         : Display background, list_text and list_button from 
        Fight_Action_Point()    : Generates action point for every character and allows them to take turn when reaching 100/100
        Turn_Phase()            : Check if the character taking an action is a player or enemy. If it is an enemy, it will automatically take an action
        Attack_Choice()         : Allows the player to select its target.
        """
        # Fight
        if self.fight == True:
            # Setup
            self.button = True
            self.text = True

            # Update
            Fight.update()



        """
        Display text from the list
        """
        # Text
        if self.text == True:
            for index in range(len(self.list_text)):
                self.list_text[index].display()


         
        """
        Display text being read from a file by the class StoryIG()
        Check for events and triggers to advance through the story
        """
        # Story
        if self.story == True:
            StoryIG.update()

            
    def inventory_init(self):
        if self.inventory == False:
            self.inventory = True
            self.sprite = False
            self.update_status(0)
            
            for index in range(3):
                if Fight.slot[index] == True:
                    Button(Fight.character[index].name, Text_Interface, 340, 180+150*index, 146, 38, 5, True, True, Color_Red, Color_Green, index, self.update_status)
                
        elif self.inventory == True:
            Menu_Zone()
            

    def update_inventory(self):
        gameDisplay.blit(Interface_Inventory, (0, 0))
        for index in range(3):
            if Fight.slot[index] == True:
                gameDisplay.blit(Fight.character[index].Icon_Status, (300,70+150*index))


    def update_status(self, status=None):
        if self.status!=status and status!=None:
            self.status = status
            self.list_text = []
            
            Text("Status",      540, 85, True, Text_Interface)
            Text("Equipment",   760, 85, True, Text_Interface)
            Text("Inventory",   960, 85, True, Text_Interface)
            
            Text(("Class : %s"      % Fight.character[status].Class),       450, 120, False, Text_Interface)
            Text(("Level : %i"      % Fight.character[status].level),       450, 150, False, Text_Interface)
            Text(("EXP : %i/100"    % Fight.character[status].Experience),  450, 180, False, Text_Interface)
            
            Text(("Health : %i"     % Fight.character[status].Maxhealth),   450, 220, False, Text_Interface)
            Text(("Strength : %i"   % Fight.character[status].Strength),    450, 250, False, Text_Interface)
            Text(("Magic : %i"      % Fight.character[status].Magic),       450, 280, False, Text_Interface)
            Text(("Speed : %i"      % Fight.character[status].speed),       450, 310, False, Text_Interface)
            Text(("Defense : %i"    % Fight.character[status].Defense),     450, 340, False, Text_Interface)
            Text(("Resistance : %i" % Fight.character[status].Resistance),  450, 370, False, Text_Interface)

############################################################ WIP
            Text(("Accuracy : %i"   % Fight.character[status].Resistance),  450, 410, False, Text_Interface)
            Text(("Evasion : %i"    % Fight.character[status].Resistance),  450, 440, False, Text_Interface)
            Text(("Critical : %i"   % Fight.character[status].Resistance),  450, 470, False, Text_Interface)
        
Setup = Setup()



class Text():
    def __init__(self, text, x, y, center, font):
        # Tools
        Setup.list_text.append(self)

        # Text
        self.text = text
        self.font = font
        self.font_type, self.color = self.font()

        # Position
        self.x = x
        self.y = y
        self.center = center

        # Surface
        self.textSurface = self.font_type.render(self.text, True, self.color)

        # Center Text
        if center == False:
            self.textRect = (self.x, self.y)
            
        if center == True:
            self.textRect = self.textSurface.get_rect()
            self.textRect.center = (self.x, self.y)
    
    # Display
    def display(self):
        gameDisplay.blit(self.textSurface, self.textRect)



class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, center, path, dt, animation, action):
        """
        Animated sprite object.

        Args:
            position: x, y coordinate on the screen to place the AnimatedSprite.
            images: Images to use in the animation.
        """
        super(AnimatedSprite, self).__init__()

        # Tools
        Setup.list_sprite.append(self)
        Setup.all_sprites.append(pygame.sprite.Group(self))
        
        # Position
        self.x = x
        self.y = y
        self.center = center

        # Load Images
        self.path = path
        self.images = load_file(self.path, image=True)                                          # Load all images in the directory
        self.images_right = self.images                                                         # Normal image
        self.image_left = [pygame.transform.flip(image, True, False) for image in self.images]  # Flipping image.

        # Image
        self.index = 0                          # Current index
        self.image = self.images[self.index]    # Current image

        # Center Position
        if self.center == False:
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

        if self.center == True:
            self.rect = self.image.get_rect(center=(self.x, self.y))

        # Update
        self.dt = dt
            #self.animation_time    = 0.1
        self.animation_time     = animation     # Time before sprite update
        self.current_time       = 0

            #self.animation_frames  = 6
        self.animation_frames   = animation     # Frame before sprite update
        self.current_frame      = 0

        # Action
        self.action = action
        
    def button(self):
        """
        Calls the function Selection when clicking oh the image
        """
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            if Tools.event.type == pygame.MOUSEBUTTONDOWN:
                if self.action != None:
                    self.action()

    def update_time_dependent(self):
        """
        Updates the image of Sprite approximately every 0.1 second.

        Args:
            dt: Time elapsed between each frame.
        """
        
        self.current_time += self.dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def update_frame_dependent(self):
        """
        Updates the image of Sprite every 6 frame (approximately every 0.1 second if frame rate is 60).
        """

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def update(self):
        """
        This is the method that's being called when 'all_sprites.update(dt)' is called.
        """
        # Switch between the two update methods by commenting/uncommenting.
        # self.update_time_dependent()
        self.update_frame_dependent()



class Button():
    def __init__(self, text, font, x, y, w, h, b, border, center, active, inactive, selection, action=None):
        # Setup
        Setup.button = True
        
        # Tools
        Setup.list_button.append(self)

        # Text
        self.text = text
        self.font = font

        # Position
        self.x = x              # Position x
        self.y = y              # Position y
        self.w = w              # Width
        self.h = h              # Height
        self.b = b              # Border width
        self.border = border    # Border
        self.center = center    # Center

        # Color
        self.active     = active
        self.inactive   = inactive
        self.color      = inactive  # Color changes depending of the mouse position

        # Center button
        if self.center == True:
            self.x = x-w/2
            self.y = y-h/2
        self.rect   = pygame.Rect(self.x,self.y,self.w,self.h)

        # Action
        self.selection  = selection
        self.action     = action
        
    def check(self, index):
        mouse = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse):
            self.color = self.active
            if Tools.event.type == pygame.MOUSEBUTTONDOWN:
                if self.action != None and self.selection != None:
                    self.action(self.selection)
                elif self.action != None:
                    self.action()
        else:
            self.color = self.inactive

    def update(self, index):
        # Button
        if self.border == True:
            pygame.draw.rect(gameDisplay, Color_Black, self.rect, self.b)
        pygame.draw.rect(gameDisplay, self.color, self.rect)

        # Text
        font, color = self.font()
        textSurf = font.render(self.text, True, color)
        textRect = textSurf.get_rect()
        textRect.center = self.x+self.w/2, self.y+self.h/2
        gameDisplay.blit(textSurf, textRect)



class Button_Image():
    def __init__(self, x, y, center, active, inactive, selection, action=None):
        # Tools
        Setup.list_button_image.append(self)

        # Position
        self.x = x              # Position x
        self.y = y              # Position y
        self.center = center    # Center

        # Image
        self.active     = active.convert()
        self.inactive   = inactive.convert()
        self.image      = inactive.convert()    # Image changes depending of the mouse position

        # Center Button
        if self.center == False:
            self.rect = self.active.get_rect(topleft=(x,y))

        if self.center == True:
            self.rect = self.active.get_rect(center=(x,y))

        # Action
        self.selection  = selection
        self.action     = action
        
    def check(self, index):
        mouse = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse):
            self.image = self.active
            if Tools.event.type == pygame.MOUSEBUTTONDOWN:
                if self.action != None and self.selection != None:
                    self.action(self.selection)
                elif self.action != None:
                    self.action()
        else:
            self.image = self.inactive

    def update(self, index):
        # Button
        gameDisplay.blit(self.image, self.rect)







class Fight():
    def __init__(self):
        # State
        self.training = False
        self.turn = None
        self.button = False
        self.state_attack = False
        
        # Character / Slot / Death Status
        self.character = [PlayerIG, IrisIG, GyreiIG, None, None, None]
        self.slot   = [True, True, True, False, False, False]
        self.death  = [False, False, False, False, False, False]

        # Information
        self.time = 0
        self.stage = 1

        # Interface Position
        self.status_bar_y = 2*[590,640,690]
        
        self.character_x = [100,250,265,1055,905,890]
        self.character_y = [300,175,375,300,175,375]

        self.icon_x = 3*[10] + 3*[730]
        self.icon_y = 2*[570,620,670]
        self.name_x = 3*[135] + 3*[855]
        self.name_y = self.status_bar_y
        self.health_x = 3*[305] + 3*[1025]
        self.health_y = self.status_bar_y

        self.action_text_x = 3*[475] + 3*[1195]
        self.action_text_y = self.status_bar_y
        self.action_bar_x = 3*[401] + 3*[1121]
        self.action_bar_y = 2*[571,621,671]
        
        self.time_x = 1205
        self.stage_x = 75
        self.time_y = 25
        self.stage_y = 25



    def update_enemy(self, enemy=[], random_enemy=False):
        """
        Story Enemy     : Load enemy list from StoryIG.update_state (FIGHT)
        Training Enemy  : Generate a random enemy list
        """
        # Story Enemy
        if random_enemy == False:
            for index in range(len(enemy)):
                self.character[index+3] = enemy[index]
                self.slot[index+3] = True
                self.death[index+3] = False
                
        # Training Enemy
        elif random_enemy == True:
            Enemy_Count = random.randint(1,3)
            for index in range(Enemy_Count):
                self.character[index+3] = list_enemy[random.randint(0, len(list_enemy)-1)]("Monster %s" % (index+1))
                self.slot[index+3] = True
                self.death[index+3] = False


    def attack_choice(self):
        """
        self.state_attack   : Attack Choice State (Prevent from clicking multiple times)
        self.slot/death     : Check Enemy Slot and Death State
        Button              : Draw a Selection Button surrounding each Enemy
        """
        if self.state_attack == False:
            self.state_attack = True
            for index in range(3, 6):
                if self.slot[index] == True and self.death[index] == False:
                    sprite_rect = self.character[index].Sprite.get_rect(topleft=(self.character_x[index], self.character_y[index]))
                    Button(None, Text_Interface, sprite_rect[0]-10, sprite_rect[1]-10, sprite_rect[2]+20, sprite_rect[3]+20, 8, True, False, Color_Red, Color_Green, index, self.attack)

    def attack(self, target):
        """
        Precision   : Value generated randomly corresponding to the hit & critical chance
            [Between 0 and 100]
            
        Accuracy    : Accuracy rate of the character to hit the target
            [2.5*Level + Speed^1.2/2 + 85]
            
        Evasion     : Subtract the accuracy of the character by the evasion rate of the target
            [2.5*Level + Speed/3]
            
        Critical    : Chance to make a critical hit that doubles the damage
            [35 - 25*(Health/Maxhealth)^(0.5 + 0.25*(P.Level-E.Level))]      35 - 25*(50/100)^0.5 = 20%
            
        Damage      : Damage value between 80% and 100% of the character strength
        """
        attacker = self.character[self.turn]
        defender = self.character[target]
        
        precision   = random.randint(0, 100)
        accuracy    = 2.5*attacker.level + attacker.speed**1.2/2 + 85
        evasion     = 2.5*defender.level + defender.speed/3
        critical    = 35 - 25*(attacker.Health/attacker.Maxhealth)**(0.5 + 0.25*(attacker.level-defender.level))
        damage      = random.randint(int(0.75*attacker.Strength), int(attacker.Strength))

        print(attacker.name)
        print("Precision = %i" % precision)
        print("Accuracy = %i" % accuracy)
        print("Evasion = %i" % evasion)
        print("Hit rate = %i" % (accuracy-evasion))
        print("Critical rate = %i" % critical)
        print("Damage = %i" % damage)
        print()

        # Success
        if (accuracy-evasion) >= precision:
            # Sound
            Random_SFX = random.randint(0, len(attacker.SFX_Attack)-1)
            pygame.mixer.Sound(attacker.SFX_Attack[Random_SFX]).play()
            
            # Normal Damage
            if critical >= precision:
                defender.Health -= damage

            # Critical Damage
            else:
                defender.Health -= damage*2

            # Death
            if defender.Health < 0:
                defender.Health = 0
                defender.Action_Point = 0
                self.death[target] = True
                pygame.mixer.Sound(SFX_Battle_Defeated_battle02).play()

        # Miss
        else :
            pygame.mixer.Sound(SFX_Battle_Miss_battle14).play()

        self.end_turn()

    def end_turn(self):
        """
        Action Point    : Reset the Character Action Point to 0
        State_attack    : End Attack Choice State
        Turn            : Reset Turn to None
        Win             : Check for win condition
        """
        # Reset
        self.character[self.turn].Action_Point = 0
        self.state_attack = False
        self.turn = None

        # Win Condition
        Win = True
        for index in range(3,6):
            if self.slot[index] == True and self.death[index] == False:
                Win = False
                
        if Win == True:
            if self.training == False:
                Setup.update_init(story=True)
                StoryIG.next_file(story=True)
                Progress.fight += 1
                Progress.story += 1

            else:
                Setup.update_init(background=Interface_Fight, music=BGM_Victory_1)
                self.result()


    def result(self):
        if Setup.result == False:
            Setup.result    = True
            Setup.text      = True
            Setup.button    = True
                
            EXP  = 0
            Gold = 0
            for index in range(3,6):
                if self.slot[index] == True:
                    EXP  += self.character[index].EXP_Gain
                    Gold += self.character[index].Gold_Gain
            
            for index in range(3):
                # Player
                if self.slot[index] == True:
                    Text(self.character[index].name, 340, 180+150*index, True, Text_Interface)
                    Text(self.character[index].Class, 540, 90+150*index, True, Text_Interface)
                    Text("Level : %i" % self.character[index].level, 540, 135+150*index, True, Text_Interface)
                    Text("EXP : %i + %i" % (self.character[index].Experience, EXP), 540, 180+150*index, True, Text_Interface)

                # Enemy
                if self.slot[3+index] == True:
                    Text(self.character[3+index].name, 785, 135+95*index,  True, Text_Interface)
                    Text("Level : %i" % self.character[3+index].level, 785, 180+95*index,  True, Text_Interface)
                    
            Text("Stage : %s" % Fight.stage, 760, 430, True, Text_Interface)
            Text("Gold : %i + %i" % (PlayerIG.Gold, Gold), 760, 480, True, Text_Interface)
            Text("Result",      760, 85,  True, Text_Interface)
            Text("Inventory",   960, 85,  True, Text_Interface)
            Button("Next", Text_Button, 960, 455, 131, 86, 4, False, True, Color_Green, Color_Red, None, Menu_Zone)

            for index in range(3):
                if self.slot[index] == True:
                    self.character[index].Experience += EXP

                    while self.character[index].Experience >= 100:
                        self.character[index].update_level()
                        StoryIG.text_line[1][index] = self.character[index].name + " has Leveled Up!"
            self.character[0].Gold += Gold

        
    def update(self):
        """
        Update : User Interface
            Setup   : Refresh information each loop
            Text    : Information, Name, Health & Action_Point
            Image   : Character's Sprite & Icon
            Button  : Appears when it is the turn of a character
        """
        # Setup
        Setup.list_text = []
        
        # Information
        Text("Time: %s"  % self.time, self.time_x, self.time_y, True, Text_Interface)
        Text("Stage: %s" % self.stage, self.stage_x, self.stage_y, True, Text_Interface)

        # Characters Status
        for index in range(6):
            if self.slot[index] == True:
                # Characters - Image
                if self.death[index] == False:
                    gameDisplay.blit(self.character[index].Sprite, (self.character_x[index], self.character_y[index]))  # Sprite
                gameDisplay.blit(self.character[index].Icon, (self.icon_x[index], self.icon_y[index]))                  # Icon

                # Character - Information
                Text("%s" % self.character[index].name, self.name_x[index], self.name_y[index], True, Text_Interface)
                Text("HP: %i/%i" % (self.character[index].Health, self.character[index].Maxhealth), self.health_x[index], self.health_y[index], True, Text_Interface)

                # Character - Action Point
                Text("AP: %i/100" % self.character[index].Action_Point, self.action_text_x[index], self.action_text_y[index], True,Text_Interface)
                pygame.draw.rect(gameDisplay, Color_Green, (self.action_bar_x[index], self.action_bar_y[index], 1.48 * self.character[index].Action_Point, 38))

                
        """
        Update : Action Point
            Generate Action_Point up to 100
            When 100 is reached, give a turn to the character
            Reset List_Button after a Turn Reset
        """
        if self.turn == None:
            Setup.list_button = []
            
            for index in range(6):
                # Generating Action Point
                if self.slot[index] == True and self.death[index] == False:
                    self.character[index].Action_Point += self.character[index].speed/10
                    
                    # Gain a Turn to the character
                    if self.character[index].Action_Point > 100:
                        self.character[index].Action_Point = 100
                        self.turn   = index
                        self.button = True


        """
        Update : Turn Phase
            -Player Phase   :
                Sprite_rect : Highlight the active character
                Button      : Displays available actions
            -Enemy Phase    : Randomly attacks a player
        """
        if self.turn != None:
            # Player Phase
            if self.turn < 3:
                sprite_rect = self.character[self.turn].Sprite.get_rect(topleft=(self.character_x[self.turn], self.character_y[self.turn]))
                pygame.draw.rect(gameDisplay, Color_Red, sprite_rect, 5)

                if self.button == True:
                    self.button = False
                    Button("Attack", Text_Button, 640, 590, 140, 40, 6, True, True, Color_Button, Color_Red, None, self.attack_choice)
                    Button("Skill",  Text_Button, 640, 640, 140, 40, 6, True, True, Color_Button, Color_Red, None, None)
                    Button("Guard",  Text_Button, 640, 690, 140, 40, 6, True, True, Color_Button, Color_Red, None, None)

            # Enemy Phase
            else:
                target = []
                for index in range(3):
                    if self.slot[index] == True:
                        target.append(index)
                random_target = random.choice(target)
                self.attack(random_target)
                
Fight = Fight()



class StoryIG():
    def __init__(self):
        # Text Input
        self.textinput  = TextInput()
        self.input_line = self.textinput.get_text()
        
        # State
        self.path           = ""                                            # Path of text files
        self.bootup         = ""                                            # Run self.update() once
        self.list_story     = load_file("Data\Story")                       # Load text files
        self.list_fight     = load_file("Data\Fight")                       # Load Enemy Informations
        self.file           = open(self.list_story[Progress.story], "r")    # Open the text file
        self.read_line      = ""                                            # Line of text read from the file
        self.state_read     = True                                          # Continue/Stop Reading
        self.state_input    = False                                         # Display input field

        # Position text
        self.x              = 5
        self.y              = 565
        self.character_x    = [100, 1180]
        self.character_y    = [535, 535]
        
        # Position input_box
        self.input_x        = 540
        self.input_y        = 340
        self.input_width    = 200
        self.input_height   = 40
        self.input_border   = 5
        
        # Display
        self.index          = [0,0]                         # Line index
        self.side           = ["[L]","[R]"]                 # Side of the text
        self.character      = ["",""]                       # Name of the speaking characters
        self.text_line      = [["","","","","","",""],      # Left side text
                               ["","","","","","",""]]      # Right side text

    def update_init(self):
        self.index          = [0,0]
        self.side           = ["[L]","[R]"]
        self.character      = ["",""]
        self.text_line      = [["","","","","","",""], ["","","","","","",""]]
        self.read_line      = ""
        self.state_read     = True
        self.state_input    = False
        self.file           = open(self.list_story[Progress.story], "r")
        

            
    def update(self):
        if self.textinput.update(Tools.events) or self.bootup!=self.file:
            """
            Bootup          : Start events once to load information like background, first line, etc...
            """
            if self.bootup != self.file:
                self.bootup = self.file

            
            """
            Input_Line      : Text entered by the keyboard
            Textinput       : Text Surface
            """
            # Input Text
            self.input_line = self.textinput.get_text()
            self.textinput  = TextInput()

            """
            State_Input     : Remove the Input Field
            State_Read      : Resume reading the Text File
            PlayerIG.name   : Name of the Player entered in the Input Field
            """
            # Player Name Input
            if self.state_input == True and self.input_line != "":
                self.next_file(story=True)
                self.bootup         = self.file
                self.state_input    = False
                self.state_read     = True
                PlayerIG.name       = self.input_line
                self.character[0]   = PlayerIG.name
                self.input_line     = ""

        
            """
            Read_Line       : Next Line in Text File
            Update_State    : Check for a change of State
            Clear_Text      : Clear Text if all lines are filled
            """
            # Read
            if self.state_read == True:
                self.read_line  = self.file.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % PlayerIG.name))    # Text in File
                self.update_state()
                self.clear_text()
                
                for i in range(2):
                    if self.side[i] in self.read_line:
                        self.text_line[i][self.index[i]]                = self.read_line.replace(self.side[i], "")
                        self.text_line[i][self.index[i]+1]              = "(-> Press Enter)"
                        self.text_line[abs(i-1)][self.index[abs(i-1)]]  = ""
                        self.index[i] += 1
        self.update_display()


    def update_state(self):
        """
        Story Informations :
            Background  : Change the wallpaper by what is written in the text file
            Music       : Play the music written in the text file
            Sound       : Play the sound written in the text file
            Name        : Displays the name of the character in the corresponding side
            rstrip('\n'): Prevent reading bugs
        """
        if "(BACKGROUND)" in self.read_line:
            Setup.background = eval(self.read_line.replace("(BACKGROUND)", ""))
            self.read_line = self.file.readline().rstrip('\n')
            self.clear_text(left=True, right=True)
            self.character = ["",""]
            self.update_state()

        
        if "(MUSIC)" in self.read_line:
            Setup.update_music(eval(self.read_line.replace("(MUSIC)", "")))
            self.read_line = self.file.readline().rstrip('\n')
            self.clear_text(left=True, right=True)
            self.character = ["",""]
            self.update_state()

        
        if "(SOUND)" in self.read_line:
            eval(self.read_line.replace("(SOUND)", "")).play()
            self.read_line = self.file.readline().rstrip('\n')
            self.update_state()

    
        if "(NAME)" in self.read_line:
            for index in range(2):
                if self.side[index] in self.read_line:
                    self.character[index] = self.read_line.replace("(NAME)%s" % self.side[index], "").replace("%PlayerIG.name", ("%s" % PlayerIG.name))
            self.read_line = self.file.readline().rstrip('\n').replace("%PlayerIG.name", ("%s" % PlayerIG.name))
            self.update_state()


        """
        Story Events :
            Event   : Stop reading during an event
            Input   : Display an input field
            Next    : Open next text file
            Fight   : Start the fight with the enemies corresponding to the combat text file
            Result  : Shows victory screen
        """
        if "(INPUT)" in self.read_line:
            self.state_input    = True
            self.read_line      = self.read_line.rstrip('\n').replace("(INPUT)", "")
            self.input_line     = ""

        
        if "(EVENT)" in self.read_line:
            self.state_read = False
            self.read_line  = self.read_line.rstrip('\n').replace("(EVENT)", "")
            
        
        if "(NEXT)" in self.read_line:
            self.next_file(story=True)
            

        if "(FIGHT)" in self.read_line:
            # Informations : Load Background and Music
            self.next_file(fight=True)
            self.read_line = self.file.readline().rstrip('\n')
            self.update_state()

            enemy = []
            enemy_count = file_len(self.list_fight[Progress.fight])-3
            for index in range(enemy_count):
                enemy.append(eval(self.file.readline().rstrip('\n')))

            # User Interface
            Fight.update_enemy(enemy)
            Setup.update_init(Setup.background, Setup.music, fight=True)

        if "(RESULT)" in self.read_line:
            self.text_line[0][self.index[0]] = ""
            self.text_line[1][self.index[1]] = ""
            Fight.result()


    def update_display(self):
        """
        Background  : Cutscene's User Interface
        Text        : Character's Dialogue
        Input Box   : Display Input Field & Text Entered
        """
        # Background
        gameDisplay.blit(Interface_Cutscene, (0,0))

        # Input Box
        if self.state_input == True:
            pygame.draw.rect(gameDisplay, Color_Grey,   [self.input_x, self.input_y, self.input_width, self.input_height])
            pygame.draw.rect(gameDisplay, Color_Black,  [self.input_x, self.input_y, self.input_width, self.input_height], self.input_border)

            # Text Center
            rect    = self.textinput.get_surface()
            text_w  = rect.get_width()//2
            text_h  = rect.get_height()//2
            box_w   = self.input_x + self.input_width/2
            box_h   = self.input_y + self.input_height/2
            size    = (box_w-text_w, box_h-text_h)
            gameDisplay.blit(self.textinput.get_surface(), size)

        # Text
        for side in range(len(self.text_line)):
            self.load_text(self.character[side], self.character_x[side], self.character_y[side], True)
            for index in range(len(self.text_line[side])):
                self.load_text(self.text_line[side][index], self.x+720*side, self.y+20*index)
                

    def load_text(self, text, x, y, center=False):
        font     = pygame.font.Font("freesansbold.ttf",  35)
        textSurf = font.render(text, True, Color_Black)
        textRect = textSurf.get_rect(topleft=(x,y))
        
        if center == True:
            textRect = textSurf.get_rect(center=(x,y))

        gameDisplay.blit(textSurf, textRect)
    
    def clear_text(self, left=False, right=False):
        side = [left,right]
        for index in range(2):
            if side[index] == True or self.side[index] in self.read_line and self.index[index] == 6:
                self.text_line[index] = ["","","","","","",""]
                self.index[index] = 0

    def next_file(self, story=False, fight=False):
        self.file.close()

        if story == True:
            Progress.story += 1
            self.file = open(self.list_story[Progress.story], "r")
            
        elif fight == True:
            self.file = open(self.list_fight[Progress.fight], "r")
            self.clear_text(left=True, right=True)
                              
StoryIG = StoryIG()
    


##### ###### ##### #####



def Quit_Game():
    pygame.quit()
    quit()


    
# Game - Main Function
def Title_Screen():
    # Setup
    Setup.update_init(Background_Title_Screen_1, BGM_Title_Screen, text=True)
    
    # Button
    Button("Start",    Text_Button, 1*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, None, Main_Story)
    Button("Gallery",  Text_Button, 2*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, None, OST_Gallery)
    Button("Main",     Text_Button, 3*display_width/4, 3*display_height/4, display_width/8, display_height/12, 15, True, True, Color_Green, Color_Red, None, Menu_Zone)

    # Text
    Text(Project_Title, display_width/2, display_height/4, True, Text_Title_Screen)
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()


def Menu_Zone():
    # Setup
    Setup.update_init(Interface_Main_Menu, BGM_Menu_1, sprite=True, text=True)

    # Setup - Sprite
    AnimatedSprite(1230, 470, True, "Data\Sprite_Button\Sprite_Button_Fight",   clock.tick(FPS), 4, Main_Story)
    AnimatedSprite(615,  385, True, "Data\Sprite_Button\Sprite_Button_Traning", clock.tick(FPS), 4, Main_Training)

    # Setup - Button
    Button("Inventory", Text_Button, 120, 680, 144, 34, 0, False, True, Color_Green, Color_Red, None, Setup.inventory_init)
    Button("Status",    Text_Button, 284, 680, 144, 34, 0, False, True, Color_Green, Color_Red, None, Status)
    Button("Save",      Text_Button, 448, 680, 144, 34, 0, False, True, Color_Green, Color_Red, None, Game_Save)
    Button("Music",     Text_Button, 1083, 661, 77, 77, 0, False, True, Color_Green, Color_Red, None, OST_Gallery)
    Button("Credits",   Text_Button, 1199, 661, 77, 77, 0, False, True, Color_Green, Color_Red, None, Credits)

    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()

def Main_Story():
    # Setup
    Setup.update_init(story=True)
    StoryIG.update_init()
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()


def Main_Training():
    # Setup
    Setup.update_init(Interface_Fight, List_BGM[random.randint(8, 12)], fight=True)
    Fight.training = True

    # Enemy List
    Fight.update_enemy(random_enemy=True)
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()

    
def OST_Gallery():
    # Setup
    Setup.update_init(Background_Title_Screen_2, BGM_Title_Screen)

    # Music Buttons
    index = 0
    for row in range(round(0.5+len(List_BGM)/6)) :
        for col in range(6):
            if index < len(List_BGM):
                Button("Music %i" % (index+1), Text_Button, 60+200*col, 100+112*row, 160, 72, 12, True, False, Color_Green, Color_Red, List_BGM[index], Music_Play)
                index += 1

    # Exit Button
    Button_Image(1255, 25, True, Icon_Exit, Icon_Exit, None, Title_Screen)
    
    # Loop
    gameExit = False
    while not gameExit:
        Setup.update()
        for event in Tools.events:
            if event.type == pygame.QUIT:
                Quit_Game()

def Status():
    print("Status!")

def Game_Save():
    print("Game Saved!")

def Credits():
    print("Credits!")

Title_Screen()
