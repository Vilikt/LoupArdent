import PySimpleGUI as sg
import os
from classes.Character import *
from classes.Player import *
from classes.Fight import *
from classes.Log import *
from constants import *
from layout import *

LOADED_CHARACTER = None
LOADED_CHARACTER_FILENAME = ''
PRINCIPAL_WINDOW = None
FIGHT_WINDOW = None
DICES_VALUES = (1, 1)


def updateSheetValues():
    global PRINCIPAL_WINDOW, LOADED_CHARACTER

    PRINCIPAL_WINDOW['-STRENGHT-'].update(str(LOADED_CHARACTER.strenght))
    PRINCIPAL_WINDOW['-SPEED-'].update(str(LOADED_CHARACTER.speed))
    PRINCIPAL_WINDOW['-ENDURANCE-'].update(str(LOADED_CHARACTER.endurance))
    PRINCIPAL_WINDOW['-COURAGE-'].update(str(LOADED_CHARACTER.courage))
    PRINCIPAL_WINDOW['-LUCK-'].update(str(LOADED_CHARACTER.luck))
    PRINCIPAL_WINDOW['-MAGNETISM-'].update(str(LOADED_CHARACTER.magnetism))
    PRINCIPAL_WINDOW['-SEDUCTION-'].update(str(LOADED_CHARACTER.seduction))
    PRINCIPAL_WINDOW['-SKILL-'].update(str(LOADED_CHARACTER.skill))
    PRINCIPAL_WINDOW['-START_LIFEPOINTS-'].update(str(LOADED_CHARACTER.startLifePoints))
    PRINCIPAL_WINDOW['-LIFEPOINTS-'].update(str(LOADED_CHARACTER.lifePoints))
    PRINCIPAL_WINDOW['-VICTORY-'].update(str(LOADED_CHARACTER.nbVictory))
    PRINCIPAL_WINDOW['-MOD_WEAPON-'].update(str(LOADED_CHARACTER.modWeapon))
    PRINCIPAL_WINDOW['-MOD_DEFENCE-'].update(str(LOADED_CHARACTER.modDefence))
    PRINCIPAL_WINDOW['-NEW_FIGHT-'].update(disabled=False)


def updateFightSheetValues(enemy):
    global FIGHT_WINDOW, LOADED_CHARACTER

    FIGHT_WINDOW['-NAME-'].update(str(enemy.name))
    FIGHT_WINDOW['-STRENGHT-'].update(str(enemy.strenght))
    FIGHT_WINDOW['-SPEED-'].update(str(enemy.speed))
    FIGHT_WINDOW['-ENDURANCE-'].update(str(enemy.endurance))
    FIGHT_WINDOW['-COURAGE-'].update(str(enemy.courage))
    FIGHT_WINDOW['-LUCK-'].update(str(enemy.luck))
    FIGHT_WINDOW['-MAGNETISM-'].update(str(enemy.magnetism))
    FIGHT_WINDOW['-SEDUCTION-'].update(str(enemy.seduction))
    FIGHT_WINDOW['-SKILL-'].update(str(enemy.skill))
    FIGHT_WINDOW['-START_LIFEPOINTS-'].update(str(enemy.startLifePoints))
    FIGHT_WINDOW['-LIFEPOINTS-'].update(str(enemy.lifePoints))
    FIGHT_WINDOW['-MOD_WEAPON-'].update(str(enemy.modWeapon))
    FIGHT_WINDOW['-MOD_DEFENCE-'].update(str(enemy.modDefence))
    FIGHT_WINDOW['-NB_ASSAULT_PLAYER-'].update(str(LOADED_CHARACTER.nbAssaultCumulActual))
    FIGHT_WINDOW['-NB_ASSAULT_ENEMY-'].update(str(enemy.nbAssaultCumulActual))
    FIGHT_WINDOW['-NB_ASSAULT_MAX_ENEMY-'].update(str(enemy.nbAssaultCumulMax))
    FIGHT_WINDOW['-LIFEPOINTS_PLAYER-'].update(str(LOADED_CHARACTER.lifePoints))


