from Server.tournament import Tournament


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
            tournament.choose_pairs()
            tournament.publish_pairs()

        elif "UPDATE_IN" == command:
            tournament.update_google_form()

        elif "EDIT_GROUP" == command:
            pass

        elif "EXIT" != command:
            print(" < Unknown command")

    print(" > Bye bye")