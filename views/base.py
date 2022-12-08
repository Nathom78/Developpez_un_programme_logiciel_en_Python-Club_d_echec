"""Base view."""
import datetime


class PlayerView:
    """Player view."""

    @staticmethod
    def prompt_for_player():
        """Prompt for a name.
        family_name, first_name, date_of_birth, sex, ranking, score=0
        """
        family_name = input("tapez le nom de famille du joueur :")
        first_name = input("tapez le prénom du joueur :")
        date_of_birth = ""
        if_date = False
        while not if_date:
            date_of_birth = input("tapez la date de naissance du joueur (dd/mm/yyyy) :")
            try:
                datetime.datetime.strptime(date_of_birth, '%d/%m/%Y')
                if_date = True
            except ValueError:
                print("Incorrect data format, should be dd/mm/yyyy")

        sex = input("tapez le genre du joueur (M ou F ou preciser) :")
        ranking = 0
        if_number = False
        while not if_number:
            ranking = input("taper le score (rang Elo) :")
            try:
                ranking = int(ranking)
                if_number = True
            except ValueError:
                print("Veuillez taper un nombre")

        parameter = [family_name, first_name, date_of_birth, sex, ranking]
        return parameter

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
