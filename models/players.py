import string
from typing import List
from tinydb import TinyDB

db = TinyDB('../database/db.json')


class Player(dict):
    """ Créer un joueur sous forme de dictionnaire:
    Player(family_name, first_name, date_of_birth, sex,ranking) ->
    joueur Paul={
        'family_name': "Lebon",
        'first_name': "Paul",
        'date_of_birth': "21/06/1969",
        'sex': "M",  # (M ou F)
        'ranking': 12
        }
    """

    def __init__(self, family_name, first_name, date_of_birth, sex, ranking=0):
        """Initialise un joueur"""
        super().__init__()
        self['family_name'] = string.capwords(family_name)
        self['first_name'] = string.capwords(first_name)
        self['date_of_birth'] = date_of_birth
        self['sex'] = sex
        self['ranking'] = ranking

    def __str__(self):
        return f"Joueur {self['first_name']}:\n" \
               f"- family name : {self['family_name']}\n" \
               f"- first name : {self['first_name']}\n" \
               f"- date of birth : {self['date_of_birth']}\n" \
               f"- sex : {self['sex']}\n" \
               f"- ranking : {self['ranking']}\n"

    def modify(self):
        pass


class Players(list):
    """

    """

    # attribut de class : nom de la liste des players dans le fichier
    # de la base de donnée stocké ./database/db.json
    players_table = db.table('players')

    def __init__(self, list_players):
        super().__init__()
        self.list_players: List[Player]
        self.save_all(list_players)

    def append(self, player):
        if not isinstance(player, Player):
            return ValueError("Joueur mal défini!")
        return super().append(player)

    def save_all(self, list_players):

        self.players_table.truncate()  # clear the table first
        self.players_table.insert_multiple(list_players)

    def load_all(self):
        pass


list_players_test = []
for i in range(8):
    list_players_test.append(Player("Lebon", "Paul", "21/06/1969", "M", 15))
Players().save_all(list_players_test)

