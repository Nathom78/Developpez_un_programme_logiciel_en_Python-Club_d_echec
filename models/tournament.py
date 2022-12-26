from typing import List, Tuple
from time import strftime
from tinydb import TinyDB
from models.players import PlayersId

PATH = '../database/tournaments.json'
NAME_PLAYERS_TABLE = 'players'
NAME_TOURNAMENTS_TABLE = 'Tournaments'


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
        self['rounds']: List[Round] = []
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
               f"liste des rounds : {self['rounds']}\n" \
               f"liste des joueurs : {self['players']}"

    def tournament_players(self, list_player):
        self['players'] = list_player

    def save(self):
        name = self['name']
        db = TinyDB(PATH)
        tournaments_table = db.table(name)  # pour le tournoi regroupant tout
        tournaments_table.insert(self)

    @staticmethod
    def correspond_tournament(tournament_temp: dict):
        """ Test and put data from BD, in instance of Tournament"""
        tournament = {}
        try:
            tournament = Tournament(tournament_temp['name'],
                                    tournament_temp['place'],
                                    tournament_temp['type_game_time'],
                                    tournament_temp['number_total_round'],
                                    tournament_temp['description'],
                                    tournament_temp['date_creation'])
            tournament['date_end'] = tournament_temp['date_end']
            tournament['players'] = tournament_temp['players']
            tournament['rounds'] = tournament_temp['rounds']
        except(KeyError, TypeError,):
            print(f"Base de donnée incorrect pour le joueur {tournament_temp}")
        finally:
            if not isinstance(tournament, Tournament):
                raise ValueError("tournoi mal défini!")
        return tournament

    @staticmethod
    def load(name):
        """
        :param name: #name of the tournament to load
        :return: an instance of the tournament
        """
        db = TinyDB(PATH)
        tournament_table = db.table(name)  # pour le tournoi regroupant tout
        tournament_db = tournament_table.all()
        tournament = Tournament.correspond_tournament(tournament_db[0])
        if not isinstance(tournament, Tournament):
            raise ValueError("Tournament in DB not correct")
        return tournament


class Tournaments(list):
    """
    Tournament's name list
    Tournament_actif list for extension (case of multiple tournament in same time)
    """

    list_tournament = []
    tournaments_actif: List[Tournament] = []

    def __init__(self):
        super().__init__()

    @classmethod
    def add_db_tournament(cls, tournament):
        """ Add name of tournament in table tournaments
            And become active"""
        db = TinyDB(PATH)
        tournaments_table = db.table(NAME_TOURNAMENTS_TABLE)  # pour les tournois regroupant tout
        tournaments_table.insert(tournament['name'])
        cls.tournaments_actif.append(tournament)

    @classmethod
    def save_all(cls):  # pas bon
        """
        save list of name of tournament
        :return: ok
        """
        for element in cls.tournaments_actif:
            db = TinyDB(PATH)
            tournaments_table = db.table(NAME_TOURNAMENTS_TABLE)  # pour le tournoi regroupant tout
            tournaments_table.insert_multiple(element['name'])
        return

    @classmethod
    def load_all(cls):
        """
        :return: Load in list_of_tournament all the names of existing tournaments
        """
        db = TinyDB(PATH)
        tournaments_table = db.table(NAME_TOURNAMENTS_TABLE)
        list_tables = db.tables()
        cls.list_tournament = []
        list_temp = tournaments_table.all()
        for document in list_temp:
            if document in list_tables:
                cls.list_tournament.append(document)
            else:
                print(ValueError(f"Tournament {document} incorrectly saving"))

    @classmethod
    def print_all(cls):
        """
        :return: -> str text with all tournament for print
        """
        text = ""
        for x in range(len(cls.list_tournament)):
            text += f"Tournoi {cls.list_tournament[x]}:\n{Tournament.load(cls.list_tournament[x])}"
        return text


class Round(list):
    """
    Actuellement, nous appelons nos tours "Round 1", "Round 2", etc.
    Elle doit également contenir un champ Date et heure de début
    et un champ Date et heure de fin, qui doivent tous deux être
    automatiquement remplis lorsque l'utilisateur crée un tour et le marque comme terminé.
    (Au moment de la fin du tour, le score du joueur sera mis à jour.)
    Et contient la liste des matches.
    """

    def __init__(self, list_players_id):
        super().__init__()
        self.list_players_id = list_players_id
        self.name = ""
        self.starting_date = strftime('%d/%m/%Y')
        self.starting_time = strftime('%H:%M:%S')
        self.finish_time = ""
        self.list_matches_resultat = ()
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

    def __init__(self, couple_players):
        self.couple_players = couple_players
        self.resultat_match: Tuple = ()

    def match_resultat(self):
        [player1, player2] = self.match_players_ids_to_players()
        player1_id = self.couple_players[0]
        player2_id = self.couple_players[1]
        player1_resultat = player1['score_last_match']
        player2_resultat = player2['score_last_match']
        self.resultat_match = ([player1_id, player1_resultat], [player2_id, player2_resultat])
        return self.resultat_match

    def match_players_ids_to_players(self):
        player1_id = self.couple_players[0]
        player2_id = self.couple_players[1]
        player1 = PlayersId.id_to_dict(player1_id)
        player2 = PlayersId.id_to_dict(player2_id)
        return [player1, player2]



