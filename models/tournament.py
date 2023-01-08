from typing import List, Tuple
from time import strftime
from tinydb import TinyDB, where
from models.players import PlayersId, Player

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
        return f"Le tournoi {self['name']} du lieu {self['place']} commencé le " \
               f"{self['date_creation']}\n" \
               f"a {self['number_total_round']} rondes, le type du jeux est " \
               f"{self['type_game_time']},\n" \
               f"liste des rounds : {self['rounds']}\n" \
               f"liste des joueurs : {self['players']}\n"

    def tournament_players(self, list_player_id):
        self['players'] = list_player_id

    def save(self):
        name = self['name']
        db = TinyDB(PATH)
        tournaments_table = db.table(name)  # pour le tournoi regroupant tout
        tournaments_table.upsert(self, where('name') == self['name'])

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
            print(f"Base de donnée incorrect pour le tournoi {tournament_temp}")
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
    def save_all(cls):  # pas possible sauf en nommant l'instance du tournoi avec un index,
        # correspondant à celui dans la liste, et en passant les tournois en parameter
        """
        Save les tournois actifs
        :return: ok
        """
        # À changer pour save les tournois et non la liste des noms
        for element in cls.tournaments_actif:
            db = TinyDB(PATH)
            tournaments_table = db.table(NAME_TOURNAMENTS_TABLE)  # pour le tournoi regroupant tout
            tournaments_table.upsert({'name': element['name']}, where('name') == element['name'])
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
            if document['name'] in list_tables:
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
            text += f"Tournoi {cls.list_tournament[x]} :\n{Tournament.load(cls.list_tournament[x])}"
        return text


class Round:
    """
    Actuellement, nous appelons nos tours "Round 1", "Round 2", etc.
    Elle doit également contenir un champ Date et heure de début
    et un champ Date et heure de fin, qui doivent tous deux être
    automatiquement remplis lorsque l'utilisateur crée un tour et le marque comme terminé.
    (Au moment de la fin du tour, le score du joueur sera mis à jour.)
    Et contient la liste des matches.
    """

    def __init__(self):
        self.name = ""
        self.starting_date = strftime('%d/%m/%Y')
        self.starting_time = strftime('%H:%M:%S')
        self.finish_time = ""
        self.finish_date = ""
        self.list_results = []
        self.list_matches: List[Match] = []

    def __str__(self):
        return f"\nLa ronde {self.name} commencé le " \
               f"{self.starting_date} à {self.starting_time}\n" \
               f"\nListe des matchs :\n\n" \
               f"{self.list_matches[0]}\n" \
               f"{self.list_matches[1]}\n" \
               f"{self.list_matches[2]}\n" \
               f"{self.list_matches[3]}\n" \
               f"Finis le {self.finish_date} à {self.finish_time}\n"

    @staticmethod
    def instantiate(serialized_round):
        round_temp = Round
        try:
            round_temp.name = serialized_round['name']
            round_temp.starting_date = serialized_round['starting_date']
            round_temp.starting_time = serialized_round['starting_time']
            round_temp.finish_time = serialized_round['finish_time']
            round_temp.finish_date = serialized_round['finish_date']
            round_temp.list_results = serialized_round['list_results']
            round_temp.list_matches = serialized_round['list_matches']
        except(KeyError, TypeError,):
            print(f"Base de donnée incorrect pour le round {serialized_round}")
        finally:
            if not isinstance(round_temp, Round):
                raise ValueError("tournoi mal défini!")
        return round_temp


class RoundSerialized(dict):

    def __init__(self):
        super().__init__()
        self['name'] = ""
        self['starting_date'] = ""
        self['starting_time'] = ""
        self['finish_time'] = ""
        self['finish_date'] = ""
        self['list_results'] = []
        self['list_matches']: List[Match] = []

    def ready_to_save(self, round_to):
        """

        :type round_to: Round
        """
        self['name'] = round_to.name
        self['starting_date'] = round_to.starting_date
        self['starting_time'] = round_to.starting_time
        self['finish_time'] = round_to.finish_time
        self['finish_date'] = round_to.finish_date
        self['list_results'] = round_to.list_results
        for match_to in round_to.list_matches:
            self['list_matches'].append(MatchSerialized(match_to))
        return self


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
               f"le resultat est :\n" \
               f"{player1['family_name']} {player1['first_name']} " \
               f"a {player1_result} point\n" \
               f"{player2['family_name']} {player2['first_name']} " \
               f"a {player2_result} point\n"

    def match_result(self):
        [player1, player2] = self.match_players_ids_to_players()
        player1_id = self.couple_players_id[0]
        player2_id = self.couple_players_id[1]
        player1_result = player1['score_last_match']
        player2_result = player2['score_last_match']
        self.result_match = ([player1_id, player1_result], [player2_id, player2_result])

    def match_players_ids_to_players(self):
        player1_id = self.couple_players_id[0]
        player2_id = self.couple_players_id[1]
        player1 = PlayersId.id_to_dict(player1_id)
        player2 = PlayersId.id_to_dict(player2_id)
        return [player1, player2]


class MatchSerialized(dict):

    def __init__(self, match_to):
        """

        :type match_to: Match
        """
        super().__init__()
        self['couple_players_id'] = match_to.couple_players_id
        self['result_match'] = match_to.result_match


# t1 = Tournament('T1', 'Maison', 'bullet')
# t2 = Tournament('T2', 'Home', 'bullet')
# Tournaments.add_db_tournament(t1)
# Tournaments.add_db_tournament(t2)
# t1.tournament_players([1, 2, 3, 4, 5, 6, 7, 8])
# round1 = Round()
# round1.name = 'Round1'
# match1 = Match([1, 2])
# match2 = Match([3, 4])
# match3 = Match([5, 6])
# match4 = Match([7, 8])
# round1.list_matches = [match1, match2, match3, match4]
# for match in round1.list_matches:  # Peut-être supprimer round couples players
#     match.match_result()
# round1.list_results = [1, 1, 3, 2]
# round1.finish_time = strftime('%H:%M:%S')
# round1.finish_date = strftime('%d/%m/%Y')
# print(round1)
# round1_serialized = RoundSerialized().ready_to_save(round1)
#
# t1['rounds'].append(round1_serialized)
# print(t1['rounds'])
# t1.save()
