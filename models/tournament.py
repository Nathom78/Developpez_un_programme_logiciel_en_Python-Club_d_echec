from typing import List, Tuple
from time import strftime
from tinydb import TinyDB, where
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

    def tournament_players(self, list_player_id):
        self['players'] = list_player_id

    def save(self):
        name = self['name']
        db = TinyDB(PATH)
        tournaments_table = db.table(name)  # pour le tournoi regroupant tout
        tournaments_table.upsert(self, 'name' == self['name'])

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

        tournaments_table.upsert({'name': tournament['name']},
                                 where('name') == tournament['name'])
        cls.tournaments_actif.append(tournament)

    @classmethod
    def save_all(cls):  # pas bon 1) risque de 2 fois le même
        """
        Save les tournois actifs
        :return: ok
        """
        # A changer pour save le tournois
        for element in cls.tournaments_actif:
            db = TinyDB(PATH)
            tournaments_table = db.table(NAME_TOURNAMENTS_TABLE)  # pour le tournoi regroupant tout
            tournaments_table.upsert({'name': element['name']}, 'name' == element['name'])
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
                cls.list_tournament.append(document['name'])
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

    def __init__(self):
        super().__init__()
        self.name = ""
        self.starting_date = strftime('%d/%m/%Y')
        self.starting_time = strftime('%H:%M:%S')
        self.finish_time = ""
        self.finish_date = ""
        self.list_matches_result: List[Match.match_result] = []
        self.list_results = []
        self.couples_players = []
        self.list_matches: List[Match] = []

    def __str__(self):
        return f"\nLa ronde {self.name} commencé le " \
               f"{self.starting_date} à {self.starting_time}\n" \
               f"avec {self['number_total_round']} ronde, le type du jeux est " \
               f" {self['type_game_time']}\n" \
               f"liste des rounds : {self['rounds']}\n" \
               f"liste des joueurs : {self['players']}"

    def append(self, object: object):  # ne sert pas
        """Append a match. """
        if not isinstance(object, Match):
            return ValueError("Tour mal configuré")
        return super().append(object)


class Match:
    """
    Création d'un tuple contenant deux listes, chacune contenant deux éléments :
    une référence à une instance de joueur et un score
    """

    def __init__(self, couple_players_id):
        """
        :param couple_players_id: LIST de 2 id
        """
        self.couple_players_id = couple_players_id
        self.result_match: Tuple = ()

    def __str__(self):
        [player1, player2] = self.match_players_ids_to_players()
        ([_, player1_result], [_, player2_result]) = self.result_match
        return f"Match {player1['family_name']} {player1['first_name']} " \
               f"contre {player2['family_name']} {player2['first_name']}\n" \
               f"Le resultat est :\n" \
               f" {player1['family_name']} {player1['first_name']} " \
               f"à {player1_result} point\n" \
               f" {player2['family_name']} {player2['first_name']} " \
               f"à {player2_result} point\n"

    def match_result(self):
        [player1, player2] = self.match_players_ids_to_players()
        player1_id = self.couple_players_id[0]
        player2_id = self.couple_players_id[1]
        player1_result = player1['score_last_match']
        player2_result = player2['score_last_match']
        self.result_match = ([player1_id, player1_result], [player2_id, player2_result])
        return self.result_match

    def match_players_ids_to_players(self):
        player1_id = self.couple_players_id[0]
        player2_id = self.couple_players_id[1]
        player1 = PlayersId.id_to_dict(player1_id)
        player2 = PlayersId.id_to_dict(player2_id)
        return [player1, player2]


t1 = Tournament('T1', 'Maison', 'bullet')
t2 = Tournament('T2', 'Home', 'bullet')
Tournaments.add_db_tournament(t1)
Tournaments.add_db_tournament(t2)
t1.tournament_players([1, 2, 3, 4, 5, 6, 7, 8])
round1 = Round()
round1.name = 'Round1'
match1 = Match([1, 2])
match2 = Match([3, 4])
match3 = Match([5, 6])
match4 = Match([7, 8])
round1.list_matches = [match1, match2, match3, match4]
for match in round1.list_matches:  # Peut-être supprimer round couples players
    round1.couples_players.append(match.match_players_ids_to_players())

