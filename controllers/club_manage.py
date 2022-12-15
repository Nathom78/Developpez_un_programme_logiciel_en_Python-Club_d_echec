from models.players import Player, PlayersId


class ControllerMenuPlayersLists:

    def __init__(self, view):
        self.view = view

    def case_1(self):  # 1) Enregistrer un nouveau joueur
        # demander à la view infos
        # enregistrer dans la base
        return

    def case_2(self):  # 2) Listes :
        # ●	Liste de tous les acteurs :
        #   ○	par ordre alphabétique ;
        #   ○	par classement.
        # ●	Liste de tous les joueurs d'un tournoi :
        #   ○	par ordre alphabétique ;
        #   ○	par classement.
        # ●	Liste de tous les tournois.
        # ●	Liste de tous les tours d'un tournoi.
        # ●	Liste de tous les matchs d'un tournoi.
        # Demander quelles listes dans la view ou sortir
        # Demander infos pour le type de tris à la view
        # afficher la liste dans la view if ...
        return

    def case_3(self):  # 3) Modifier un joueur
        pass

    def case_4(self):  # 4) retour
        return 'quit'

    def choice(self, cases):
        default = "Mauvais choix"
        switch = 'case_' + str(cases)
        return getattr(self, switch, lambda: default)()

    def run(self):
        menu = ""
        while menu != 'quit':
            choice = self.view.menu_players
            menu = self.choice(choice)
        return


