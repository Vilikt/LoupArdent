from classes.Character import *
from constants import *
#from main import addLineToLog


class Player(Character):
    def __init__(self):
        super().__init__()

        self.nbVictory = 0
        self.name = WINDOW_TITLE

    def generate(self):
        self.strenght = (r.randint(1, 6) + r.randint(1, 6)) * 8
        self.speed = (r.randint(1, 6) + r.randint(1, 6)) * 8
        self.endurance = (r.randint(1, 6) + r.randint(1, 6)) * 8
        self.courage = (r.randint(1, 6) + r.randint(1, 6)) * 8
        self.luck = (r.randint(1, 6) + r.randint(1, 6)) * 8
        self.magnetism = (r.randint(1, 6) + r.randint(1, 6)) * 8
        self.seduction = (r.randint(1, 6) + r.randint(1, 6)) * 8
        self.startLifePoints = self.strenght + self.speed + self.endurance + self.courage + self.luck + self.magnetism + self.seduction
        self.lifePoints = self.startLifePoints

    def hydrateAttributes(self, player_values_from_window):
        if player_values_from_window is not None:
            self.strenght = int(player_values_from_window['-STRENGHT-']) if checkInt(player_values_from_window['-STRENGHT-']) else 0
            self.speed = int(player_values_from_window['-SPEED-']) if checkInt(player_values_from_window['-SPEED-']) else 0
            self.endurance = int(player_values_from_window['-ENDURANCE-']) if checkInt(player_values_from_window['-ENDURANCE-']) else 0
            self.courage = int(player_values_from_window['-COURAGE-']) if checkInt(player_values_from_window['-COURAGE-']) else 0
            self.luck = int(player_values_from_window['-LUCK-']) if checkInt(player_values_from_window['-LUCK-']) else 0
            self.magnetism = int(player_values_from_window['-MAGNETISM-']) if checkInt(player_values_from_window['-MAGNETISM-']) else 0
            self.seduction = int(player_values_from_window['-SEDUCTION-']) if checkInt(player_values_from_window['-SEDUCTION-']) else 0
            self.skill = int(player_values_from_window['-SKILL-']) if checkInt(player_values_from_window['-SKILL-']) else 0
            self.startLifePoints = int(player_values_from_window['-START_LIFEPOINTS-']) if checkInt(player_values_from_window['-START_LIFEPOINTS-']) else 0
            self.lifePoints = int(player_values_from_window['-LIFEPOINTS-']) if checkInt(player_values_from_window['-LIFEPOINTS-']) else 0
            self.nbVictory = int(player_values_from_window['-VICTORY-']) if checkInt(player_values_from_window['-VICTORY-']) else 0
            self.modWeapon = int(player_values_from_window['-MOD_WEAPON-']) if checkInt(player_values_from_window['-MOD_WEAPON-']) else 0
            self.modDefence = int(player_values_from_window['-MOD_DEFENCE-']) if checkInt(player_values_from_window['-MOD_DEFENCE-']) else 0
