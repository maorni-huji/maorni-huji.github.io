# This file calculates who plays verses who and saves the results in it according to the users' reports
import pandas as pd
from random import choice, shuffle
from colorama import Fore, Style
import os

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
# InfinityFree account and Website:
# main page - https://dash.infinityfree.com/accounts (go to the control panel to edit the web)
# website - https://maornimri45.infinityfreeapp.com/
#
# (Not updated) GitHub Website:
# https://maorni-huji.github.io/
# edit the website by editing index.html and push it to GitHub (maorni-huji.github.io)


class Competitor:
    DEFAULT_PARTICIPANTS = r"C:\Users\TLP-001\PycharmProjects\ShabatMadat\Server\participants.xlsx"
    DEFAULT_WINNERS = r"C:\Users\TLP-001\PycharmProjects\ShabatMadat\Server\winners.xlsx"

    def __init__(self, comp_names: list[str]):
        self.group_name = Competitor.edit_group_name(comp_names)
        self.avoided_battle = False
        self.won = False
        self.score = 0  # inner score, used for the system decisions of who plays verses who (it doesn't say who wins)

        if 0 == len(comp_names):  # should never happen
            raise Exception("error - illegal group details")

    @staticmethod
    def edit_group_name(comp_names: list[str]):
        return "הקבוצה של: " + ", ".join(comp_names)

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
        Parses the participants google form answers into python object,
        and decide who are the couples that will compete together
        :param file_path: The participants' Excel file location
        :return: None, it updates the class's variable itself
        """
        self.participants_in = []
        comp_names = []

        content = pd.read_excel(file_path).to_dict()

        for i in range(len(content["איך קוראים לך?"])):
            if isinstance(content["איך קוראים לך?"][i], str):
                comp_names += [content["איך קוראים לך?"][i]]
            # comp_names = [user for user in [content["משתתף 1"][i], content["משתתף 2"][i], content["משתתף 3 (רק באישור שלנו)"][i]] if isinstance(user, str)]
            # self.participants_in += [Competitor(comp_names=comp_names, group_name=content["שם הקבוצה"][i])]

        shuffle(comp_names)

        if len(comp_names) % 2 == 0:
            self.participants_in = [Competitor(comp_names=[comp_names[i], comp_names[i + 1]])
                                    for i in range(0, len(comp_names), 2)]
        else:  # there is one group with 3 participants
            self.participants_in = [Competitor(comp_names=[comp_names[i], comp_names[i + 1]])
                                    for i in range(0, len(comp_names) - 1, 2)]
            self.participants_in[0] = Competitor(comp_names=[comp_names[0], comp_names[1], comp_names[-1]])

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

    def publish_pairs(self, odd_player, html_file_path,
                      upload_to_github: bool = False, game_token: str = "", stage_num: int = 0):
        """
        Publishes the competitors who compete each other in the current stage
        It can edit index.html or edit an online Google sheets
        :param odd_player: The player who doesn't have someone to compete against (None if there isn's such a player)
        :param html_file_path: The path to the html file to publish the results at
        :param upload_to_github: Whether to upload the site to GitHub or just change it locally
        :param game_token: a unique token of the current tournament to be added to the git commits
        :param stage_num: the number of the current stage
        :return: None, it edits the index.html (and automatically pushes the content to Git)
        """
        # build the html table object
        table_html = """<table>
    <tr>
        <th>קבוצה א'</th>
        <th>קבוצה ב'</th>
    </tr>"""
        google_form_view = ""

        i = 1
        for pair in self.compete_in:
            table_html += """
    <tr>
        <td>""" + pair[0].group_name + """</td>
        <td>""" + pair[1].group_name + """</td>
    </tr>"""
            google_form_view += str(i) + ".  " + pair[0].group_name + " --- VS --- " + pair[1].group_name + "\n"
            i += 1

        if odd_player:
            table_html += """
    <tr>
        <td>""" + odd_player.group_name + """</td>
        <td>אוטומטית עולה לסיבוב הבא (מזליסטים)</td>
    </tr>"""
            google_form_view += str(i) + ".  " + odd_player.group_name + "  --- VS --- עולה אוטמטית לסיבוב הבא (מזליסטים), אין צורך שתמלאו את הפורם הסיבוב" + "\n"

        table_html += "\n</table>"

        # append the table to the site
        with open(html_file_path, "r", encoding="utf8") as the_web:
            web_content = the_web.read()

        with open(html_file_path, "w", encoding="utf8") as the_web:
            before = web_content.index("<table>")
            after = web_content.index("</table>") + len("</table>")
            total = web_content[:before] + table_html + web_content[after:]
            the_web.write(total)

        # upload the site to GitHub
        # if upload_to_github:
        #     Tournament.upload_site_to_github(game_token, stage_num)

        return google_form_view

    @staticmethod
    def upload_site_to_github(game_token: str, stage_num: int):
        """
        It uploads index.html to Github using push requests, so everyone can access it in https://maorni-huji.github.io/
        This action should be run from ShabatMadat directory, not from one of its subdirectories
        :param game_token: a unique token of the current tournament to be added to the git commits
        :param stage_num: the number of the current stage
        :return: None
        """
        print(Fore.LIGHTMAGENTA_EX, end="")
        os.system("git add --all")
        os.system("git commit -m \"Committing index.html for Game {" + game_token + "}, Stage " + str(stage_num) + "\"")
        os.system("git push origin")
        print(Style.RESET_ALL, end="")

    def update_google_form(self):
        """
        Prints to the screen the name of the winning competitors - so the program's runner can copy those names
        and paste them in the Google forms that asks who won the current game
        :return: None, it prints the names of the self.participants_in to the screen
        """
        print("    Competitors who are currently in the game: ")
        for competitors in self.participants_in:
            print("    " + str(competitors))

    def fetch_winners(self, file_path=Competitor.DEFAULT_WINNERS, odd_player=None):
        """
        Parses the names of the winning groups (from Google forms) into the class,
        it just removes all of the participants who were not assigned as winners (and adds the losers to self.participants_out)
        :param file_path: The winner groups Excel file location
        :param odd_player: The player who didn't have competitor to compete against and automatically wins
        :return: A list of groups that were both assigned as winners or both losers (by mistake)
        """
        mistaken_groups = []
        content = pd.read_excel(file_path).to_dict()

        for winner in content["איזה זוג ניצח מביניכם?"].values():
            if isinstance(winner, str):
                win_player = self.find_competitor(group_name=winner)
                if win_player:
                    win_player.won = True
                elif not odd_player or odd_player.group_name != winner:
                    print("Competitor group '" + winner + "' was not found in the participants list, SHOULDN'T HAPPEN")

        for p1, p2 in self.compete_in:
            if (p1.won and not p2.won) or (not p1.won and p2.won):
                win_player, lost = (p1, p2) if p1.won else (p2, p1)
                self.participants_in.remove(lost)
                self.participants_out += [lost]
                lost.won = win_player.won = False
            else:
                mistaken_groups += [(p1, p2)]

        return mistaken_groups

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

    def is_done(self):
        """
        Checks if the tournament is done or not and return the winner
        :return: A Competitor object of the winner, or None if the competitor is not done
        """
        if len(self.participants_in) == 1:
            return self.participants_in[0]
        else:
            return None

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
