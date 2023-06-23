import PySimpleGUI as sg
import os.path
import PIL.Image
import io
import base64


def getPrincipalLayaout():
    # ------ Menu Definition ------ #
    menu_def = [['Fichier', ['Nouveau', 'Ouvrir', 'Enregistrer', 'Enregistrer sous', 'Quitter']]]

    return [
        [sg.Menu(menu_def, tearoff=False)],
        [sg.Text('FEUILLE D\'AVENTURE', size=(30, 1), justification='center', font=("Arial", 25), relief=sg.RELIEF_RIDGE)],
        [sg.B('Nouveau combat', key='-NEW_FIGHT-', disabled=True)],
        [
            sg.Frame(
                layout=[
                    [sg.Text('FORCE'), sg.InputText('', size=(5, 1), key='-STRENGHT-', enable_events=True), sg.Text('RAPIDITE'), sg.InputText('', size=(5, 1), key='-SPEED-', enable_events=True), sg.Text('ENDURANCE'), sg.InputText('', size=(5, 1), key='-ENDURANCE-', enable_events=True)],
                    [sg.Text('COURAGE'), sg.InputText('', size=(5, 1), key='-COURAGE-', enable_events=True), sg.Text('CHANCE'), sg.InputText('', size=(5, 1), key='-LUCK-', enable_events=True), sg.Text('MAGNETISME'), sg.InputText('', size=(5, 1), key='-MAGNETISM-', enable_events=True)],
                    [sg.Text('SEDUCTION'), sg.InputText('', size=(5, 1), key='-SEDUCTION-', enable_events=True), sg.Text('HABILETE'), sg.InputText('', size=(5, 1), key='-SKILL-', enable_events=True)],
                    [sg.Text('TOTAL DE DEPART DE POINTS DE VIE'), sg.InputText('', size=(5, 1), key='-START_LIFEPOINTS-', enable_events=True)],
                    [sg.Text('TOTAL ACTUEL'), sg.InputText('', size=(5, 1), key='-LIFEPOINTS-', enable_events=True)],
                ], title='Points de vie de LOUP*ARDENT', title_color='red', relief=sg.RELIEF_SUNKEN
            )
        ],
        [
            sg.Frame(
                layout=[
                    [sg.Text('NOMBRE DE COMBATS VICTORIEUX'), sg.InputText('', size=(5, 1), key='-VICTORY-', enable_events=True)],
                    [sg.Text('MODIFICATEUR D\'ARME'), sg.InputText('', size=(5, 1), key='-MOD_WEAPON-', enable_events=True)],
                    [sg.Text('MODIFICATEUR DE DEFENSE'), sg.InputText('', size=(5, 1), key='-MOD_DEFENCE-', enable_events=True)],
                ], title='Données de combats', title_color='red', relief=sg.RELIEF_SUNKEN
            )
        ]
    ]


