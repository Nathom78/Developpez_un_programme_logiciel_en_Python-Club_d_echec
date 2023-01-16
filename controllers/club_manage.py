from models.players import Player, PlayersId
from models.tournament import Tournaments, Tournament


class ControllerMenu:
    """
    Menu for report and manage players
    """

    load = 0

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
        player_id = Player.create(player)
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
            # choix du tournoi
            Tournaments.load_all()
            name_tournament = self.view.menu_manage_club_case_2_2_choice(
                Tournaments.list_tournament)
            if name_tournament == 0:
                return
            tournament = Tournament.load(name_tournament)
            # choix du classement
            sort = self.view.menu_manage_club_case_2_a()
            # Affichage
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

        # ●	4) Liste de tous les rounds d'un tournoi.
        elif choice == 4:
            Tournaments.load_all()
            name_tournament = self.view.menu_manage_club_case_2_2_choice(
                Tournaments.list_tournament)
            if name_tournament == 0:
                return
            tournament: Tournament = Tournament.load(name_tournament)
            text = ""
            for ronde in tournament['rounds']:
                text += f"{ronde}\n"
            self.view.menu_manage_club_case_2_print(text)
            return

        # ●	5) Liste de tous les matchs d'un tournoi.
        elif choice == 5:
            Tournaments.load_all()
            name_tournament = self.view.menu_manage_club_case_2_2_choice(
                Tournaments.list_tournament)
            if name_tournament == 0:
                return
            tournament: Tournament = Tournament.load(name_tournament)
            for ronde in tournament['rounds']:
                text = f"\n{ronde['name']}"
                self.view.menu_manage_club_case_2_print(text)
                for match in ronde['list_matches']:

                    try:
                        ([player1_id, player1_score], [player2_id, player2_score]) = \
                            match['result_match']
                    except ValueError:
                        [player1, player2] = match.match_players_ids_to_players()
                        text = f"Match {player1['family_name']} {player1['first_name']} " \
                               f"contre {player2['family_name']} {player2['first_name']} :\n" \
                               f"match non joué\n"
                    else:
                        player1 = PlayersId.id_to_dict(player1_id)
                        player2 = PlayersId.id_to_dict(player2_id)
                        if player1_score > player2_score:
                            winner = f"{player1['family_name']} {player1['first_name']}"
                        elif player1_score < player2_score:
                            winner = f"{player1['family_name']} {player1['first_name']}"
                        else:
                            winner = "match nul"
                        text = f"Match {player1['family_name']} {player1['first_name']} " \
                               f"contre {player2['family_name']} {player2['first_name']}\n" \
                               f"Le gagnant est : {winner}\n"

                    self.view.menu_manage_club_case_2_print(text)
        return

    def case_3(self):  # 3) Modifier un joueur
        # afficher la list du club afin de choisir le joueur
        text = PlayersId.print_list_club()
        nb_player = len(PlayersId.players_IDs)
        player_id = self.view.menu_manage_club_case_3_1(text, nb_player)
        # modification des valeurs par la vue
        player = PlayersId.id_to_dict(player_id)
        player_modify = self.view.menu_manage_club_case_3_2(player)
        # enregistrement du joueur et dire ok
        text2 = ""
        try:
            ok = Player.modify(player_modify, player_id)
            if ok == "ok":
                text2 = f"Joueur {player_modify['family_name']}" \
                       f" {player_modify['first_name']} est bien modifié"
        except ValueError:
            text2 = f"Joueur {player_modify['family_name']} " \
                   f"{player_modify['first_name']} n'a pas été enregistré, veuillez avertir " \
                   "l'administrateur"
        finally:
            self.view.menu_manage_club_case_3_3(text2)
        return

    def case_4(self):  # 4) Enregistrer le tournoi
        tournaments = Tournaments.tournaments_actif
        tournament = self.view.menu_manage_club_case_4_choice(tournaments)
        if isinstance(tournament, Tournament):
            tournament.save()
            self.view.menu_manage_club_case_4_done(tournament['name'])
        else:
            raise ValueError("Erreur Tournament not save ")
        return

    def case_5(self):  # 5) Charger un tournoi
        self.load = 1
        return 'load'

    @staticmethod
    def case_6():  # 6) Quitter
        exit()

    @staticmethod
    def case_7():  # 7) Continuer
        return 'quit'

    def choice(self, cases):
        default = "Mauvais choix"
        switch = 'case_' + str(cases)
        return getattr(self, switch, lambda: default)()

    def run(self):
        menu = ""
        while menu != 'quit':
            choice = self.view.menu_manage_club()
            menu = self.choice(choice)
            if menu == 'load':
                return 'load'
        return
