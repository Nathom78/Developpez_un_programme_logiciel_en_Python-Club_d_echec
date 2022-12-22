import views.base
from models.players import Player, PlayersId
from models.tournament import Tournaments, Tournament
from controllers.club_manage import ControllerMenuPlayersLists
from typing import List

NUMBER_OF_PLAYERS = 8


class ControllerTournaments:

    def __init__(self, view, controller_menu, method_calcul_round):
        """a list of players, a tournament, some rounds"""
        # models
        self.players: List[PlayersId] = []
        self.tournaments = Tournaments

        # views
        self.view = view

        # manage players' club
        self.menu: ControllerMenuPlayersLists = controller_menu

        # method calcul ronde
        self.method_calcul_round = method_calcul_round

    def get_players(self):
        """
        :return: list of NUMBER_OF_PLAYER IDs
        """
        PlayersId.load_all()
        list_player_id = PlayersId.players_IDs
        while len(self.players) <= NUMBER_OF_PLAYERS:
            # enlever de la liste à afficher, les joueurs deja dans le tournoi
            for id_player in self.players:
                list_player_id.remove(id_player)

            self.view.clear_screen()
            list_player = PlayersId.ids_to_dicts(list_player_id)
            text = ""
            for player in range(len(list_player)):
                text = f"Joueur {player + 1}:\n{list_player[player]}"
            number_in_list = self.view.make_list_player_from_db(text)
            player_id = list_player_id[number_in_list - 1]
            self.players.append(player_id)

    def menu_players_and_lists(self):
        return self.menu.run()

    def new_tournament_or_load(self):
        choice = self.view.ask_start()
        tournament = Tournament
        if choice == 1:
            parameter = self.view.prompt_for_tournament()
            tournament = Tournament(*parameter)
        elif choice == 2:
            Tournaments.load_all()
            name_tournament = self.view.menu_manage_club_case_2_2_choice(
                Tournaments.list_tournament)
            tournament = Tournament.load(name_tournament)
            self.players = tournament['players']
        return tournament

    def run(self):

        new_tournament = self.new_tournament_or_load()
        # ajouter un tournoi à la liste des tournaments actif, dans le cas futur
        # plusieurs tournois joué en même temps
        Tournaments.tournaments_actif.append(new_tournament)
        # afficher le menu, afin d'ajouter un joueur ou consulter
        self.menu_players_and_lists()
        # Listes des joueurs
        if len(self.players) < 8:
            self.get_players()
            new_tournament['players'] = self.players

