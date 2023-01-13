"""main"""
from os import makedirs
from controllers.base import ControllerTournaments
from controllers.club_manage import ControllerMenu
from controllers.system_swiss import ControllerSwiss

from views.base import View


def main():
    # création du repertoire database si besoin
    makedirs('database', exist_ok=True)

    view = View
    menu = ControllerMenu(view)
    method_calcul_round = ControllerSwiss
    game = ControllerTournaments(view, menu, method_calcul_round)

    while game.fin != 1:
        game.run()
        if game.load == 1 or menu.load == 1:
            game.load_tournament()
            game.load = 0
            menu.load = 0


if __name__ == "__main__":
    main()
