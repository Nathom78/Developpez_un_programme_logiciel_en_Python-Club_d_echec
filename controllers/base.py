from models.players import Player, PlayersId
from models.tournament import Tournaments, Tournament, Round
from typing import List
from time import strftime, sleep

from controllers.club_manage import ControllerMenu
from controllers.system_swiss import ControllerSwiss
from views.base import View

NUMBER_OF_PLAYERS = 8


class ControllerTournaments:

    load = 0
    fin = 0

    def __init__(self, view, controller_menu, method_calcul_round):
        """a list of players, a tournament, some rounds"""
        # models
        self.players: List[PlayersId] = []
        self.tournaments = Tournaments

        # views ## type View à effacer
        self.view: View = view

        # manage players' club ## type Controller à effacer
        self.menu: ControllerMenu = controller_menu

        # method calcul des rondes du tournoi ## type Controller à effacer
        self.method_calcul_round: ControllerSwiss = method_calcul_round()

    def get_players(self):
        """
        :return: list of NUMBER_OF_PLAYER IDs (self.players
        """
        PlayersId.load_all()
        list_player_id = PlayersId.players_IDs  # tous les joueurs du club
        while len(self.players) < NUMBER_OF_PLAYERS:
            # enlever de la liste à afficher, les joueurs deja dans le tournoi
            for id_player in self.players:
                try:
                    list_player_id.remove(id_player)
                except ValueError:
                    continue
            # preparer la liste des joueurs à afficher
            list_player = PlayersId.ids_to_dicts(list_player_id)
            text = ""
            for player in range(len(list_player)):
                text += f"\nJoueur {player + 1}:\n{list_player[player]}"
            # Demander via la view le numéro du joueur à ajouter
            self.view.clear_screen()
            number_in_list = self.view.make_list_player_from_db(text)
            # Voir si ne pas créer un nouveau joueur dans la base
            player_id = 0
            if number_in_list == 0:
                attribut_player = self.view.menu_manage_club_case_1()
                player = Player(*attribut_player)
                # enregistrer dans la base
                player_id = Player.create(player)
                PlayersId.players_IDs.append(player_id)
            # sinon ajouter le numéro ID indiqué à la liste des joueurs
            elif number_in_list > 0:
                player_id = list_player_id[number_in_list - 1]
            self.players.append(player_id)

    def menu_players_and_lists(self):
        return self.menu.run()

    def new_tournament_or_load(self):
        #
        choice = self.view.ask_start()
        tournament = Tournament
        if choice == 1:
            parameter = self.view.prompt_for_tournament()
            tournament = Tournament(*parameter)
        elif choice == 2:
            self.load = 1
            return 'load'

        return tournament

    def load_tournament(self):
        Tournaments.load_all()
        name_tournament = self.view.menu_manage_club_case_2_2_choice(
            Tournaments.list_tournament)
        if name_tournament == 0:
            return
        tournament = Tournament.load(name_tournament)
        self.players = tournament['players']
        # pour plus tard pour plusieurs tournois actifs, ajouter à la liste des tournois ou
        # le rendre unique
        self.tournaments.tournaments_actif = []
        self.tournaments.tournaments_actif.append(tournament)

    def run(self):
        new_tournament: Tournament
        self.view.clear_screen()
        # afficher le menu, afin d'ajouter un joueur au club ou autre
        load = self.menu_players_and_lists()
        if load == 'load':
            return
        self.view.clear_screen()
        # ajouter un tournoi à la liste des tournaments actif, dans le cas futur
        # où plusieurs tournois seront joués en même temps et stock dans la DB le nom
        if not self.tournaments.tournaments_actif:
            new_tournament = self.new_tournament_or_load()
            if new_tournament == 'load':
                return
            else:
                Tournaments.add_db_tournament(new_tournament)
        else:
            new_tournament = self.tournaments.tournaments_actif[-1]

        # afficher le menu, afin d'ajouter un joueur au club ou autre
        load = self.menu_players_and_lists()
        if load == 'load':
            return
        self.view.clear_screen()

        # Listes des joueurs
        if len(self.players) < 8:
            self.get_players()
        new_tournament.tournament_players(self.players)
        # ajouter le nom du tournoi à la liste des tournois joué par le joueur
        # et initialiser son score si le joueur n'était pas dans le tournoi
        list_players = PlayersId.ids_to_dicts(self.players)
        for player, player_id in zip(list_players, self.players):
            if_exist = False
            for player_tournament in player['tournaments']:
                if new_tournament['name'] == player_tournament[0]:
                    if_exist = True
            if not if_exist:
                player['tournaments'].append([new_tournament['name'], 0])
            player['score'] = 0
            player['opponents'] = []
            player.modify(player, player_id)

        # Détermination du numéro du round en cours
        nb_round_max = new_tournament['number_total_round']
        i = len(new_tournament['rounds'])
        if i == 0 or (i < nb_round_max and new_tournament['rounds'][i-1]['finish_time'] != ""):
            i += 1
        if i == nb_round_max and new_tournament['date_end'] != "":
            text = "Tournoi déja remplis"
            self.view.menu_manage_club_case_2_print(text)

        # round x:
        while new_tournament['date_end'] == "":
            round_x: Round
            round_x_couples_players = []

            # création du round s'il n'existe pas dans le tournoi
            if 0 < i <= nb_round_max and len(new_tournament['rounds']) < i:
                round_x = Round()
                round_x['name'] = f"Round {i}"

                # Listes des matchs
                round_x['list_matches'] = self.method_calcul_round.run(self.players, i)

                # Stockage du round dans le tournoi et sauvegarde du tournoi
                new_tournament['rounds'].append(round_x)
                new_tournament.save()
                text = "Tournoi sauvegardé"
                self.view.menu_manage_club_case_2_print(text)
                sleep(2)
                self.view.clear_screen()

            round_x = new_tournament['rounds'][i-1]

            # Stockage des couples de joueurs de chaque match
            for match in round_x['list_matches']:
                round_x_couples_players.append(match.match_players_ids_to_players())

            # Afin d'afficher les matchs
            self.view.print_match(round_x_couples_players, i)

            # remplissage des résultats du round tant que nécessaire
            while round_x['finish_time'] == "":
                # Proposition du menu
                choice = 0
                while not choice == 1:
                    choice = self.view.ask_resultat_or_menu()
                    if choice == 2:
                        load = self.menu_players_and_lists()
                        if load == 'load':
                            return
                    self.view.clear_screen()

                # Matchs
                m = 0
                for match, couple in zip(round_x['list_matches'], round_x_couples_players):
                    if len(round_x['list_results']) == m:
                        result_ok = False
                        while not result_ok:
                            result = self.view.input_match_result(couple, m, i)
                            # enregistrer le résultat du match
                            if result == 1:
                                couple[0]['score_last_match'] = 1
                                couple[1]['score_last_match'] = 0
                            if result == 2:
                                couple[0]['score_last_match'] = 0
                                couple[1]['score_last_match'] = 1
                            if result == 3:
                                couple[0]['score_last_match'] = 0.5
                                couple[1]['score_last_match'] = 0.5
                            if result == 4:
                                self.menu_players_and_lists()
                            else:
                                round_x['list_results'].append(result)
                                result_ok = True
                        # création du tuple resultat du match
                        match.match_result()
                        round_x['list_matches'][m] = match
                        # mise à jour des scores dans db des joueurs
                        for player, player_id in zip(couple, match['couple_players_id']):
                            player['score'] += player['score_last_match']
                            Player.modify(player, player_id)
                    m += 1

                # Cloture du round
                round_x['finish_time'] = strftime('%H:%M:%S')
                round_x['finish_date'] = strftime('%d/%m/%Y')

                # save tournament
                new_tournament['rounds'][i-1] = round_x
                # Si dernier round est finis
                if i == nb_round_max:
                    new_tournament['date_end'] = strftime('%d/%m/%Y')
                new_tournament.save()
                text = "Tournoi sauvegardé"
                self.view.menu_manage_club_case_2_print(text)
                sleep(2)
                self.view.clear_screen()
            i += 1

        text = f"Tournoi finis le {new_tournament['date_end']} à " \
               f"{new_tournament['rounds'][nb_round_max-1]['finish_date']}"
        self.view.menu_manage_club_case_2_print(text)
        self.fin = 1
