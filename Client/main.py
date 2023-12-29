import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import snake_platform
from colorama import Fore, Style
import webbrowser
import logging
from datetime import datetime
import hashlib
from os.path import isfile
import os

# TODO:
# 1. Change the hash to the updated snake_platform.py hash
# 2. Set the maximum amount of "time" to 90 * FPS (instead of 900)
# 3. When the game ends, tell which snake wins - INCLUDING whether it is the HOST or the OPPONENT
# 4. At the end of a real game, open a new gui window containing the link to the who-won-the-game forms


def browse_file(entry_var):
    """
    Browses the file from the user's file explorer
    :param entry_var: The entry var to save the file's address at
    :return: None
    """
    file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py"), ("All files", "*.*")])
    entry_var.set(file_path)


def open_in_google(url):
    webbrowser.open_new(url)


def run_game(opponent_script_path, is_real):
    """
    Runs the game with the opponent's script
    :param opponent_script_path: The path to the opponent's script python file
    :param is_real: Is it a real game against an opponent whose script was just uploaded (True) or a demo game for training (False)
    :return: None
    """
    # this function can copy the given file's data and create the wanted opponent's file by itself,
    # after the game it needs to remove the file it created to prevent collisions
    if not is_real:  # demo game for training your snake
        print(Fore.MAGENTA, f"Running demo game against default_snake.py", Style.RESET_ALL,
              "\nYou are the ", Fore.BLUE, "blue snake", Style.RESET_ALL,
              " and default_snake.py's snake is the ", Fore.GREEN, "green snake", Style.RESET_ALL, ".", sep="")

        # run the game
        winner = snake_platform.run_snakes_game(is_real)
        if snake_platform.HOST_WINS == winner:
            print(Fore.BLUE, "Your Snake Has Won The Game!", Style.RESET_ALL, sep="")
        else:
            print(Fore.GREEN, "You Lost This Time, The Default Snake Has Won The Game...", Style.RESET_ALL, sep="")

    else:  # real game - against another competitor
        print(Fore.MAGENTA, f"Running game with opponent's script: {opponent_script_path}", Style.RESET_ALL,
              "\nThe host is the ", Fore.BLUE, "blue snake", Style.RESET_ALL,
              " and the guest is the ", Fore.GREEN, "green snake", Style.RESET_ALL, ".", sep="")

        # read the opponent's script
        opponent_data = ""
        with open(opponent_script_path, "r") as opponent_script:
            opponent_data = opponent_script.read()

        logging.basicConfig(filename="actions.log", filemode="a", format=" >> %(message)s", level=logging.INFO)
        logging.info(
            "<<<<<<<<<<<<< STARTING NEW SNAKES GAME :: " + datetime.now().strftime("%H:%M:%S") + " >>>>>>>>>>>>>>")
        logging.info("Opponent Script Path: " + opponent_script_path)

        # upload the opponent's script
        current_directory = str(Path(__file__))
        if "\\" in current_directory:
            current_directory = current_directory[:current_directory.rindex("\\")]
        elif "/" in current_directory:
            current_directory = current_directory[:current_directory.rindex("/")]
        else:
            raise Exception("ERROR Reading the file path - call the Superiors")

        with open(current_directory + "\\opponent_snake.py", "w") as opponent_file:
            opponent_file.write(opponent_data)

        # run the game
        winner = snake_platform.run_snakes_game(is_real)

        if snake_platform.HOST_WINS == winner:
            print(Fore.BLUE, "The Blue Snake (This Computer's Code) Wins!", Style.RESET_ALL, sep="")
        else:
            print(Fore.GREEN, "The Green Snake (The Guest's Code) Wins!", Style.RESET_ALL, sep="")


