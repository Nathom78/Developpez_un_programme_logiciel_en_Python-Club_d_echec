"""Base view."""
import datetime


class View:
    """view."""

    @staticmethod
    def prompt_for_tournament():
        """Prompt  for information to create a tournament"""
        name = input("Donner un nom au tournoi :")
        place = input("Lieu du tournoi :")
        type_game_time = input("Type du jeu (bullet, blitz, ou coup rapide :")
        number_total_round = input("Nombre de ronde (par default 4 ) :")
        description = input("description (facultatif) :")
        parameter = [name, place, type_game_time, number_total_round, description]
        return parameter

    @staticmethod
    def make_list_player_from_db():
        """ Afficher la liste des joueurs et choisir x joueurs
        Return : List ID's players for tournament
        """
        pass

    # Menu Club Manage
    @staticmethod
    def menu_manage_club():
        """
        Return : choix dans le menu
        """
        print("1) Enregistrer un nouveau joueur 2) Liste des joueurs "
              "3) Modifier un joueur 4) Retour")
        choice = 0
        if_number = False
        while not if_number:
            choice = input()
            try:
                choice = int(choice)
                if 0 < choice <= 4:  # number max in menu...
                    if_number = True
            except ValueError:
                print("Veuillez taper un nombre entre 1 et 4")
        return choice

    @staticmethod
    def menu_manage_club_case_1():
        """Prompt for player.
        family_name, first_name, date_of_birth, sex, ranking, score=0
        return une list
        """
        family_name = ""
        if_str = False
        while not if_str:
            family_name = input("tapez le nom de famille du joueur :")
            try:
                if_str = family_name.isalpha()
            except ValueError:
                print("Veuillez mettre seulement des lettres")

        first_name = ""
        if_str = False
        while not if_str:
            first_name = input("tapez le prénom du joueur :")
            try:
                if_str = first_name.isalpha()
            except ValueError:
                print("Veuillez mettre seulement des lettres")

        date_of_birth = ""
        if_date = False
        while not if_date:
            date_of_birth = input("tapez la date de naissance du joueur (dd/mm/yyyy) :")
            try:
                datetime.datetime.strptime(date_of_birth, '%d/%m/%Y')
                if_date = True
            except ValueError:
                print("Incorrect data format, should be dd/mm/yyyy")

        sex = ""
        if_sex = False
        while not if_sex:
            sex = input("tapez le genre du joueur (M ou F) :")
            if sex == ("M" or "F" or "m" or "f"):
                if_sex = True
            else:
                print("Mauvaise lettre")

        ranking = 0
        if_number = False
        while not if_number:
            ranking = input("taper le score (rang Elo) :")
            try:
                ranking = int(ranking)
                if_number = True
            except ValueError:
                print("Veuillez taper un nombre")

        score = 0
        if_number = False
        while not if_number:
            score = input("Rentrer le score si different de 0")
            if score == "":
                score = 0
            try:
                score = int(ranking)
                if_number = True
            except ValueError:
                print("Veuillez taper un nombre")

        parameter = [family_name, first_name, date_of_birth, sex, ranking, score]
        return parameter

    @staticmethod
    def menu_manage_club_case_2():
        """ Prompt for List """
        print("1) Liste de tous les acteurs\n "
              "2) Liste de tous les joueurs d'un tournoi\n"
              "3) Liste de tous les tournois.\n"
              "4) Liste de tous les tours d'un tournoi.\n"
              "5) Liste de tous les matchs d'un tournoi.\n"
              "0) Retour")
        choice = 0
        if_number = False
        while not if_number:
            choice = input()
            try:
                choice = int(choice)
                if 0 <= choice <= 5:  # number max in menu...
                    if_number = True
            except ValueError:
                print("Veuillez taper un nombre entre 0 et 5")
        return choice

    @staticmethod
    def menu_manage_club_case_2_a():
        """ request the choice of sorting from the list"""
        print("1) Rangé par ordre alphabétique\n"
              "2) Rangé par classement")
        sort = 0
        if_number = False
        while not if_number:
            sort = input()
            try:
                sort = int(sort)
                if 0 < sort <= 2:  # number max in menu...
                    if_number = True
            except ValueError:
                print("Veuillez taper 1 ou 2")
        return sort

    @staticmethod
    def menu_manage_club_case_2_print(text):
        """ Print List of all Players' Club"""
        print(text)
        pass

    @staticmethod
    def menu_manage_club_case_2_2_choice(tournaments):
        """
        Choice from the list of tournaments
        :return: name of the tournament to print
        """
        print("Choisir un tournoi pour afficher sa liste de joueur")
        i = 0
        for tournament in tournaments:
            i += 1
            print(f"{i}) {tournament}")
        choice = 0
        if_number = False
        while not if_number:
            choice = input("Entrer le numéro du tournoi")
            try:
                choice = int(choice)
                if 0 < choice <= i:
                    if_number = True
            except ValueError:
                print(f"Veuillez entrer un nombre entre 1 et {i}")
        return tournaments[choice-1]

    @staticmethod
    def menu_manage_club_case_2_3():
        """ Print List of all tournaments"""
        pass

    @staticmethod
    def menu_manage_club_case_2_4():
        """ Print List of all rounds"""
        pass

    @staticmethod
    def menu_manage_club_case_2_5():
        """ Print List of all matches"""
        pass
