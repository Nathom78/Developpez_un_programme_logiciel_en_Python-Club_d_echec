from models.tournament import Match
from models.players import PlayersId


class ControllerSwiss:
    """
    :return: List de match
    """

    def __init__(self):
        self.list_match = Match
        self.players = []

    def run(self, player_tournament):
        self.players = player_tournament
        match1 = Match([1, 2])
        match2 = Match([3, 4])
        match3 = Match([5, 6])
        match4 = Match([7, 8])
        self.list_match = [match1, match2, match3, match4]
        return self.list_match