def convertToBytes(filename, resize=(30, 30)):
    img = PIL.Image.open(filename)
    cur_width, cur_height = img.size
    new_width, new_height = resize
    scale = min(new_height / cur_height, new_width / cur_width)
    img = img.resize((int(cur_width * scale), int(cur_height * scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img

    return bio.getvalue()


def getFightLayout():
    # ------ Menu Definition ------ #
    menu_def = [['Fichier', ['Ouvrir', 'Quitter', 'Enregistrer sous']]]

    # dices images
    data = convertToBytes('assets/dice0.png')

    return [
        [sg.Menu(menu_def, tearoff=False)],
        [sg.Text('COMBAT EN COURS', size=(30, 1), justification='center', font=("Arial", 25), relief=sg.RELIEF_RIDGE)],
        [
            [
                sg.Frame(
                    layout=[
                        [sg.B('Déterminer', key='-BEGIN_NORMAL-', disabled=True),
                         sg.B('Loup*Ardent', key='-BEGIN_PLAYER-', disabled=True),
                         sg.B('Ennemi', key='-BEGIN_ENEMY-', disabled=True)]
                    ], title='Qui commence', title_color='red', relief=sg.RELIEF_SUNKEN
                ),
                sg.Frame(
                    layout=[
                        [sg.B('Prochain assaut', key='-NEXT_ASSAULT-', disabled=True),
                         sg.B('Terminer', key='-STOP-')],
                    ], title='Commande combat', title_color='red', relief=sg.RELIEF_SUNKEN
                )
            ],
            [
                sg.Frame(
                    layout=[
                        [sg.Text('NOM'), sg.InputText('', size=(20, 1), key='-NAME-', enable_events=True)],
                        [sg.Text('FORCE'), sg.InputText('', size=(5, 1), key='-STRENGHT-', enable_events=True), sg.Text('RAPIDITE'), sg.InputText('', size=(5, 1), key='-SPEED-', enable_events=True), sg.Text('ENDURANCE'), sg.InputText('', size=(5, 1), key='-ENDURANCE-', enable_events=True)],
                        [sg.Text('COURAGE'), sg.InputText('', size=(5, 1), key='-COURAGE-', enable_events=True), sg.Text('CHANCE'), sg.InputText('', size=(5, 1), key='-LUCK-', enable_events=True), sg.Text('MAGNETISME'), sg.InputText('', size=(5, 1), key='-MAGNETISM-', enable_events=True)],
                        [sg.Text('SEDUCTION'), sg.InputText('', size=(5, 1), key='-SEDUCTION-', enable_events=True), sg.Text('HABILETE'), sg.InputText('', size=(5, 1), key='-SKILL-', enable_events=True)],
                        [sg.Text('TOTAL DE DEPART DE POINTS DE VIE'), sg.InputText('', size=(5, 1), key='-START_LIFEPOINTS-', enable_events=True)],
                        [sg.Text('TOTAL ACTUEL'), sg.InputText('', size=(5, 1), key='-LIFEPOINTS-', enable_events=True)]
                    ], title='Caractéristiques de l\'adversaire', title_color='red', relief=sg.RELIEF_SUNKEN
                ),
                [
                    sg.Frame(
                        layout=[
                            [sg.Text('MODIFICATEUR D\'ARME'), sg.InputText('', size=(5, 1), key='-MOD_WEAPON-', enable_events=True)],
                            [sg.Text('MODIFICATEUR DE DEFENSE'), sg.InputText('', size=(5, 1), key='-MOD_DEFENCE-', enable_events=True)]
                        ], title='Données de combat', title_color='red', relief=sg.RELIEF_SUNKEN
                    ),
                    sg.Frame(
                        layout=[
                            [sg.Image(key='-DICE1-', data=data, size=(30, 30), enable_events=True), sg.Image(key='-DICE2-', data=data, size=(30, 30), enable_events=True)],
                            [sg.B('Lancer', key='-DICE_LAUNCH-')]
                        ], title='Dés', title_color='red', relief=sg.RELIEF_SUNKEN
                    ),
                    sg.Frame(
                        layout=[
                            [sg.Text('Loup*Ardent : '), sg.Text('0', key='-NB_ASSAULT_PLAYER-'), sg.Text(' / '), sg.Text('', key='-NB_ASSAULT_MAX_PLAYER-')],
                            [sg.Text('Adversaire : '), sg.Text('0', key='-NB_ASSAULT_ENEMY-'), sg.Text(' / '), sg.Text('', key='-NB_ASSAULT_MAX_ENEMY-')]
                        ], title='Nombre d\'assaults cumulés', title_color='red', relief=sg.RELIEF_SUNKEN
                    ),
                    sg.Frame(
                        layout=[
                            [sg.Text('', key='-LIFEPOINTS_PLAYER-')]
                        ], title='PV restant de Loup*Ardent', title_color='red', relief=sg.RELIEF_SUNKEN
                    ),
                ]
            ]
        ],
        [sg.MLine(key='-LOG-', size=(100, 20))]
    ]
