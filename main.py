"""main"""

from controllers.base import ControllerTournaments
from controllers.club_manage import ControllerMenu
from controllers.system_swiss import ControllerSwiss

from views.base import View


def main():
    view = View
    menu = ControllerMenu(view, ControllerTournaments)
    method_calcul_round = ControllerSwiss

    ControllerTournaments(view, menu, method_calcul_round).run()


if __name__ == "__main__":
    main()
