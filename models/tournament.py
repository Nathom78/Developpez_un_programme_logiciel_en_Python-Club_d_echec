from typing import List, Tuple
from time import strftime
from tinydb import TinyDB


class Tournaments(list):

    def __init__(self):
        super().__init__()
        self.tournaments: List[Tournament] = []

    def save_all(self):
        for element in self.tournaments:
            name = element['name']
            path = f'../database/tournaments.json'
            db = TinyDB(path)
            tournaments_table = db.table(name)  # pour les tournois regroupant tout
            tournaments_table.insert_multiple(self.tournaments)

    def load_all(self):
        pass


class Tournament(dict):
    """
    Chaque tournoi doit contenir au moins les informations suivantes :
    ●	Nom : (unique)
    ●	Lieu :
    ●	Date de création :
        ○	Jusqu'à présent, tous nos tournois sont des événements d'un jour,
            mais nous pourrions en organiser de plusieurs jours à l'avenir,
            ce qui devrait donc permettre de varier les dates.
    ●	Nombre de tours :
        ○	Réglez la valeur par défaut sur 4.
    ●	Tournées :
        ○	La liste des instances rondes.
    ●	Joueurs :
        ○	Liste des indices correspondant aux instances du joueur stockées en mémoire.
    ●	Contrôle du temps
        ○	C'est toujours un bullet, un blitz ou un coup rapide.
    ●	Description
        ○	Les remarques générales du directeur du tournoi vont ici.
    """

    def __init__(self, name, place, type_game_time, number_total_round=4,
                 description="", date=strftime('%d/%m/%Y')):
        super().__init__()
        self['name'] = name
        self['Rounds']: List[Round] = []
        self['place'] = place
        self['date_creation'] = date
        self['date_end'] = ""
        self['number_total_round'] = number_total_round
        self['players'] = []
        self['type_game_time'] = type_game_time
        self['description'] = description

    def __str__(self):
        return f"\nLe tournoi {self['name']} de {self['place']} commencé le " \
               f"{self['date_creation']}\n" \
               f"avec {self['number_total_round']} ronde, le type du jeux est " \
               f" {self['type_game_time']}\n" \
               f"liste des rounds : {self['Rounds']}\n" \
               f"liste des joueurs : {self['players']}"

    def tournament_players(self, list_player):
        self['players'] = list_player


class Round(list):
    """
    Actuellement, nous appelons nos tours "Round 1", "Round 2", etc.
    Elle doit également contenir un champ Date et heure de début
    et un champ Date et heure de fin, qui doivent tous deux être
    automatiquement remplis lorsque l'utilisateur crée un tour et le marque comme terminé.
    (Au moment de la fin du tour, le score du joueur sera mis à jour.)
    Et contient la liste des matches.
    """

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.starting_date = strftime('%d/%m/%Y')
        self.starting_time = strftime('%H:%M:%S')
        self.finish_time = ""
        self.list_matches_finishing = None
        self.couples_players = []
        self.list_matches = []

    def append(self, object: object):
        """Append a match. """
        if not isinstance(object, Match):
            return ValueError("Tour mal configuré")
        return super().append(object)


class Match:
    """
    Création d'un tuple contenant deux listes, chacune contenant deux éléments :
    une référence à une instance de joueur et un score
    """

    resultat_match: Tuple = None

    def __init__(self, couple_players):
        self.couple_players = couple_players

    def match_resultat(self):
        player1 = self.couple_players[0]
        player2 = self.couple_players[1]
        player1_resultat = player1['score_last_match']
        player2_resultat = player2['score_last_match']
        self.resultat_match = ([player1, player1_resultat], [player2, player2_resultat])
        return self.resultat_match
