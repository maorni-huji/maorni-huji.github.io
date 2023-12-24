# This file calculates who plays verses who and saves the results in it according to the users' reports
import pandas as pd
from random import choice

# Who won the game form:
# edit - https://docs.google.com/forms/d/1bpUep3OJk6Lx0wG3vYGh91DKMyjE9XEtcPc_vk49U2k/edit
# results - https://docs.google.com/spreadsheets/d/1IyzT8g9rnnWTDLsSvEwOAX9BEZAHkCDNzbdMkDwWO9s/edit?resourcekey#gid=1329863517
# publish - https://forms.gle/49FchrWEK4fFDqqV6
#
# Participants form:
# edit - https://docs.google.com/forms/d/1XQB1ZfV5IWo0DV9wPTN_Z5Djd7rPNp5p1mmdxkb0n0M/edit
# results - https://docs.google.com/spreadsheets/d/1eTYPuTH6OzPgOxFmy-78SW6aQ3jH9pkksxTKOlegOhU/edit?resourcekey#gid=443634803
# publish - https://forms.gle/m8ocsvYgksHqcFy3A
#
# Website:
# https://maorni-huji.github.io/
# edit the website by editing index.html and push it to GitHub (maorni-huji.github.io)


class Competitor:
    DEFAULT_PARTICIPANTS = "Server/participants.xlsx"
    DEFAULT_WINNERS = "Server/winners.xlsx"

    def __init__(self, comp_names: list[str], group_name):
        self.group_name = Competitor.edit_group_name(comp_names, group_name)
        self.avoided_battle = False
        self.won = False
        self.score = 0  # inner score, used for the system decisions of who plays verses who (it doesn't say who wins)

        if 0 == len(comp_names) or "" == group_name:  # should never happen
            raise Exception("error - illegal group details")

    @staticmethod
    def edit_group_name(comp_names: list[str], group_name: str):
        return group_name + " (" + ", ".join(comp_names) + ")"

    def __str__(self):
        return self.group_name


class Tournament:
    def __init__(self, participants: list[Competitor] = None):
        self.participants_in = participants if participants is not None else []  # participants inside the tournament
        self.participants_out = []  # participants out of the tournament (and want to keep playing for fun or rating)
        self.compete_in = []  # list of competitors who currently compete each other
        self.compete_out = []  # list of competitors who are out of the game
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
        Chooses pairs to compete in the current tournament stage (it updates self.compete_in)
        :return: In case there is an odd number of players, it returns the group that doesn't have anyone to compete with,
                 otherwise - it returns None
                 Maybe: return a list of pairs who lost the game to compete each other just for fun
        """
        odd_player = None

        if len(self.participants_in) % 2 == 1:  # in case there is an odd number of players
            for player in self.participants_in:
                if not player.avoided_battle:
                    odd_player = player
                    player.avoided_battle = True
                    break

            if odd_player is None:  # everyone has already avoided a game, just pick one randomly
                for player in self.participants_in:  # reset
                    player.avoided_battle = False
                odd_player = choice(self.participants_in)
                odd_player.avoided_battle = True

        up_to = len(self.participants_in) if not odd_player else len(self.participants_in) - 1
        self.compete_in = [(self.participants_in[i], self.participants_in[i + 1]) for i in range(0, up_to, 2)]

        return odd_player

    def publish_pairs(self, odd_player, html_file_path):
        """
        Publishes the competitors who compete each other in the current stage
        It can edit index.html or edit an online Google sheets
        :param odd_player: The player who doesn't have someone to compete against (None if there isn's such a player)
        :param html_file_path: The path to the html file to publish the results at
        :return: None, it edits the index.html (and automatically pushes the content to Git)
        """
        # build the html table object
        table_html = """<table>
    <tr>
        <th>קבוצה א'</th>
        <th>קבוצה ב'</th>
    </tr>"""

        for pair in self.compete_in:
            table_html += """
    <tr>
        <td>""" + pair[0].group_name + """
        <td>""" + pair[1].group_name + """
    </tr>"""
        table_html += "\n</table>"

        # append the table to the site
        with open(html_file_path, "r", encoding="utf8") as the_web:
            web_content = the_web.read()

        with open(html_file_path, "w", encoding="utf8") as the_web:
            before = web_content.index("<table>")
            after = web_content.index("</table>") + len("</table>")
            total = web_content[:before] + table_html + web_content[after:]
            the_web.write(total)

    def update_google_form(self):
        """
        Prints to the screen the name of the winning competitors - so the program's runner can copy those names
        and paste them in the Google forms that asks who won the current game
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
        content = pd.read_excel(file_path).to_dict()
        print("content:", content["איזה זוג ניצח מביניכם?"].values())

        for winner in content["איזה זוג ניצח מביניכם?"].values():
            win_player = self.find_competitor(group_name=winner)
            if win_player:
                win_player.won = True
            else:
                raise Exception("Competitor group '" + winner + "' was not found in the participants list")

        print("Compete in:", self.compete_in)
        for p1, p2 in self.compete_in:
            win_player, lost = (p1, p2) if p1.won else (p2, p1)

            print("win_player:", str(win_player), "lost:", str(lost))
            self.participants_in.remove(lost)
            self.participants_out += [lost]

            lost.won = win_player.won = False


        #for winner in content["איזה זוג ניצח מביניכם?"]:
        #    for pair in self.compete_in:
        #        if winner in pair:
        #            loser = self.pop_competitor(group_name=(pair[0] if pair[0] != winner else pair[1]))
        #            if loser is not None:
        #                self.participants_out += [loser]
        #            else:
        #                raise Exception("Competitor not found competitors list")
        #            break

    def find_competitor(self, group_name: str):
        """
        Returns the object of the wanted group by the group's name
        :param group_name: the name of the group
        :return: the object of the wanted group or None if not found
        """
        the_group = None

        for group in self.participants_in:
            if group.group_name == group_name:
                the_group = group
                break

        if not the_group:
            for group in self.participants_out:
                if group.group_name == group_name:
                    the_group = group
                    break

        return the_group

    def pop_competitor(self, group_name: str):
        """
        Find a competitor by the group name and pop it from the self.participants_in array
        :param group_name: The name of the group to pop
        :return: The object of the group that was just popped
        """
        i = 0
        for comp in self.participants_in:
            if group_name == comp.group_name:
                return self.participants_in.pop(i)
            i += 1

        return None
