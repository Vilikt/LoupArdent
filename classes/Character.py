import random as r
from constants import *


def checkInt(stringValue):
    try:
        int(stringValue)
        return True
    except ValueError:
        return False


class Character:
    def __init__(self):
        self.name = ''
        self.strenght = 0
        self.speed = 0
        self.endurance = 0
        self.courage = 0
        self.luck = 0
        self.magnetism = 0
        self.seduction = 0
        self.skill = 0
        self.startLifePoints = 0
        self.lifePoints = 0
        self.modWeapon = 0
        self.modDefence = 0
        self.nbAssaultCumulMax = 0
        self.nbAssaultCumulActual = 0
        self.resetNbAssaultCumul()

    def resetNbAssaultCumul(self):
        self.nbAssaultCumulMax = int(int(self.endurance) / 10)
        self.nbAssaultCumulActual = 0

    def hydrateAttributes(self, enemy_values_from_window):
        if enemy_values_from_window is not None:
            self.name = enemy_values_from_window['-NAME-'] if enemy_values_from_window['-NAME-'] is not None else ''
            self.strenght = int(enemy_values_from_window['-STRENGHT-']) if checkInt(enemy_values_from_window['-STRENGHT-']) else 0
            self.speed = int(enemy_values_from_window['-SPEED-']) if checkInt(enemy_values_from_window['-SPEED-']) else 0
            self.endurance = int(enemy_values_from_window['-ENDURANCE-']) if checkInt(enemy_values_from_window['-ENDURANCE-']) else 0
            self.courage = int(enemy_values_from_window['-COURAGE-']) if checkInt(enemy_values_from_window['-COURAGE-']) else 0
            self.luck = int(enemy_values_from_window['-LUCK-']) if checkInt(enemy_values_from_window['-LUCK-']) else 0
            self.magnetism = int(enemy_values_from_window['-MAGNETISM-']) if checkInt(enemy_values_from_window['-MAGNETISM-']) else 0
            self.seduction = int(enemy_values_from_window['-SEDUCTION-']) if checkInt(enemy_values_from_window['-SEDUCTION-']) else 0
            self.skill = int(enemy_values_from_window['-SKILL-']) if checkInt(enemy_values_from_window['-SKILL-']) else 0
            self.startLifePoints = int(enemy_values_from_window['-START_LIFEPOINTS-']) if checkInt(enemy_values_from_window['-START_LIFEPOINTS-']) else 0
            self.lifePoints = int(enemy_values_from_window['-LIFEPOINTS-']) if checkInt(enemy_values_from_window['-LIFEPOINTS-']) else 0
            self.modWeapon = int(enemy_values_from_window['-MOD_WEAPON-']) if checkInt(enemy_values_from_window['-MOD_WEAPON-']) else 0
            self.modDefence = int(enemy_values_from_window['-MOD_DEFENCE-']) if checkInt(enemy_values_from_window['-MOD_DEFENCE-']) else 0
