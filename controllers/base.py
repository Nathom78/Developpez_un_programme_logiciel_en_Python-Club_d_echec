from models.players import Player, PlayersId
from models.tournament import Tournaments, Tournament
from typing import List

NUMBER_OF_PLAYERS = 8


class ControllerTournaments:

    def __init__(self, view, controller_menu, method_calcul_round):
        """a list of players, a tournament, some rounds"""
        # models
        self.players: List[Player] = []
        self.tournaments = Tournaments

        # views
        self.view = view

        # manage players' club
        self.menu = controller_menu.run()

        # method calcul ronde
        self.method_calcul_round = method_calcul_round

    def get_players(self):
        while len(self.players) < NUMBER_OF_PLAYERS:
            parameter = self.view.prompt_for_player()
            if not parameter:
                return
            player = Player(*parameter)  # à remplacer avec ID du player
            self.players.append(player)

    def menu_players_and_lists(self):
        return self.menu

    def run(self):

        parameter = self.view.prompt_for_tournament()
        new_tournament = Tournament(*parameter)
        # ajouter un tournoi à la liste tournaments
        # voir save

        print(new_tournament)

        self.get_players()
        new_tournament['players'] = self.players
