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
        self['Tournaments'] = []

    def __str__(self):
        return f"- family name : {self['family_name']}, " \
               f"first name : {self['first_name']},\n" \
               f"- date of birth : {self['date_of_birth']}, " \
               f"sex : {self['sex']},\n" \
               f"- ranking : {self['ranking']}, " \
               f"score : {self['score']}.\n"

    def modify(self):
        pass

    @staticmethod
    def correspond_player(player_temp: dict):
        """ Test and put data from BD, in instance of Player"""
        player = {}
        try:
            player = Player(player_temp['family_name'], player_temp['first_name'],
                            player_temp['date_of_birth'], player_temp['sex'],
                            player_temp['ranking'], player_temp['score'])
        except(KeyError, TypeError,):
            print(f"Base de donnée incorrect pour le joueur {player_temp}")
        finally:
            if not isinstance(player, Player):
                raise ValueError("Joueur mal défini!")
        return player

    @staticmethod
    def save(player):
        db = TinyDB(PATH)
        players_table = db.table(NAME_PLAYERS_TABLE)
        if not isinstance(player, Player):
            return ValueError("Joueur mal défini!")
        players_table.insert(player)


class PlayersId:
    """
    a player ID give a player dict, the players with ID is écolo
    avec une list des ID des players du club

    Pour l'instant je ne sais pas si j'aurais besoin d'instance de PlayerId sinon faire des
    @classmethod
    """
    players_IDs = []

    @classmethod
    def print_list_player_sort_abc(cls, list_players_id):  # à faire mieux et ménage
        list_players = cls.ids_to_dicts(list_players_id)
        list_sort = sorted(list_players, key=lambda player: player['family_name'])
        for x in range(len(list_sort)):
            print(f"Joueur {x + 1}:\n{list_sort[x]}")

    @classmethod
    def print_list_player_sort_rank(cls, list_players_id):  # à faire mieux et ménage
        players = cls.ids_to_dicts(list_players_id)

        players_sorted = sorted(players, key=lambda player: player['ranking'],
                                reverse=True)
        for x in range(len(players_sorted)):
            print(f"Joueur {x + 1}:\n{players_sorted[x]}")

    @classmethod
    def ids_to_dicts(cls, list_players_id):  # à faire mieux et ménage Players.list_player
        """ Liste de joueur ID, retourne une liste de Player(dict)"""
        list_player = []
        player = {}
        for player_id in list_players_id:
            dict_player = cls.id_to_dict(player_id)
            try:
                player = Player.correspond_player(dict_player)
            except ValueError:
                print(f"Base de donnée incorrect pour le joueur {player_id}")
            finally:
                list_player.append(player)
        return list_player

    @classmethod
    def print_list_club(cls, sort=0):
        """ Retourne une liste prête à être affiché, de tous les joueurs
        sort = 1 : rangé par ordre alphabétique
        sort = 2 : rangé par score
        sort = 0 : ordre de la base
        """
        cls.load_all()
        if sort == 1:
            cls.print_list_player_sort_abc(cls.players_IDs)
        elif sort == 2:
            cls.print_list_player_sort_rank(cls.players_IDs)
        else:
            list_player = cls.ids_to_dicts(cls.players_IDs)
            for player in range(len(list_player)):
                print(f"Joueur {player + 1}:\n{list_player[player]}")

    @classmethod
    def load_all(cls):
        # voir remplacer par une liste des IDs de la BD
        db = TinyDB(PATH)
        players_table = db.table(NAME_PLAYERS_TABLE)
        list_temp = players_table.all()
        cls.players_IDs = []
        for document in list_temp:
            try:
                Player.correspond_player(document)
            except ValueError:
                print(ValueError)
            finally:
                cls.players_IDs.append(document.doc_id)

    @staticmethod
    def id_to_dict(player_id):
        """ Joueur avec ID, retourne un document de la BD valide ou pas"""
        db = TinyDB(PATH)
        players_table = db.table('players')
        return players_table.get(doc_id=player_id)


# for i in range(8):
#    Player.save(Player(f"Lebon{i + 1}", "Paul", "21/06/1969", "M", 15 + i))

# adidas = PlayersId()
# adidas.load_all()
# tom = adidas.players_IDs
# print(adidas.players_IDs)
# adidas.print_list_club(0)
# print(adidas.id_to_dict(3))
# print((Player.correspond_player(Player("Lebon", "Paul", "21/06/1969", "M", 15))))
