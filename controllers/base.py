from models.players import Player, PlayersId
from models.tournament import Tournaments, Tournament, Round, RoundSerialized, Match
from typing import List
from time import strftime

from controllers.club_manage import ControllerMenu
from controllers.system_swiss import ControllerSwiss
from views.base import View


NUMBER_OF_PLAYERS = 8


class ControllerTournaments:

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
        self.method_calcul_round: ControllerSwiss = method_calcul_round

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
                player_id = Player.create(player)
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

    def load_tournament(self):
        Tournaments.load_all()
        name_tournament = self.view.menu_manage_club_case_2_2_choice(
            Tournaments.list_tournament)
        tournament = Tournament.load(name_tournament)

        self.tournaments.tournaments_actif.append(tournament)
        self.run()

    def run(self):
        #
        new_tournament = self.new_tournament_or_load()
        # ajouter un tournoi à la liste des tournaments actif, dans le cas futur
        # où plusieurs tournois seront joués en même temps et stock dans la DB le nom
        Tournaments.add_db_tournament(new_tournament)

        # afficher le menu, afin d'ajouter un joueur au club ou autre
        self.menu_players_and_lists()
        # Listes des joueurs
        if len(self.players) < 8:
            self.get_players()
        new_tournament.tournament_players(self.players)
        # ajouter le nom du tournoi à la liste des tournois joué par le joueur
        # et initialiser son score si le joueur n'était pas dans le tournoi
        list_players = PlayersId.ids_to_dicts(self.players)
        for player, player_id in zip(list_players, self.players):
            if new_tournament['name'] not in player['tournaments']:
                player['tournaments'].append(new_tournament['name'])
                player['score'] = 0
                player.modify(player, player_id)

        # round 1:
        round1: Round
        round1_couples_players = []
        i = 1  # numéro du round

        # création du round s'il n'existe pas dans le tournoi
        if not isinstance(new_tournament['rounds'][i - 1], Round):
            round1 = Round()
            round1.name = "round1"
            # Listes des matchs
            round1.list_matches = self.method_calcul_round.run(self.players)
            # Stockage des couples de joueurs de chaque match dans le round
            for match in round1.list_matches:  # Peut-être supprimer round couples players
                round1_couples_players.append(match.match_players_ids_to_players())
            # Afin d'afficher les matchs
            self.view.print_match(round1_couples_players, i)
            # Stockage du round dans le tournoi et sauvegarde (création) du tournoi
            round1_serialized = RoundSerialized().ready_to_save(round1)
            new_tournament['rounds'].append(round1_serialized)
            new_tournament.save()

        # Proposition du menu
        choice = 0
        while not choice == 1:
            choice = self.view.ask_resultat_or_menu()

        # remplissage du round si nécessaire
        round1 = new_tournament['rounds'][i - 1]
        while round1.finish_time != "":
            m = 0
            for match, couple in zip(round1.list_matches, round1_couples_players):
                if round1.list_results[m] is None:
                    result = self.view.input_match_result(couple, m, i)
                    round1.list_results.append(result)
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
                    # création du tuple resultat du match
                    match.match_result()
                    # mise à jour dans db des joueurs
                    for player, player_id in zip(couple, match.couple_players_id):
                        player['score'] += player['score_last_match']
                        Player.modify(player, player_id)
            # Cloture du round
            round1.finish_time = strftime('%H:%M:%S')
            round1.finish_date = strftime('%d/%m/%Y')
            # save tournament
            round1_serialized = RoundSerialized().ready_to_save(round1)
            new_tournament['rounds'][i - 1] = round1_serialized
            new_tournament.save()
            text = "Tournoi sauvegardé"
            self.view.menu_manage_club_case_2_print(text)



