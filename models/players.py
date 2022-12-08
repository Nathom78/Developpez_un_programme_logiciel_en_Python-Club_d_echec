import string
from typing import List
from tinydb import TinyDB


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
        self['family_name'] = string.capwords(family_name)
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


class Players(list):
    """ Tout ce qui concernent tous les players de tous les tournois
    - ajouter un player à la liste class.list_player (append)
    - sauver dans la base de donnée tous les players class.save_all(nom du tournoi)
    - afficher la liste class.list_player (print_list)
    """

    # attribut de class : nom de la liste des players dans le fichier
    # de la base de donnée stocké ./database/db.json
    list_players: List[Player] = []

    def __init__(self):
        super().__init__()

    @classmethod
    def append(cls, player):
        if not isinstance(player, Player):
            return ValueError("Joueur mal défini!")
        return super().append(player)

    @classmethod
    def save_all(cls, name: string):
        path = f'../database/{name}.json'
        db = TinyDB(path)
        players_table = db.table('players')
        players_table.truncate()  # clear the table first
        players_table.insert_multiple(cls.list_players)

    def load_all(self):
        pass

    @classmethod
    def print_list_club(cls):
        list_tom = ""
        for player in range(len(cls.list_players)):
            list_tom = list_tom + f"Joueur {player+1}:\n{cls.list_players[player]}\n"
        return list_tom


"""
tournament = Players
for i in range(8):
    tournament.list_players.append(Player(f"Lebon{i + 1}", "Paul", "21/06/1969", "M", 15))

print(tournament.print_list_club())
tournament.save_all('tournament')
"""

