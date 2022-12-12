from views.base import View
from models.players import Player, Players


class ListPlayerClub:

    def __init__(self):
        self.view = View

    def case_1(self):  # 1) Enregistrer un nouveau joueur
        pass

    def case_2(self):  # 2) Liste des joueurs
        pass

    def case_3(self):  # 3) Modifier un joueur
        pass

    def case_4(self):  # 4) Retour
        pass

    def choice(self, cases):
        default = "Mauvais choix"
        switch = 'case_' + str(cases)
        return getattr(self, switch, lambda: default)()

    def run(self):
        switcher = ListPlayerClub()
        choice = self.view.menu_players
        switcher.choice(choice)

