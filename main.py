"""main"""

from controllers.base import ControllerTournaments
from controllers.club_manage import ControllerMenuPlayersLists
from controllers.system_swiss import ControllerSwiss

from views.base import View


def main():
    view = View
    menu = ControllerMenuPlayersLists(view)
    method_calcul_round = ControllerSwiss

    game = ControllerTournaments(view, menu, method_calcul_round)
    game.run()


if __name__ == "__main__":
    main()