def main():
    """
    Runs the GUI that asks the user to enter his / her opponent's script,
    this function should be called first - and it calls the other functions that run the game
    :return: None
    """
    root = tk.Tk()
    root.title("The Snake Game")

    # Styling with dark green background and white text
    root.configure(bg="#006400")  # Dark green background
    root.geometry("534x510")  # Set window size

    main_frame = ttk.Frame(root, padding=(20, 10), style="Main.TFrame")
    main_frame.grid(row=0, column=0)

    # heading
    title = ttk.Label(main_frame, text="The Snake Game", font=('Helvetica', 18), style="Title1.TLabel")
    title.grid(row=0, column=0, pady=10, columnspan=2)

    title2 = ttk.Label(main_frame, text="Blue (Host) VS Green (Opponent)", font=('Helvetica', 16), style="Title2.TLabel")
    title2.grid(row=1, column=0, pady=10, columnspan=2)

    # demo game
    label1 = ttk.Label(main_frame, text="Run Training Game Against default_snake.py:", font=('Helvetica', 14), style="Title.TLabel")
    label1.grid(row=2, column=0, pady=10, columnspan=2)

    run_button_style = "DemoButton.TButton"
    run_button = ttk.Button(main_frame, text="Run Demo Game", command=lambda: on_run_game(entry_var.get(), is_real=False), style=run_button_style)
    run_button.grid(row=3, column=0, pady=20, columnspan=2)

    # real game
    label = ttk.Label(main_frame, text="To Start The Real Game, Upload Your Opponent's Script:", font=('Helvetica', 14), style="Title.TLabel")
    label.grid(row=4, column=0, pady=10, columnspan=1)

    entry_var = tk.StringVar()
    entry = ttk.Entry(main_frame, textvariable=entry_var, width=40, font=('Helvetica', 12), style="Entry.TEntry")
    entry.grid(row=6, column=0, pady=20, columnspan=2)

    run_button_style = "Competitors.TButton"
    competitors_link = ttk.Button(root, text="But Who is My Opponent?", cursor="hand2",
                                  command=lambda url="https://forms.gle/49FchrWEK4fFDqqV6": open_in_google(url),
                                  style=run_button_style)
    competitors_link.grid(row=5, column=0, pady=10, columnspan=2)

    browse_button_style = "BrowseButton.TButton"
    browse_button = ttk.Button(main_frame, text="Browse", command=lambda: browse_file(entry_var), style=browse_button_style)
    browse_button.grid(row=6, column=0, pady=10, padx=10, sticky="e")

    run_button_style = "RunButton.TButton"
    run_button = ttk.Button(main_frame, text="Run Game", command=lambda: on_run_game(entry_var.get(), is_real=True), style=run_button_style)
    run_button.grid(row=7, column=0, pady=10, columnspan=2)

    # choose FPS
    selected = tk.StringVar(root)
    selected.set("10 FPS")  # Set the default option

    # Create an OptionMenu widget
    options_list = ["5 FPS", "10 FPS", "20 FPS", "30 FPS", "50 FPS"]
    option_menu = tk.OptionMenu(root, selected, *options_list, command=None)
    option_menu.grid(row=7, column=0, pady=10, columnspan=2, sticky="e")

    # Style configurations
    root.style = ttk.Style()
    root.style.configure("Main.TFrame", background="#006400", foreground="yellow")  # Dark green background, white text
    root.style.configure("Title.TLabel", background="#006400", foreground="white")
    root.style.configure("Title1.TLabel", background="#006400", foreground="yellow")
    root.style.configure("Title2.TLabel", background="#006400", foreground="lightblue")
    root.style.configure("Entry.TEntry", background="white", foreground="black")
    root.style.configure("DemoButton.TButton", padding=(10, 5), font=('Helvetica', 12), background="black", foreground="black")
    root.style.configure("BrowseButton.TButton", padding=(10, 5), font=('Helvetica', 12), background="#8B0000", foreground="red")  # Dark red
    root.style.configure("RunButton.TButton", padding=(10, 5), font=('Helvetica', 12), background="#8B0000", foreground="red")  # Dark red
    root.style.configure("Competitors.TButton", padding=(10, 5), font=('Helvetica', 12), background="purple", foreground="purple")  # Dark red

    def on_run_game(opponent_script_path, is_real):
        # make sure that the snake_platform file wasn't changed
        with open("snake_platform.py", "r") as snake_platform_file:
            if sha256_hash(snake_platform_file.read().encode()) != '5cc3c8ddb0d3f4bd6e86ddc254440ccd00d15ba2eaf07aa1a681b84ef1caa266':  # CHANGE THIS
                if not is_real:
                    label1.config(text="Oops!\nIt seems like snake_platform.py was accidentally edited.\nTry to re-download the file from GitHub", foreground="#ff6666")
                else:
                    label.config(text="Oops!\nIt seems like snake_platform.py was accidentally edited.\nTry to re-download the file from GitHub", foreground="#ff6666")
                return

        if is_real and not isfile(opponent_script_path):
            label.config(text="Couldn't find the file specified, try to upload the correct file", foreground="#ff6666")

        # Destroy the GUI window before calling run_game
        else:
            snake_platform.FPS = int(selected.get().split()[0])  # game FPS
            root.destroy()
            run_game(opponent_script_path, is_real)

    root.mainloop()


def sha256_hash(data):
    # Create a new SHA-256 hash object
    sha256 = hashlib.sha256()

    # Update the hash object with the bytes-like object (e.g., a string or bytes)
    sha256.update(data)

    # Get the hexadecimal representation of the hash
    hashed_data = sha256.hexdigest()

    return hashed_data


if "__main__" == __name__:
    main()
