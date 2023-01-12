import string
from tinydb import TinyDB

#  Path to database Tiny
PATH = 'database/tournaments.json'
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
        'score_last_match' : 0
        'tournaments': [["T1", score], ["T3", score]]
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
        self['tournaments'] = []
        self['opponents'] = []
        self['score_last_match'] = 0

    def __str__(self):
        tournament_played = ""
        for tournament in self['tournaments']:
            tournament_played += f"Tournoi {tournament[0]}: {tournament[1]} pt(s), "
        return f"- family name : {self['family_name']}, " \
               f"first name : {self['first_name']},\n" \
               f"- date of birth : {self['date_of_birth']}, " \
               f"sex : {self['sex']},\n" \
               f"- ranking : {self['ranking']}, " \
               f"score : {self['score']},\n" \
               f"- tournaments played : {tournament_played}.\n"

    @staticmethod
    def correspond_player(player_temp: dict):
        """ Test and put data from BD, in instance of Player"""
        player = {}
        try:
            player = Player(player_temp['family_name'], player_temp['first_name'],
                            player_temp['date_of_birth'], player_temp['sex'],
                            player_temp['ranking'], player_temp['score'])
            player['tournaments'] = player_temp['tournaments']
            player['opponents'] = player_temp['opponents']
            player['score_last_match'] = player_temp['score_last_match']

        except (KeyError, TypeError,):
            print(f"Base de donnée incorrect pour le joueur {player_temp}")
        finally:
            if not isinstance(player, Player):
                raise ValueError("Joueur mal défini!")
        return player

    @staticmethod
    def create(player):
        db = TinyDB(PATH)
        players_table = db.table(NAME_PLAYERS_TABLE)
        if not isinstance(player, Player):
            raise ValueError("Joueur mal défini!")
        return players_table.insert(player)

    @staticmethod
    def modify(player_modify, player_id):
        """
        Update in DB, the player with ID player_id.
        :param player_modify:
        :param player_id:
        :return: ok or error
        """
        try:
            if not isinstance(player_modify, Player):
                player_modify = Player.correspond_player(player_modify)
            if isinstance(player_modify, Player):
                db = TinyDB(PATH)
                players_table = db.table(NAME_PLAYERS_TABLE)
                doc_id_return = players_table.update(player_modify, doc_ids=[player_id])
                if doc_id_return == player_id:
                    return "ok"
        except ValueError as error:
            print("Uh oh, unexpected error occurred!")
            raise error


class PlayersId:
    """
    a player ID give a player dict, the players with ID is écolo
    avec une list des ID des players du club
    """
    players_IDs = []

    @classmethod
    def print_list_player_sort_abc(cls, list_players_id):  # à faire mieux et ménage
        list_players = cls.ids_to_dicts(list_players_id)
        list_sort = sorted(list_players, key=lambda player: player['family_name'])
        text = ""
        for x in range(len(list_sort)):
            text += f"Joueur {x + 1}:\n{list_sort[x]}"
        return text

    @classmethod
    def print_list_player_sort_rank(cls, list_players_id):  # à faire mieux et ménage
        players = cls.ids_to_dicts(list_players_id)

        players_sorted = sorted(players, key=lambda player: player['ranking'],
                                reverse=True)
        text = ""
        for x in range(len(players_sorted)):
            text += f"Joueur {x + 1}:\n{players_sorted[x]}"
        return text

    @classmethod
    def ids_to_dicts(cls, list_players_id):
        """ Liste de joueur ID, retourne une liste de Player(dict)"""
        list_players = []
        player = {}
        for player_id in list_players_id:
            dict_player = cls.id_to_dict(player_id)
            try:
                player = Player.correspond_player(dict_player)
            except ValueError:
                print(f"Base de donnée incorrect pour le joueur {player_id}")
            finally:
                list_players.append(player)
        return list_players

    @classmethod
    def print_list_club(cls, sort=0):
        """ Retourne une liste prête à être affiché, de tous les joueurs
        sort = 1 : rangé par ordre alphabétique
        sort = 2 : rangé par score
        sort = 0 : ordre de la base
        """
        cls.load_all()
        text = ""
        if sort == 1:
            text = cls.print_list_player_sort_abc(cls.players_IDs)
        elif sort == 2:
            text = cls.print_list_player_sort_rank(cls.players_IDs)
        else:
            list_player = cls.ids_to_dicts(cls.players_IDs)
            for player in range(len(list_player)):
                text += f"Joueur {player + 1}:\n{list_player[player]}"
        return text

    @classmethod
    def load_all(cls):
        """
        :return: nothing
        But a list of id's players in DB,
        stocked in class attribut Player_IDs
        """
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
        players_table = db.table(NAME_PLAYERS_TABLE)
        return players_table.get(doc_id=player_id)


# for i in range(8):
#    Player.create(Player(f"Lebon{i + 1}", "Paul", "21/06/1969", "M", 15 + i))

# adidas = PlayersId()
# adidas.load_all()
# tom = adidas.players_IDs
# print(adidas.players_IDs)
# adidas.print_list_club(0)
# print(adidas.id_to_dict(3))
# print((Player.correspond_player(Player("Lebon", "Paul", "21/06/1969", "M", 15))))
