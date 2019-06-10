import random

from Ressources import *


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
        self.Strength       = 8     + 1.5 * (self.level-1)
        self.Speed          = 10    + 0.8 * (self.level-1)
        self.Defense        = 3     + 1.3 * (self.level-1)
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
        self.Strength       = 10    + 2.0 * (self.level-1)
        self.Speed          = 8     + 0.9 * (self.level-1)
        self.Defense        = 2     + 0.7 * (self.level-1)
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
        self.Strength       = 6     + 1.2 * (self.level-1)
        self.Speed          = 12    + 1.4 * (self.level-1)
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
        self.Speed      = 4 + 1 * (self.level - 1)
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
        self.Speed      = 6 + 1 * (self.level - 1)
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
        self.Speed      = 3 + 1 * (self.level - 1)
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
        self.Speed      = 3 + 1 * (self.level - 1)
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
        self.Speed      = 3 + 1 * (self.level - 1)
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
        self.Speed      = 3 + 1 * (self.level - 1)
        self.Defense    = 1 + 0.5 * (self.level - 1)
        self.Resistance = 0 + 0.5 * (self.level - 1)
Shadow_BlueIG = Shadow_Blue("Shadow_Blue")


list_enemy = [Wolf, Direwolf, Ghoul, Zombie, Shadow_Red, Shadow_Blue]
