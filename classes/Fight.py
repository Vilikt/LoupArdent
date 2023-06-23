from enum import Enum, auto
#from main import addLineToLog


class AutoName(Enum):
    def _generate_next_value_(self, start, count, last_values):
        return self


class FightState(AutoName):
    DETERMINE_BEGIN_TYPE = auto()
    DETERMINE_PLAYER_ATTACK_FORCE = auto()
    DETERMINE_ENEMY_ATTACK_FORCE = auto()
    WAIT_FOR_NEXT_ASSAULT = auto()
    WAIT_FOR_TRY_TO_STRIKE = auto()


class Turn(AutoName):
    TURN_PLAYER = auto()
    TURN_ENEMY = auto()


class Fight:
    def __init__(self, player, enemy, log):
        self.player = player
        self.enemy = enemy
        self.state = None
        self.player_attack_force = 0
        self.enemy_attack_force = 0
        self.actual_turn = None
        self.log = log

        self.attacker = None
        self.attacked = None
        self.text_color = ''
        self.background_color = ''

        self.total_to_reach = 0

        self.started = False
        self.over = False

    def writePlayerAttackForce(self, dicevalues):
        dice1, dice2 = dicevalues

        self.player_attack_force = dice1 + dice2 + self.player.speed + self.player.courage + self.player.luck
        self.log.addLineToLog('Force d\'attaque de ' + self.player.name + ' = ' + str(
            dice1 + dice2) + ' + RAPIDITE(' + str(self.player.speed) + ') + COURAGE(' + str(
            self.player.courage) + ') + CHANCE(' + str(self.player.luck) + ') = ' + str(self.player_attack_force), 'white', 'green')

    def writeEnemyAttackForce(self, dicevalues):
        dice1, dice2 = dicevalues

        self.enemy_attack_force = dice1 + dice2 + self.enemy.speed + self.enemy.courage + self.enemy.luck
        self.log.addLineToLog('Force d\'attaque de ' + self.enemy.name + ' = ' + str(
            dice1 + dice2) + ' + RAPIDITE(' + str(self.enemy.speed) + ') + COURAGE(' + str(
            self.enemy.courage) + ') + CHANCE(' + str(self.enemy.luck) + ') = ' + str(self.enemy_attack_force), 'white', 'red')

    def initializeFight(self, turn=None):
        if turn is None:
            self.actual_turn = Turn.TURN_PLAYER if self.player_attack_force > self.enemy_attack_force else Turn.TURN_ENEMY
        else:
            self.actual_turn = turn

        self.player.resetNbAssaultCumul()
        self.enemy.resetNbAssaultCumul()

        if self.actual_turn is Turn.TURN_PLAYER:
            self.log.addLineToLog(self.player.name + ' attaque le premier')
        elif self.actual_turn is Turn.TURN_ENEMY:
            self.log.addLineToLog(self.enemy.name + ' attaque le premier')

        self.state = FightState.WAIT_FOR_NEXT_ASSAULT

    def setAttacker(self, attacker):
        if attacker.nbAssaultCumulActual >= attacker.nbAssaultCumulMax:
            if attacker is self.player:
                attacked_name = self.enemy.name
            elif attacker is self.enemy:
                attacked_name = self.player.name

            self.log.addLineToLog(attacker.name + ' à atteint ses limites d\'ENDURANCE, ' + attacked_name + ' va attaquer!', 'red', 'yellow')
            attacker.nbAssaultCumulActual = 0
            self.changeTurn()
        else:
            if attacker is self.player:
                self.attacker = self.player
                self.attacked = self.enemy
                self.text_color = 'white'
                self.background_color = 'green'
            elif attacker is self.enemy:
                self.attacker = self.enemy
                self.attacked = self.player
                self.text_color = 'white'
                self.background_color = 'red'

    def changeTurn(self):
        if self.actual_turn is Turn.TURN_PLAYER:
            self.actual_turn = Turn.TURN_ENEMY
            self.setAttacker(self.enemy)
        elif self.actual_turn is Turn.TURN_ENEMY:
            self.actual_turn = Turn.TURN_PLAYER
            self.setAttacker(self.player)

    def nextAssault(self):
        if self.actual_turn is Turn.TURN_PLAYER:
            self.setAttacker(self.player)
        elif self.actual_turn is Turn.TURN_ENEMY:
            self.setAttacker(self.enemy)

        self.tryToStrike()

    def tryToStrike(self):
        self.log.addLineToLog(' ', 'black', 'white')
        self.total_to_reach = 7 - int(self.attacker.skill / 10)
        if self.attacker.luck >= 72:
            self.total_to_reach -= 1

        self.log.addLineToLog(
            self.attacker.name + ' tente de porter un coup... Score à atteindre = ' + str(self.total_to_reach),
            self.text_color, self.background_color)

        self.state = FightState.WAIT_FOR_TRY_TO_STRIKE

    def dertermineIfStrike(self, dicevalues):
        dice1, dice2 = dicevalues

        dices_result = dice1 + dice2

        if dices_result >= self.total_to_reach:
            self.log.addLineToLog(self.attacker.name + ' touche ' + self.attacked.name + '!', self.text_color, self.background_color)
            self.log.addLineToLog(self.attacker.name + ' a ' + str(dices_result - self.total_to_reach) + ' de plus que le score a atteindre', self.text_color, self.background_color)
            theoretic_wound = (dices_result - self.total_to_reach) * 10
            self.log.addLineToLog('La blessure théorique est donc de ' + str(theoretic_wound), self.text_color, self.background_color)
            force_add_value = int(self.attacker.strenght / 8)
            theoretic_wound += force_add_value
            self.log.addLineToLog('La FORCE de ' + self.attacker.name + ' étant de ' + str(self.attacker.strenght) + ', on y ajoute ' + str(force_add_value) + '. Soit ' + str(theoretic_wound), self.text_color, self.background_color)
            theoretic_wound += self.attacker.modWeapon

            if self.attacked.modWeapon > 0:
                self.log.addLineToLog('Grâce à son arme, ' + self.attacker.name + ' inflige +' + str(self.attacker.modWeapon) + '. Soit ' + str(theoretic_wound), self.text_color, self.background_color)

            if self.attacked.modDefence > 0:
                self.log.addLineToLog('Cependant, l\'équipement de ' + self.attacked.name + ' le protège de -' + str(self.attacked.modDefence), self.text_color, self.background_color)
                theoretic_wound -= self.attacked.modDefence

            self.attacked.lifePoints = self.attacked.lifePoints - theoretic_wound

            self.log.addLineToLog('La blessure infligée est de ' + str(theoretic_wound) + '.', self.text_color, self.background_color)
            self.log.addLineToLog('Il reste ' + str(self.attacked.lifePoints) + ' PV à ' + self.attacked.name + '.', self.text_color, self.background_color)
            self.checkIfIsOver()
        else:
            self.log.addLineToLog(self.attacker.name + ' a râté son coup...', self.text_color, self.background_color)

        self.attacker.nbAssaultCumulActual += 1

        self.state = FightState.WAIT_FOR_NEXT_ASSAULT
        self.changeTurn()

    def checkIfIsOver(self):
        name = ''

        if self.player.lifePoints <= 0:
            name = self.player.name
        elif self.enemy.lifePoints <= 0:
            name = self.enemy.name

        if name != '':
            self.log.addLineToLog(name + ' est mort... Fin du combat')
            self.over = True
