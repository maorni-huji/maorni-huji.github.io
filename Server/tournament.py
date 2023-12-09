# This file calculates who plays verses who and saves the results in it according to the users' reports
import numpy
import pandas as pd
import numpy as np

# Who won the game form:
# edit / results - https://docs.google.com/forms/d/1bpUep3OJk6Lx0wG3vYGh91DKMyjE9XEtcPc_vk49U2k/edit
# publish - https://forms.gle/49FchrWEK4fFDqqV6
#
# Participants form:
# edit - https://docs.google.com/forms/d/1XQB1ZfV5IWo0DV9wPTN_Z5Djd7rPNp5p1mmdxkb0n0M/edit
# results - https://docs.google.com/spreadsheets/d/1eTYPuTH6OzPgOxFmy-78SW6aQ3jH9pkksxTKOlegOhU/edit?resourcekey#gid=443634803
# publish - https://forms.gle/m8ocsvYgksHqcFy3A


class Competitor:
    DEFAULT_PARTICIPANTS = "Server/participants.xlsx"
    DEFAULT_WINNERS = "Server/winners.xlsx"

    def __init__(self, comp_names: list, group_name):
        self.competitors = comp_names
        self.group_name = group_name
        self.score = 0  # inner score, used for the system decisions of who plays verses who (it doesn't say who wins)

        if 0 == len(comp_names) or "" == group_name:  # should never happen
            raise Exception("error - illegal group details")

    def __str__(self):
        if len(self.competitors) > 1:
            return self.group_name + " (" + ", ".join(self.competitors) + ")"
        else:
            return self.group_name + " (" + self.competitors[0] + ")"


class Tournament:

    def __init__(self, participants: list[Competitor] = None):
        self.participants_in = participants if participants is not None else []  # participants inside the tournament
        self.participants_out = []  # participants out of the tournament (and want to keep playing for fun or rating)
        self.stage = 0

    def fetch_participants(self, file_path=Competitor.DEFAULT_PARTICIPANTS):
        """
        Parses the participants google form answers into python object
        :param file_path: The participants' Excel file location
        :return: None, it updates the class's variable itself
        """
        content = pd.read_excel(file_path).to_dict()
        for i in range(len(content["משתתף 1"])):
            comp_names = [user for user in [content["משתתף 1"][i], content["משתתף 2"][i], content["משתתף 3 (רק באישור שלנו)"][i]] if isinstance(user, str)]
            self.participants_in += [Competitor(comp_names=comp_names, group_name=content["שם הקבוצה"][i])]

    def choose_pairs(self):
        """
        Chooses pairs to compete in the current tournament stage
        :return: A list of pairs to compete each other in the tournament,
                 and a list of pairs who lost the game to compete each other just for fun
        """
        pass

    def publish_pairs(self, pairs_to_compete, pairs_for_fun):
        """
        Publishes the competitors who compete each other in the current stage
        It can edit index.html or edit an online Google sheets
        :param pairs_to_compete: A list of pairs who compete each other in the tournament
        :param pairs_for_fun: A list of pairs who have already lost the game, but still compete each other
        :return: None, it edits the index.html
        """
        pass

    def update_google_form(self):
        """
        Prints to the screen the name of the winning competitors - so the program's runner can copy those names
        and paste them in the google forms that asks who won the current game
        :return: None, it prints the names of the self.participants_in to the screen
        """
        print("Competitors who are currently in the game: ")
        for competitors in self.participants_in:
            print(competitors)
        print()

    def fetch_winners(self, file_path=Competitor.DEFAULT_WINNERS):
        """
        Parses the names of the winning groups (from Google forms) into the class
        :param file_path: The winner groups Excel file location
        :return: None, it updates the data
        """
        pass
