import string


class Player:
    """ Créer un joueur sous forme de dictionnaire:
    Paul={
        'family_name': "Lebon",
        'first_name': "Paul",
        'date_of_birth': "21/06/1969",
        'sex': "M",  # (M ou F)
        'ranking': 12
        }

    """
    def __init__(self, family_name, first_name, date_of_birth, sex, ranking=0):
        self.family_name = string.capwords(family_name)
        self.first_name = string.capwords(first_name)
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.ranking = ranking

    def add_to_list(self):
        pass


class ListPlayers:
    pass
