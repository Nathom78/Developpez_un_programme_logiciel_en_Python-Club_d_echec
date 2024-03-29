from models.players import PlayersId
from models.tournament import Match, Tournament
from typing import List
from random import choice
from datetime import datetime, timedelta


class ControllerSwiss:
    """
    :return: List de match
    """

    def __init__(self):
        self.list_match: List[Match] = []
        self.players = []

    def run(self, player_tournament, tournament: Tournament, nb_round):
        self.players = player_tournament
        opponents_possible = []

        if nb_round == 1:
            self.list_match = []
            # création de deux listes de joueurs classés par rang
            list_players_sort = PlayersId.sort_rank(self.players)
            list_ids_sort = []
            for player in list_players_sort:
                # transforme la liste triée des joueurs, en liste d'Ids de joueurs
                list_ids_sort.append(PlayersId.get_id(player['family_name'], player['first_name']))
            nb_player = len(list_ids_sort)
            if nb_player % 2 != 0:
                raise Exception("Nombre de joueur impair")
            nb_half = int(nb_player / 2)

            players_sup = list_ids_sort[:nb_half]
            players_inf = list_ids_sort[nb_half:]

            # création des couples et Match
            for i in range(nb_half):
                match = Match([players_sup[i], players_inf[i]])
                tournament.add_opponent(players_sup[i], players_inf[i])
                self.list_match.append(match)

        if nb_round > 1:
            self.list_match = []
            list_players_sort = PlayersId.sort_score(self.players)
            list_ids_sort = []
            for player in list_players_sort:
                # transforme la liste triée des joueurs, en liste d'Ids de joueurs

                list_ids_sort.append(PlayersId.get_id(player['family_name'], player['first_name']))

            # détermination du nombre de match
            nb_players = len(list_ids_sort)
            if nb_players % 2 != 0:
                raise Exception("Nombre de joueur impair")
            nb_match = int(nb_players / 2)

            # tableau des adversaires disponibles pour chaque joueur
            x = 0
            unwanted_opponents = []

            for player_id in list_ids_sort:
                opponents_possible.append(list_ids_sort)
                unwanted_opponents.append(list_ids_sort[x])
                key = str(player_id)
                unwanted_opponents.extend(tournament['opponents'][key])

                opponents_possible[x] = tuple(ele for ele in opponents_possible[x] if ele not in
                                              unwanted_opponents)
                unwanted_opponents = []
                x += 1

            # liste des joueurs triés encore en liste
            list_player_opponent = list(zip(list_ids_sort, opponents_possible))

            # créations des matchs
            time = datetime.now()
            wtd = time + timedelta(seconds=10)
            while len(self.list_match) < nb_match:
                # prendre le premier de la liste pour le joueur 1
                player1_id = list_player_opponent[0][0]
                # Et essayer les suivants pour le joueur 2
                for player2_id, opponents_possible in list_player_opponent[1:]:
                    if player1_id in opponents_possible:
                        match = Match([player1_id, player2_id])
                        tournament.add_opponent(player1_id, player2_id)
                        self.list_match.append(match)
                        # enleve le premier joueur
                        del list_player_opponent[0]
                        # enleve le deuxième joueur
                        list_player_opponent.remove((player2_id, opponents_possible))
                        break
                now = datetime.now()
                # faire plus propre en rajoutant un for du nb_match, et sinon effacer les matchs,
                # refaire list_player_opponent et jusqu' refaire opponents possible
                if now > wtd:
                    break

        return self.list_match

    @staticmethod
    def color(nb_match):
        list_color = []
        list_choice = ['blanc', 'noir']
        for x in range(nb_match):
            color = choice(list_choice)
            list_color.append(color)
        return list_color
