from Server.tournament import Tournament
from colorama import Fore, Style
from random import randint
import os

INDEX_HTML_PATH = r"index.html"


def server_control():
    """
    Controls the server by the program's runner
    :return: None
    """
    tournament = Tournament()
    command = ""

    print("Welcome to Server Control")

    while command != "EXIT":
        command = input("\n > Enter command: ")

        if "?" == command:  # show menu
            print("? - show list of commands",
                    "EXIT - exit the server control",
                    "FETCH_P - fetch participants from Google forms",
                    "SET_BATTLES - set the battles between the players",
                    "FETCH_W - fetch winning users from Google forms",
                    "UPDATE_IN - update the groups that are still in the game for Google forms",
                    "EDIT_GROUP - edit the details of a specific group",
                    sep="\n")

        elif "FETCH_P" == command or "FETCH_W" == command:
            path = input(" > Enter the location of the file to load data from: ")
            while input(" > Fetch " + ("participants" if "FETCH_P" == command else "winners") + "? (Y/N) ") != "Y":
                path = input(" > Enter the location of the file to load data from:")

            if "" != path:
                tournament.fetch_participants(path) if "FETCH_P" == command else tournament.fetch_winners(path)

            else:  # open default file
                tournament.fetch_participants() if "FETCH_P" == command else tournament.fetch_winners()

            print(" < " + ("participants" if "FETCH_P" == command else "winners") + " fetched successfully")

        elif "SET_BATTLES" == command:
            odd_player = tournament.choose_pairs()
            tournament.publish_pairs(odd_player=odd_player, html_file_path=INDEX_HTML_PATH,
                                     upload_to_github=True, game_token="Hand Server", stage_num=0)

        elif "UPDATE_IN" == command:
            tournament.update_google_form()

        elif "EDIT_GROUP" == command:
            pass

        elif "EXIT" != command:
            print(" < Unknown command")

    print(" > Bye bye")


def server_auto_control():
    """
    Runs the game automatically - as much as possible
    :return: None
    """
    tournament = Tournament()
    # os.system("cd ..")  # adjust for uploading the file process

    print(" >> Welcome to Server Auto Control\n"
          r"1. To start, make sure that the form https://docs.google.com/forms/d/1XQB1ZfV5IWo0DV9wPTN_Z5Djd7rPNp5p1mmdxkb0n0M/edit has no answers, and so as the table below in (3)" + "\n"
          r"2. Please send everyone the poll https://forms.gle/m8ocsvYgksHqcFy3A, so each one who competes would say so" + "\n"
          r"3. When everyone has answered the form, enter https://docs.google.com/spreadsheets/d/1eTYPuTH6OzPgOxFmy-78SW6aQ3jH9pkksxTKOlegOhU/edit?resourcekey#gid=443634803," + "\n"
          r"   and copy the whole table to C:\Users\TLP-001\PycharmProjects\ShabatMadat\Server\participants.xlsx" + "\n"
          r"*  NOTE: When dealing with local files, always close them after entering data, so the code can access them")
    wait()

    # start the game loop
    i = 1
    the_winner = tournament.is_done()
    while not the_winner:
        print(Fore.BLUE + "\n >> Stage " + str(i) + ":" + Style.RESET_ALL)

        # initialise winners form and publish the competitors
        print(r"  > Delete all of the answers from https://docs.google.com/forms/d/1bpUep3OJk6Lx0wG3vYGh91DKMyjE9XEtcPc_vk49U2k/edit and " + "\n"
              r"    from https://docs.google.com/spreadsheets/d/1IyzT8g9rnnWTDLsSvEwOAX9BEZAHkCDNzbdMkDwWO9s/edit?resourcekey#gid=1329863517" + "\n"
              r"  > Now, copy the following values into the first link above as the options of the question:")
        tournament.update_google_form()
        wait()

        odd_player = tournament.choose_pairs()
        google_form_competitors = tournament.publish_pairs(odd_player=odd_player, html_file_path=INDEX_HTML_PATH)

        print(r" > Alright, now - copy the following competitors into the description of https://docs.google.com/forms/d/1bpUep3OJk6Lx0wG3vYGh91DKMyjE9XEtcPc_vk49U2k/edit," + "\n",
              r"   So they would know who plays verses who (published in https://forms.gle/49FchrWEK4fFDqqV6), and change the title's stage to ", Fore.BLUE, "Stage ", i, Style.RESET_ALL, sep="")
        print(google_form_competitors)
        wait()
        print(r"  > Alright, now they can use the forms https://forms.gle/49FchrWEK4fFDqqV6 to say who wins")

        # fetch winners
        print(r"  > When the players have finished playing:" + "\n"
              r"  > Enter the table https://docs.google.com/spreadsheets/d/1IyzT8g9rnnWTDLsSvEwOAX9BEZAHkCDNzbdMkDwWO9s/edit?resourcekey#gid=1329863517," + "\n"
              r"    and copy its values to C:\Users\TLP-001\PycharmProjects\ShabatMadat\Server\winners.xlsx")
        wait()
        mistaken_groups, is_wrong = tournament.fetch_winners(odd_player=odd_player)

        while mistaken_groups or is_wrong:  # some groups were both assigned as losers or both assigned as winners (by a mistake)
            print(Fore.MAGENTA + "  > Some groups were not both assigned as winners or both as losers:")
            j = 1
            for mistaken_compete in mistaken_groups:
                print("   " + str(j) + ".", mistaken_compete[0], "vs", mistaken_compete[1])
                j += 1
            print("  > Find out what happens with them, and when you figure out who are the winners -\n"
                  r"    add their EXACT name to C:\Users\TLP-001\PycharmProjects\ShabatMadat\Server\winners.xlsx, or remove the loser's name" + Style.RESET_ALL)
            wait()
            mistaken_groups, is_wrong = tournament.fetch_winners(odd_player=odd_player)

        i += 1
        the_winner = tournament.is_done()

    print("Congratulations! The winner is", the_winner.group_name)


def server_quick_control():
    """
    Only splits the participants into pairs and prints instructions on the screen
    :return: None
    """
    tournament = Tournament()

    print(" >> Welcome to Server Auto Control - New\n"
          "    To start, make sure that participants.xlsx contains all of the participants' names")
    wait()
    tournament.fetch_participants()  # pair the participants randomly

    print(" >> Alright, the participants are in - now it's time to pair them! The pairs are:")
    tournament.update_google_form()
    print(r" >> Now:" + "\n"
          r" >> 1. Enter https://challonge.com/tournament/bracket_generator and create a new Double-Elimination tournament" + "\n"
          " >> 2. Copy the pairs from above and print them in the players segment, then continue the process and run the tournament\n"
          " >> 3. Check the box \"1 match\" in Settings -> Grand Finals\n"
          " >> 4. Copy the tournament's address\n"
          r" >> 5. Put that address in https://docs.google.com/forms/ both in the heading and in question 1" + "\n"                                                                                                                                        
          r" >> 6. Make sure there are no comments in the Google forms and in https://docs.google.com/spreadsheets/d/1SqH0sKSNJUqZslUzuj1489p5yemyMvLKWzZWHDWExVM/edit?resourcekey#gid=2132861224")
    wait()

    print("Alright, the tournament is ready - open the Excel file in (7) and the tournament in another tab, and follow answers")


def wait(continue_letter: str = 'Y'):
    """
    Waits until the server runner completes the assignment
    :param continue_letter: The letter the server runner should input to continue
    :return: None
    """
    while input(Fore.RED + " << Whenever you are ready, press " + continue_letter + ": " + Style.RESET_ALL) != continue_letter:
        continue
    # exit auto server control?
