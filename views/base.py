"""Base view."""

import datetime
import string
from os import system, name
from time import sleep


class View:
    """view."""

    @staticmethod
    def ask_start():
        """Starting Tournament New tournament or load
        :return choice:
        """
        print("1) Nouveau tournoi\n2) Charger un tournoi")
        choice = 0
        if_number = False
        while not if_number:
            choice = input(": ")
            try:
                choice = int(choice)
                if 0 < choice <= 2:  # number max in menu...
                    if_number = True
            except ValueError:
                print("Veuillez taper un nombre entre 1 et 2")
        return choice

    @staticmethod
    def ask_resultat_or_menu():
        """

        :return: choice
        """
        print("Voulez-vous rentrer un résultat (1) ou voir le menu (2)")
        choice = 0
        if_number = False
        while not if_number:
            choice = input(": ")
            try:
                choice = int(choice)
                if 0 < choice <= 2:  # number max in menu...
                    if_number = True
            except ValueError:
                print("Veuillez taper un nombre entre 1 et 2")
        return choice

    @staticmethod
    def prompt_for_tournament(exist_names):
        """Prompt  for information to create a tournament"""
        not_exist = False
        name_t = ""
        while not not_exist:
            name_t = input("Donner un nom au tournoi : ")
            if name_t not in exist_names:
                not_exist = True
            else:
                print("Nom déja existant")
        place = input("Lieu du tournoi : ")
        type_game_time = input("Type du jeu (bullet, blitz, ou coup rapide : ")
        if_number = False
        number_total_round = 0
        while not if_number:
            number_total_round = input("Nombre de ronde (par default 4 ) : ")
            if number_total_round == "":
                number_total_round = 4
            try:
                number_total_round = int(number_total_round)
                if 0 <= number_total_round:
                    if_number = True
            except ValueError:
                print("Veuillez taper un nombre positif")
        description = input("description (facultatif) : ")
        parameter = [name_t, place, type_game_time, number_total_round, description]
        return parameter

    @staticmethod
    def make_list_player_from_db(text):
        """ Afficher la liste des joueurs et choisir 1 joueur
        Return : List ID's players for tournament
        """
        print(text)
        print("Entrer le numéro du joueur à ajouter, ou 0 pour ajouter un nouveau")
        if_number = False
        number_in_list = 0
        while not if_number:
            number_in_list = input(": ")
            try:
                number_in_list = int(number_in_list)
                if 0 <= number_in_list:
                    if_number = True
            except ValueError:
                print("Veuillez taper un nombre")

        return number_in_list

    # Menu Club Manage
    @staticmethod
    def menu_manage_club():
        """
        Return : choix dans le menu
        """
        print("\nMenu gestion du club")
        print("\n1) Enregistrer un nouveau joueur\n2) Listes\n"
              "3) Modifier un joueur\n4) Enregistrer le tournoi\n5) Charger un tournoi"
              "\n6) Quitter le programme\n7) Continuer\n")
        choice = 0
        if_number = False
        while not if_number:
            choice = input("Votre choix : ")
            try:
                choice = int(choice)
                if 0 < choice <= 7:  # number max in menu...
                    if_number = True
            except ValueError:
                print("Veuillez taper un nombre entre 1 et 7")
        return choice

    @staticmethod
    def menu_manage_club_case_1():
        """Prompt for player.
        family_name, first_name, date_of_birth, sex, ranking, score=0
        return  list of parameter for be a Player
        """
        family_name = ""
        if_str = False
        while not if_str:
            family_name = input("tapez le nom de famille du joueur :")
            if_str = family_name.isalpha()
            if not if_str:
                print("Veuillez mettre seulement des lettres")

        first_name = ""
        if_str = False
        while not if_str:
            first_name = input("tapez le prénom du joueur :")
            if_str = first_name.isalpha()
            if not if_str:
                print("Veuillez mettre seulement des lettres")

        date_of_birth = ""
        if_date = False
        while not if_date:
            date_of_birth = input("tapez la date de naissance du joueur (dd/mm/yyyy) : ")
            try:
                datetime.datetime.strptime(date_of_birth, '%d/%m/%Y')
                if_date = True
            except ValueError:
                print("Incorrect data format, should be dd/mm/yyyy")

        sex = ""
        if_sex = False
        while not if_sex:
            sex = input("tapez le genre du joueur (M ou F) : ")
            if sex == "M" or "F" or "m" or "f":
                if_sex = True
            else:
                print("Mauvaise lettre")

        ranking = 0
        if_number = False
        while not if_number:
            ranking = input("taper le score (rang Elo) : ")
            try:
                ranking = int(ranking)
                if_number = True
            except ValueError:
                print("Veuillez taper un nombre")

        score = 0
        if_number = False
        while not if_number:
            score = input("Rentrer le score si different de 0 : ")
            if score == "":
                score = 0
            try:
                score = int(score)
                if_number = True
            except ValueError:
                print("Veuillez taper un nombre")

        parameter = [family_name, first_name, date_of_birth, sex, ranking, score]
        return parameter

    @staticmethod
    def menu_manage_club_case_2():
        """ Prompt for List """
        print("1) Liste de tous les acteurs\n"
              "2) Liste de tous les joueurs d'un tournoi\n"
              "3) Liste de tous les tournois.\n"
              "4) Liste de tous les tours d'un tournoi.\n"
              "5) Liste de tous les matchs d'un tournoi.\n"
              "0) Retour")
        choice = 0
        if_number = False
        while not if_number:
            choice = input("Votre choix : ")
            try:
                choice = int(choice)
            except ValueError:
                print("Veuillez taper un nombre entre 0 et 5")
            else:
                if 0 <= choice <= 5:  # number max in menu...
                    if_number = True
                else:
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
            sort = input(": ")
            try:
                sort = int(sort)
                if 0 < sort <= 2:  # number max in menu...
                    if_number = True
                else:
                    print("Veuillez taper 1 ou 2")
            except ValueError:
                print("Veuillez taper 1 ou 2")
        return sort

    @staticmethod
    def menu_manage_club_case_2_print(text):
        """ Print text"""
        print(text)
        return

    @staticmethod
    def menu_manage_club_case_2_2_choice(tournaments):
        """
        Choice from the list of tournaments' names
        :return: name of the tournament to print
        """
        if len(tournaments) == 0:
            print("Aucun tournoi d'enregistré")
            sleep(2)
            return 0
        print("Choisir un tournoi")
        i = 0
        for tournament in tournaments:
            i += 1
            print(f"{i}) {tournament}")

        choice = 0
        if_number = False
        while not if_number:
            choice = input("Entrer le numéro du tournoi : ")
            try:
                choice = int(choice)
                if 0 < choice <= i:
                    if_number = True
                else:
                    print(f"Veuillez entrer un nombre entre 1 et {i}")
            except ValueError:
                print(f"Veuillez entrer un nombre entre 1 et {i}")
        return tournaments[choice - 1]

    @staticmethod
    def menu_manage_club_case_3_1(text, i):
        """ Choice Player to modify"""
        print(text)
        choice = 0
        if_number = False
        while not if_number:
            choice = input("Entrer le numéro du joueur à modifier : ")
            try:
                choice = int(choice)
                if 0 < choice <= i:
                    if_number = True
                else:
                    print(f"Veuillez entrer un nombre entre 1 et {i}")
            except ValueError:
                print(f"Veuillez entrer un nombre entre 1 et {i}")
        return choice

    @staticmethod
    def menu_manage_club_case_3_2(player):
        """
        Prompt for modify a Player
        :param player: Player
        :return: player modify
        """

        print('Entrer une nouvelle valeur ou juste taper la touche "Entrée" : ')
        player_modify = player
        if_str = False
        while not if_str:
            family_name = input(f"- nom de famille du joueur : {player['family_name']} : ")
            if family_name == "":
                if_str = True
            elif family_name.isalpha():
                player_modify['family_name'] = str.upper(family_name)
                if_str = True
            else:
                print("Veuillez mettre seulement des lettres")

        if_str = False
        while not if_str:
            first_name = input(f"tapez le prénom du joueur : {player['first_name']} : ")
            if first_name == "":
                if_str = True
            elif first_name.isalpha():
                player_modify['first_name'] = string.capwords(first_name)
                if_str = True
            else:
                print("Veuillez mettre seulement des lettres")

        if_date = False
        while not if_date:
            date_of_birth = input("tapez la date de naissance du joueur (dd/mm/yyyy) : "
                                  f"{player['date_of_birth']} : ")
            try:
                if date_of_birth != "":
                    datetime.datetime.strptime(date_of_birth, '%d/%m/%Y')
                    player_modify['date_of_birth'] = date_of_birth
                if_date = True
            except ValueError:
                print("Incorrect data format, should be dd/mm/yyyy")

        if_sex = False
        while not if_sex:
            sex = input(f"tapez le genre du joueur (M ou F) :{player['sex']} : ")
            if sex == ("M" or "F" or "m" or "f"):
                player_modify['sex'] = sex
                if_sex = True
            elif sex == "":
                if_sex = True
            else:
                print("Mauvaise lettre")

        if_number = False
        while not if_number:
            ranking = input(f"taper le score (rang Elo) : {player['ranking']} : ")
            try:
                if ranking == '':
                    if_number = True
                else:
                    ranking = int(ranking)
                    if ranking < 0:
                        raise ValueError
                    player_modify['ranking'] = ranking
                    if_number = True
            except ValueError:
                print("Veuillez taper un nombre positif")

        if_number = False
        while not if_number:
            score = input("Rentrer le score total dans le tournoi : "
                          f" {player['score']}")
            if score == "":
                break
            try:
                score = int(score)
                if score < 0:
                    raise ValueError
                player_modify['score'] = score
                if_number = True
            except ValueError:
                print("Veuillez taper un nombre positif")

        return player_modify

    @staticmethod
    def menu_manage_club_case_3_3(text):
        """ print modify state"""
        print(text)
        sleep(2)

    @staticmethod
    def menu_manage_club_case_4_choice(tournaments):
        """Choice of the tournament to save
        :param tournaments: Tournaments dans les Tournaments_actif
        :return: the tournament
        """
        i = 0
        for tournament in tournaments:
            i += 1
            print(f"\nchoix {i} :")
            print(tournament['name'])
        choice = 0
        if_number = False
        while not if_number:
            choice = input("Entrer le numéro du tournoi à sauvegarder : ")
            try:
                choice = int(choice)
                if 0 < choice <= i:
                    if_number = True
                else:
                    print(f"Veuillez entrer un nombre entre 1 et {i}")
            except ValueError:
                print(f"Veuillez entrer un nombre entre 1 et {i}")
        return tournaments[choice-1]

    @staticmethod
    def menu_manage_club_case_4_done(tournament_name):
        print(f"Tournoi {tournament_name} sauvegardé")
        return

    @staticmethod
    def clear_screen():
        # It is for macOS and Linux(here, os.name is 'posix')
        if name == 'posix':
            system('clear')

        else:
            # It is for Windows platform
            system('cls')

    @staticmethod
    def print_match(couples_players, i, list_color):
        """
        :param list_color: Liste de nb_match fois avec soit blanc ou noir
        :param i: the number of the round
        :param couples_players:
        :return: list resultat
        """
        # Affiche le round et les matches à jouer
        print(f"\nRonde {i}: ")
        x = 0
        for [player1, player2], color in zip(couples_players, list_color):
            x += 1
            print(f"match {x} opposant {player1['family_name']} {player1['first_name']} "
                  f"contre {player2['family_name']} {player2['first_name']}\n "
                  f"Joueur {player1['family_name']} {player1['first_name']} prends les {color}s")

    @staticmethod
    def input_match_result(couple_players, number_match, number_round):
        # Attend les résultats des matchs
        print(f"\nRentrer les résultats de la ronde {number_round}: ")
        [player1, player2] = couple_players
        print(f"Resultat du match {number_match + 1} : \nopposant le joueur 1 "
              f"{player1['family_name']} {player1['first_name']}\n"
              f"contre le joueur 2 {player2['family_name']} {player2['first_name']} : ")
        print("1) Joueur 1 a gagné\n2) Joueur 2 a gagné\n3) Match nul\n4) Menu")
        result_match = 0
        if_number = False
        while not if_number:
            result_match = input("Rentrer le résultat : ")
            try:
                result_match = int(result_match)
                if 0 < result_match <= 4:
                    if_number = True
            except ValueError:
                print("Veuillez taper un chiffre, soit 1, 2, 3 ou 4")
        return result_match

    @staticmethod
    def wait():
        print("appuyer sur entrer pour continuer")
        input()
        return
