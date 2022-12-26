from views.base import View
from models.players import Player, PlayersId
from models.tournament import Tournaments, Tournament, Round, Match
from controllers.club_manage import ControllerMenuPlayersLists
from controllers.system_swiss import ControllerSwiss
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

        # manage players' club ## type Controller à effacer
        self.menu:ControllerMenuPlayersLists  = controller_menu

        # method calcul ronde  ## type Controller à effacer
        self.method_calcul_round:ControllerSwiss = method_calcul_round

    def get_players(self):
        """
        :return: list of NUMBER_OF_PLAYER IDs (self.players
        """
        PlayersId.load_all()
        list_player_id = PlayersId.players_IDs  # tous les joueurs du club
        while len(self.players) <= NUMBER_OF_PLAYERS:
            # enlever de la liste à afficher, les joueurs deja dans le tournoi
            for id_player in self.players:
                list_player_id.remove(id_player)
            # preparer la liste des joueurs à afficher
            list_player = PlayersId.ids_to_dicts(list_player_id)
            text = ""
            for player in range(len(list_player)):
                text = f"Joueur {player + 1}:\n{list_player[player]}"
            # Demander via la view le numéro du joueur à ajouter
            number_in_list = self.view.make_list_player_from_db(text)
            # Voir si ne pas créer un nouveau joueur dans la base
            player_id = 0
            if number_in_list == 0:
                attribut_player = self.view.menu_manage_club_case_1()
                player = Player(*attribut_player)
                # enregistrer dans la base
                player_id = Player.save(player)
                PlayersId.players_IDs.append(player_id)
            # sinon ajouter le numéro ID indiqué à la liste des joueurs
            elif number_in_list > 0:
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
        #
        new_tournament = Tournament
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

        # round 1:
        if not isinstance(new_tournament['rounds'][0], Round):
            i = 1
            round1 = Round(self.players)
            round1.name = "round1"
            round1.list_matches = self.method_calcul_round.run()
            match_players = []
            for match in round1.list_matches:
                match_players.append(match.match_players_ids_to_players())

            results = self.view.print_match(match_players, i)
            # enregistrer résultat du match et fin du round
            for result in results:  #  zip result et match -> round -> tournament











