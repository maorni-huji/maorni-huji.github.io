import time
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
from snake_platform import HOST_WINS, OPPONENT_WINS

WHO_WON_FORMS_LINK = r"https://forms.gle/49FchrWEK4fFDqqV6"
SNAKES_COLOSSEUM_URL = r"https://drive.google.com/drive/folders/1sJMEhsJzmbQkYU-9tGrXqqiutBIZ5t3x?usp=sharing"

# TODO:
# 1. Change the hash to the updated snake_platform.py hash
# 2. When the game ends, tell which snake wins - INCLUDING whether it is the HOST or the OPPONENT


def browse_file(button_var, entry_var):
    """
    Browses the file from the user's file explorer
    :param button_var: The button to change its text to the wanted file
    :param entry_var: Variable to save the address at
    :return: None
    """
    file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")], initialdir=r"C:\Users\TLP-001\Downloads")
    if "/" in file_path:
        button_var.config(text="Play VS " + file_path[file_path.rindex("/") + 1:])
        ttk.Style().configure("button4.TButton", background="green", foreground="green")
        ttk.Style().configure("RunButton.TButton", background="red", foreground="red")
    entry_var.set(file_path)


def open_in_google(url):
    webbrowser.open_new(url)


def run_game(opponent_script_path, is_real):
    """
    Runs the game with the opponent's script
    :param opponent_script_path: The path to the opponent's script python file
    :param is_real: Is it a real game against an opponent whose script was just uploaded (True) or a demo game for training (False)
    :return: The winner - HOST_WINS or OPPONENT_WINS
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

        return winner


def end_game_popup(winner):
    """
    Popup a new gui window to the user that asks him / her to say who won in the Google forms
    :param winner: Who won - HOST_WINS or OPPONENT_WINS
    :return: None
    """
    root = tk.Tk()
    root.title("Game Winner")

    # Create a frame for better organization
    frame = ttk.Frame(root, padding=10, style='TFrame')
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Configure style for the frame
    background_color = '#b3e6ff' if HOST_WINS == winner else '#80ff80'
    foreground_color = '#005580' if HOST_WINS == winner else '#006600'
    root.style = ttk.Style()
    root.style.configure('TFrame', background=background_color)

    # Title label
    title_text = "The Host Snake Won The Game!" if HOST_WINS == winner else "The Guest Snake Won The Game!"
    title_label = ttk.Label(frame, text=title_text, font=('Helvetica', 18), style='TLabel',
                            background=background_color, foreground=foreground_color)
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

    # Configure style for the label
    root.style.configure('TLabel', foreground='black')

    # Instruction label
    inst_label = ttk.Label(frame, text="Please tell us the names of the winners here:", font=('Helvetica', 15),
                           style='TLabel', background=background_color, foreground=foreground_color)
    inst_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))

    # Create a button
    button = ttk.Button(frame, text="Open Google Forms", command=lambda url=WHO_WON_FORMS_LINK: open_in_google(url),
                        style='TButton')
    button.grid(row=2, column=0, columnspan=2)

    # Configure style for the button
    root.style.configure('TButton', background='black', foreground='black', font=('Helvetica', 14))  # Green background, white text

    # Adjust column weights for better resizing
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)

    # Run the main loop
    root.mainloop()


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
    root.geometry("540x564")  # Set window size

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
    run_button = ttk.Button(main_frame, text="Run Training Game", command=lambda: on_run_game(entry_var.get(), is_real=False), style=run_button_style)
    run_button.grid(row=3, column=0, pady=20, columnspan=2)

    # real game
    label = ttk.Label(main_frame, text="Play Against Different Green Snake, Designed by Others:", font=('Helvetica', 14), style="Title.TLabel")
    label.grid(row=4, column=0, pady=10, columnspan=1)

    entry_var = tk.StringVar()  # save the file address

    button_style = "BrowseButton.TButton"

    run_button_style = "RunButton.TButton"
    button1 = ttk.Button(root, text="Run Game", command=lambda entry=entry_var: on_run_game(entry.get(), is_real=True),
                               style=run_button_style)
    button1.grid(row=6, column=0, pady=10, padx=10)

    button2 = ttk.Button(main_frame, text="1. Who is My Opponent?", command=lambda url="https://forms.gle/49FchrWEK4fFDqqV6": open_in_google(url),
                                     style=button_style)
    button2.grid(row=7, column=0, pady=10, padx=10)

    button3 = ttk.Button(main_frame, text="2. Download Opponent's Snake", command=lambda url=SNAKES_COLOSSEUM_URL: open_in_google(url),
                                     style=button_style)
    button3.grid(row=8, column=0, pady=10, padx=10)

    button4 = ttk.Button(main_frame, text="3. Upload Opponent's Snake", command=None, style="button4.TButton")
    button4.config(command=lambda button=button4: browse_file(button, entry_var))
    button4.grid(row=10, column=0, pady=10, padx=10)

    # choose FPS
    selected = tk.StringVar(root)
    selected.set("10 FPS")  # Set the default option

    # Create an OptionMenu widget
    options_list = ["5 FPS", "10 FPS", "20 FPS", "30 FPS", "50 FPS"]
    option_menu = tk.OptionMenu(root, selected, *options_list, command=None)
    option_menu.grid(row=9, column=0, pady=10, columnspan=2, sticky="e")

    # Style configurations
    root.style = ttk.Style()
    root.style.configure("Main.TFrame", background="#006400", foreground="yellow")  # Dark green background, white text
    root.style.configure("Title.TLabel", background="#006400", foreground="white")
    root.style.configure("Title1.TLabel", background="#006400", foreground="yellow")
    root.style.configure("Title2.TLabel", background="#006400", foreground="lightblue")
    root.style.configure("Entry.TEntry", background="white", foreground="black")
    root.style.configure("DemoButton.TButton", padding=(10, 5), font=('Helvetica', 12), background="#cc6600", foreground="#cc6600")
    root.style.configure("BrowseButton.TButton", padding=(10, 5), font=('Helvetica', 12), background="purple", foreground="purple")  # Dark red
    root.style.configure("RunButton.TButton", padding=(10, 5), font=('Helvetica', 12), background="black", foreground="black")  # Dark red
    root.style.configure("button4.TButton", padding=(10, 5), font=('Helvetica', 12), background="purple", foreground="purple")  # Dark red

    def on_run_game(opponent_script_path, is_real):
        # make sure that the snake_platform file wasn't changed
        with open("snake_platform.py", "r") as snake_platform_file:
            # print("sha256: ", sha256_hash(snake_platform_file.read().encode()))

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
            winner = run_game(opponent_script_path, is_real)
            if is_real:
                end_game_popup(winner)
            # time.sleep(3)

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