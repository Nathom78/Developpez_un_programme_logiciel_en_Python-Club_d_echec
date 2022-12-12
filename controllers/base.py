from models.players import Player, Players
from models.tournament import Tournaments, Tournament
from views.base import View
from typing import List


NUMBER_OF_PLAYERS = 8


class ControllerTournaments:

    def __init__(self):
        """a list of players, a tournament, some rounds"""
        # models
        self.players: List[Player] = []
        self.tournaments = Tournaments

        # views
        self.view = View

    def get_players(self):
        while len(self.players) < NUMBER_OF_PLAYERS:
            parameter = self.view.prompt_for_player()
            if not parameter:
                return
            player = Player(*parameter)
            self.players.append(player)

    def run(self):

        parameter = self.view.prompt_for_tournament()
        new_tournament = Tournament(*parameter)
        # ajouter un tournoi à la liste tournaments
        # voir save
        print(new_tournament)

        self.get_players()
        new_tournament['players'] = self.players

        Players.list_players = self.players
        print(Players.print_list_club())




