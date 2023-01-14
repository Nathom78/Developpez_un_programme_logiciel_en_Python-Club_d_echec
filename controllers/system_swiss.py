from models.players import PlayersId
from models.tournament import Match
from typing import List


class ControllerSwiss:
    """
    :return: List de match
    """

    def __init__(self):
        self.list_match: List[Match] = []
        self.players = []

    def run(self, player_tournament, nb_round):
        self.players = player_tournament
        opponents_possible = []

        if nb_round == 1:
            self.list_match = []
            # création de deux listes de joueurs classés par rang
            list_players_sort = PlayersId.sort_rank(self.players)
            list_ids_sort = []
            for player in list_players_sort:
                # transforme la liste triée des joueurs, en liste d'Ids de joueurs
                print(player['family_name'], player['first_name'])
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
                match.add_opponents()
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
            for player in list_players_sort:
                opponents_possible.append(list_ids_sort)
                unwanted_opponents.append(list_ids_sort[x])
                unwanted_opponents.extend(player['opponents'])
                opponents_possible[x] = tuple(ele for ele in opponents_possible[x] if ele not in
                                              unwanted_opponents)
                unwanted_opponents = []
                x += 1

            # liste des joueurs triés encore en liste
            list_player_opponent = list(zip(list_ids_sort, opponents_possible))

            # créations des matchs
            while len(self.list_match) < nb_match:
                player1_id = list_player_opponent[0][0]
                for player2_id, opponents_possible in list_player_opponent[1:]:
                    if player1_id in opponents_possible:
                        match = Match([player1_id, player2_id])
                        match.add_opponents()
                        self.list_match.append(match)
                        del list_player_opponent[0]
                        list_player_opponent.remove((player2_id, opponents_possible))
                        break

        return self.list_match
