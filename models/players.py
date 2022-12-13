import string
from typing import List
from tinydb import TinyDB

#  Path to database Tiny
PATH = f'../database/tournaments.json'
NAME_PLAYERS_TABLE = 'players'


class Player(dict):
    """ Créer un joueur sous forme de dictionnaire:
    Player(family_name, first_name, date_of_birth, sex,ranking) ->
    joueur Paul={
        'family_name': "Lebon",
        'first_name': "Paul",
        'date_of_birth': "21/06/1969",
        'sex': "M",  # (M ou F)
        'ranking_Elo': 12
        'score:': 0

        }
    """

    def __init__(self, family_name, first_name, date_of_birth, sex, ranking, score=0):
        """Initialise un joueur"""
        super().__init__()
        self['family_name'] = str.upper(family_name)
        self['first_name'] = string.capwords(first_name)
        self['date_of_birth'] = date_of_birth
        self['sex'] = sex
        self['ranking'] = ranking
        self['score'] = score
        self['score_last_match'] = 0
        self['Tournaments'] = []

    def __str__(self):
        return f"- family name : {self['family_name']}, " \
               f"first name : {self['first_name']},\n" \
               f"- date of birth : {self['date_of_birth']}, " \
               f"sex : {self['sex']},\n" \
               f"- ranking : {self['ranking']}, " \
               f"score : {self['score']},\n" \
               f"score of the last match :{self['score_last_match']}.\n"

    def modify(self):
        pass


class PlayerId:
    """
    a player ID give a player dict, the players with ID is écolo

    Pour l'instant je ne sais pas si j'aurais besoin d'instance de PlayerId sinon faire des
    @classmethod
    """

    def __init__(self):  # à virer
        self.players = Players()

    def print_list_player_sort_abc(self, list_players_id):  # à faire mieux et ménage
        list_players = self.ids_to_dicts(list_players_id)
        list_sort = sorted(list_players, key=lambda player: player['family_name'])
        for x in range(len(list_sort)):
            print(f"Joueur {x + 1}:\n{list_sort[x]}")

    def print_list_player_sort_rank(self, list_players_id):  # à faire mieux et ménage
        players = self.ids_to_dicts(list_players_id)

        players_sorted = sorted(players, key=lambda player: player['ranking'],
                                reverse=True)
        for x in range(len(players_sorted)):
            print(f"Joueur {x + 1}:\n{players_sorted[x]}")

    @staticmethod
    def id_to_dict(player_id):
        """ Joueur avec ID, retourne un document de la BD valide ou pas"""
        db = TinyDB(PATH)
        players_table = db.table('players')
        return players_table.get(doc_id=player_id)

    def ids_to_dicts(self, list_players_id):  # à faire mieux et ménage Players.list_player
        """ Liste de joueur ID, retourne une liste de Player(dict)"""
        for player_id in list_players_id:
            dict_player = self.id_to_dict(player_id)
            try:
                player_temp = Player(dict_player['family_name'], dict_player['first_name'],
                                     dict_player['date_of_birth'], dict_player['sex'],
                                     dict_player['ranking'], dict_player['score'])
            except (KeyError, TypeError,):
                print(f"Base de donnée incorrect pour le joueur {player_id}")
            else:
                self.players.append(player_temp)
        return self.players


class Players(list):
    """ Tout ce qui concernent tous les players de tous les tournois
    - ajouter un player à la liste class.list_player (add)
    - sauver dans la base de donnée tous les players class.save_all(nom du tournoi)
    - afficher la liste class.list_player (print_list)
    """

    list_players: List[Player] = []  # voir List ID ou juste un Player

    def __init__(self):
        super().__init__()

    def sort_abc(self):
        pass

    def append(self, player):
        if not isinstance(player, Player):
            return ValueError("Joueur mal défini!")
        return super().append(player)

    @classmethod
    def add(cls, player):
        if not isinstance(player, Player):
            return ValueError("Joueur mal défini!")  # voir erreur ou faire try except
        cls.list_players.append(player)

    @classmethod
    def save_all(cls):  # a effacer par save one
        db = TinyDB(PATH)
        players_table = db.table(NAME_PLAYERS_TABLE)
        players_table.truncate()  # clear the table first
        players_table.insert_multiple(cls.list_players)

    @classmethod
    def load_all(cls):  # voir remplacer par une liste des IDs de la BD
        db = TinyDB(PATH)
        players_table = db.table(NAME_PLAYERS_TABLE)
        list_temp = players_table.all()
        cls.list_players = []
        for document in list_temp:
            try:
                cls.add(document)
            except ValueError:
                print(ValueError)

    @classmethod
    def print_list_club(cls):
        """ Retourne une liste prête à être affiché, de tous les joueurs """
        list_tom = ""
        for player in range(len(cls.list_players)):
            list_tom = list_tom + f"Joueur {player + 1}:\n{cls.list_players[player]}\n"
        return list_tom

    @classmethod
    def modify_player(cls):
        pass


adidas = PlayerId()
print(adidas.id_to_dict(2))
tom = adidas.players
print(tom)
adidas.print_list_player_sort_rank([1, 2, 3, 4, 5, 6, 7, 8])


"""
tournament = Players
for i in range(8):
    tournament.list_players.append(Player(f"Lebon{i + 1}", "Paul", "21/06/1969", "M", 15))

print(tournament.print_list_club())
tournament.save_all('tournament')
"""