def savePlayerFile(file_name, player):
    global PRINCIPAL_WINDOW, LOADED_CHARACTER_FILENAME

    saveCharacterFile(file_name, player)

    if file_name is not None:
        LOADED_CHARACTER_FILENAME = file_name
        PRINCIPAL_WINDOW.set_title(WINDOW_TITLE + " : " + LOADED_CHARACTER_FILENAME)


def saveCharacterFile(file_name, character):
    if file_name is None or not os.path.isfile(file_name):
        return

    file = open(file_name, "w")
    for att in character.__dict__.keys():
        print(att, getattr(character, att))
        file.write('{:30s}|{:30s}'.format(att, str(getattr(character, att))))
    file.close()


def loadFile(file_name, character):
    if file_name is None or not os.path.isfile(file_name):
        return

    file = open(file_name, "r")
    char_data = file.read(61)
    while char_data:
        name, value = char_data.split('|')
        if name in ('strenght', 'speed', 'endurance', 'courage', 'luck', 'magnetism', 'seduction', 'startLifePoints', 'lifePoints'):
            character.__setattr__(name.strip(), int(value.strip()))
        else:
            character.__setattr__(name.strip(), str(value.strip()))
        char_data = file.read(61)
    file.close()


def loadPlayerFile(file_name, player):
    global PRINCIPAL_WINDOW, LOADED_CHARACTER_FILENAME

    loadFile(file_name, player)
    player.resetNbAssaultCumul()

    if file_name is not None:
        LOADED_CHARACTER_FILENAME = file_name
        PRINCIPAL_WINDOW.set_title(WINDOW_TITLE + " : " + LOADED_CHARACTER_FILENAME)

        updateSheetValues()


def loadCharacterFile(file_name, character):
    loadFile(file_name, character)
    character.resetNbAssaultCumul()

    if file_name is not None:
        updateFightSheetValues(character)


def checkEnemyIntegrity(values):
    global FIGHT_WINDOW

    integrity = True

    if values['-NAME-'] == '':
        integrity = False
    if not checkInt(values['-STRENGHT-']) or int(values['-STRENGHT-']) < 0 or int(values['-STRENGHT-']) > 100:
        integrity = False
    if not checkInt(values['-SPEED-']) or int(values['-SPEED-']) < 0 or int(values['-SPEED-']) > 100:
        integrity = False
    if not checkInt(values['-ENDURANCE-']) or int(values['-ENDURANCE-']) < 0 or int(values['-ENDURANCE-']) > 100:
        integrity = False
    if not checkInt(values['-COURAGE-']) or int(values['-COURAGE-']) < 0 or int(values['-COURAGE-']) > 100:
        integrity = False
    if not checkInt(values['-LUCK-']) or int(values['-LUCK-']) < 0 or int(values['-LUCK-']) > 100:
        integrity = False
    if not checkInt(values['-MAGNETISM-']) or int(values['-MAGNETISM-']) < 0 or int(values['-MAGNETISM-']) > 100:
        integrity = False
    if not checkInt(values['-SEDUCTION-']) or int(values['-SEDUCTION-']) < 0 or int(values['-SEDUCTION-']) > 100:
        integrity = False
    if not checkInt(values['-SKILL-']) or int(values['-SKILL-']) < 0 or int(values['-SKILL-']) > 100:
        integrity = False
    if not checkInt(values['-START_LIFEPOINTS-']) or int(values['-START_LIFEPOINTS-']) < 0 or int(values['-START_LIFEPOINTS-']) > 999:
        integrity = False
    if not checkInt(values['-LIFEPOINTS-']) or int(values['-LIFEPOINTS-']) < 0 or int(values['-LIFEPOINTS-']) > int(values['-START_LIFEPOINTS-']):
        integrity = False
    if not checkInt(values['-MOD_WEAPON-']) or int(values['-MOD_WEAPON-']) < 0:
        integrity = False
    if not checkInt(values['-MOD_DEFENCE-']) or int(values['-MOD_DEFENCE-']) < 0:
        integrity = False

    return integrity


