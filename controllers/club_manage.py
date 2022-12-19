from models.players import Player, PlayersId
from models.tournament import Tournaments, Tournament


class ControllerMenuPlayersLists:
    """
    Menu for report and manage players
    """

    def __init__(self, view):
        """
        :param view: views.base.py
        """
        self.view = view

    def case_1(self):  # 1) Enregistrer un nouveau joueur
        # demander à la view infos
        attribut_player = self.view.menu_manage_club_case_1()
        player = Player(*attribut_player)
        # enregistrer dans la base
        player_id = Player.save(player)
        PlayersId.players_IDs.append(player_id)
        return

    def case_2(self):  # 2) Listes :
        choice = self.view.menu_manage_club_case_2()
        if choice == 0:
            return

        # ●	1) Liste de tous les acteurs :
        #   ○	par ordre alphabétique ;
        #   ○	par classement.
        elif choice == 1:
            sort = self.view.menu_manage_club_case_2_a()
            text = PlayersId.print_list_club(sort)
            self.view.menu_manage_club_case_2_print(text)
            return

        # ●	2) Liste de tous les joueurs d'un tournoi :
        #   ○	par ordre alphabétique ;
        #   ○	par classement.
        elif choice == 2:
            Tournaments.load_all()
            name_tournament = self.view.menu_manage_club_case_2_2_choice(
                Tournaments.list_tournament)
            tournament = Tournament.load(name_tournament)
            sort = self.view.menu_manage_club_case_2_a()
            text = ""
            if sort == 1:
                text = PlayersId.print_list_player_sort_abc(tournament['players'])
            elif sort == 2:
                text = PlayersId.print_list_player_sort_rank(tournament['players'])
            self.view.menu_manage_club_case_2_print(text)
            return

        # ●	3) Liste de tous les tournois.
        elif choice == 3:
            Tournaments.load_all()
            text = Tournaments.print_all()
            self.view.menu_manage_club_case_2_print(text)

        # ●	4) Liste de tous les tours d'un tournoi.
        elif choice == 4:
            Tournaments.load_all()
            name_tournament = self.view.menu_manage_club_case_2_2_choice(
                Tournaments.list_tournament)
            tournament = Tournament.load(name_tournament)
            text = tournament['rounds']
            self.view.menu_manage_club_case_2_print(text)
        # ●	5) Liste de tous les matchs d'un tournoi.

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