def setStartFightButtons(disable):
    global FIGHT_WINDOW

    FIGHT_WINDOW['-BEGIN_NORMAL-'].update(disabled=disable)
    FIGHT_WINDOW['-BEGIN_PLAYER-'].update(disabled=disable)
    FIGHT_WINDOW['-BEGIN_ENEMY-'].update(disabled=disable)


def launchDices():
    global FIGHT_WINDOW, DICES_VALUES

    die1 = r.randint(1, 6)
    die2 = r.randint(1, 6)

    FIGHT_WINDOW['-DICE1-'].update(data=convertToBytes('assets/dice' + str(die1) + '.png'))
    FIGHT_WINDOW['-DICE2-'].update(data=convertToBytes('assets/dice' + str(die2) + '.png'))

    DICES_VALUES = (die1, die2)


def resetDices():
    global FIGHT_WINDOW, DICES_VALUES

    FIGHT_WINDOW['-DICE1-'].update(data=convertToBytes('assets/dice0.png'))
    FIGHT_WINDOW['-DICE2-'].update(data=convertToBytes('assets/dice0.png'))

    DICES_VALUES = (0, 0)


def main():
    global LOADED_CHARACTER, LOADED_CHARACTER_FILENAME, PRINCIPAL_WINDOW, FIGHT_WINDOW, DICES_VALUES

    sg.theme('DarkAmber')

    LOADED_CHARACTER = Player()
    PRINCIPAL_WINDOW = sg.Window(WINDOW_TITLE, getPrincipalLayaout(), default_element_size=(40, 1), grab_anywhere=False, finalize=True)
    updateSheetValues()
    PRINCIPAL_WINDOW['-NEW_FIGHT-'].update(disabled=True)
    focus = 'PRINCIPAL_WINDOW'

    cont = True
    enemy = Character()
    fight = None
    log = None
    just_quit_fight_window = False

    while cont:
        # Principal Window events
        if focus == 'PRINCIPAL_WINDOW':
            event_princ, values_princ = PRINCIPAL_WINDOW.read()

            LOADED_CHARACTER.hydrateAttributes(values_princ)

            if event_princ == sg.WIN_CLOSED or event_princ == 'Quitter':
                cont = False
            elif event_princ == 'Nouveau':
                LOADED_CHARACTER.generate()
                updateSheetValues()
            elif event_princ == 'Enregistrer sous':
                LOADED_CHARACTER.hydrateAttributes(values_princ)
                file_name = sg.PopupGetFile('Entrer le nom absolu du fichier', save_as=True)
                savePlayerFile(file_name, LOADED_CHARACTER)
            elif event_princ == 'Enregistrer':
                if LOADED_CHARACTER_FILENAME == '':
                    LOADED_CHARACTER_FILENAME = sg.PopupGetFile('Entrer le nom absolu du fichier', save_as=True)

                LOADED_CHARACTER.hydrateAttributes(values_princ)
                savePlayerFile(LOADED_CHARACTER_FILENAME, LOADED_CHARACTER)
            elif event_princ == 'Ouvrir':
                file_name = sg.PopupGetFile('Choisir un fichier *.pers')
                loadPlayerFile(file_name, LOADED_CHARACTER)
            elif event_princ == '-NEW_FIGHT-':
                FIGHT_WINDOW = sg.Window('Combat', getFightLayout(), default_element_size=(40, 1), grab_anywhere=False, finalize=True)
                PRINCIPAL_WINDOW['-NEW_FIGHT-'].update(disabled=True)
                focus = 'FIGHT_WINDOW'
                log = Log(FIGHT_WINDOW['-LOG-'])
                FIGHT_WINDOW['-NB_ASSAULT_MAX_PLAYER-'].update(str(LOADED_CHARACTER.nbAssaultCumulMax))
                fight = Fight(LOADED_CHARACTER, enemy, log)
                fight.state = FightState.DETERMINE_BEGIN_TYPE

        # Fight Window events
        elif focus == 'FIGHT_WINDOW':
            event_fight, values_fight = FIGHT_WINDOW.read()

            enemy.hydrateAttributes(values_fight)

            # Fight states
            if fight.state == FightState.DETERMINE_BEGIN_TYPE:
                if event_fight == '-BEGIN_NORMAL-':
                    fight.started = True
                    log.addLineToLog('Détermination de qui attaque le premier', 'red', 'yellow')
                    fight.state = FightState.DETERMINE_PLAYER_ATTACK_FORCE
                    log.addLineToLog('Veuillez lancer les dés pour ' + LOADED_CHARACTER.name, 'red', 'yellow')
                    setStartFightButtons(disable=True)
                elif event_fight == '-BEGIN_PLAYER-':
                    fight.started = True
                    fight.initializeFight(Turn.TURN_PLAYER)
                    setStartFightButtons(disable=True)
                    FIGHT_WINDOW['-NEXT_ASSAULT-'].update(disabled=False)
                elif event_fight == '-BEGIN_ENEMY-':
                    fight.started = True
                    fight.initializeFight(Turn.TURN_ENEMY)
                    setStartFightButtons(disable=True)
                    FIGHT_WINDOW['-NEXT_ASSAULT-'].update(disabled=False)

            if event_fight == 'Ouvrir':
                file_name = sg.PopupGetFile('Choisir un fichier *.enn')
                loadCharacterFile(file_name, enemy)
                if checkEnemyIntegrity(values_fight):
                    setStartFightButtons(disable=False)
            elif event_fight == 'Enregistrer sous':
                enemy.hydrateAttributes(values_fight)
                file_name = sg.PopupGetFile('Entrer le nom absolu du fichier', save_as=True)
                saveCharacterFile(file_name, enemy)
            elif event_fight == '-STOP-' or event_fight == 'Quitter':
                FIGHT_WINDOW.close()
                focus = 'PRINCIPAL_WINDOW'
                PRINCIPAL_WINDOW['-NEW_FIGHT-'].update(disabled=False)
                updateSheetValues()
                del fight
                just_quit_fight_window = True
            elif event_fight == sg.WIN_CLOSED:
                focus = 'PRINCIPAL_WINDOW'
                PRINCIPAL_WINDOW['-NEW_FIGHT-'].update(disabled=False)
                updateSheetValues()
            elif event_fight in ('-NAME-', '-STRENGHT-', '-SPEED-', '-ENDURANCE-', '-COURAGE-', '-LUCK-', '-MAGNETISM-', '-SEDUCTION-', '-SKILL-', '-START_LIFEPOINTS-', '-LIFEPOINTS-', '-MOD_WEAPON-', '-MOD_DEFENCE-'):
                if checkEnemyIntegrity(values_fight) and not fight.started:
                    setStartFightButtons(disable=False)
                else:
                    setStartFightButtons(disable=True)
            elif event_fight == '-NEXT_ASSAULT-':
                if fight.state is FightState.WAIT_FOR_NEXT_ASSAULT:
                    fight.nextAssault()
                    fight.log.addLineToLog('Veuillez lancer les dés pour ' + fight.attacker.name, fight.text_color, fight.background_color)
            elif event_fight == '-DICE_LAUNCH-':
                launchDices()

                if fight.state is FightState.DETERMINE_PLAYER_ATTACK_FORCE:
                    fight.writePlayerAttackForce(DICES_VALUES)
                    fight.state = FightState.DETERMINE_ENEMY_ATTACK_FORCE
                    log.addLineToLog('Veuillez lancer les dés pour ' + enemy.name, 'red', 'yellow')
                elif fight.state is FightState.DETERMINE_ENEMY_ATTACK_FORCE:
                    fight.writeEnemyAttackForce(DICES_VALUES)
                    fight.initializeFight()
                    FIGHT_WINDOW['-NEXT_ASSAULT-'].update(disabled=False)
                elif fight.state is FightState.WAIT_FOR_TRY_TO_STRIKE:
                    fight.dertermineIfStrike(DICES_VALUES)

                if fight.over:
                    FIGHT_WINDOW['-NEXT_ASSAULT-'].update(disabled=True)

            if not just_quit_fight_window:
                FIGHT_WINDOW['-LOG-'].set_vscroll_position(100)
                updateFightSheetValues(enemy)

            updateSheetValues()

    PRINCIPAL_WINDOW.close()


if __name__ == '__main__':
    main()
