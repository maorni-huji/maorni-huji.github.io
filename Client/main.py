import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import snake_platform
from colorama import Fore, Style
import webbrowser


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

        # upload the opponent's script
        current_directory = str(Path(__file__))
        if "\\" in current_directory:
            current_directory = current_directory[:current_directory.rindex("\\")]
        elif "/" in current_directory:
            current_directory = current_directory[:current_directory.rindex("/")]
        else:
            print("ERROR Reading the file path - call the Superiors")
            return

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
    root.geometry("540x430")  # Set window size

    main_frame = ttk.Frame(root, padding=(20, 10), style="Main.TFrame")
    main_frame.grid(row=0, column=0)

    # heading
    title = ttk.Label(main_frame, text="The Snake Game", font=('Helvetica', 18), style="Title1.TLabel")
    title.grid(row=0, column=0, pady=10, columnspan=2)

    # demo game
    label1 = ttk.Label(main_frame, text="Run Training Game Against default_snake.py:", font=('Helvetica', 14), style="Title.TLabel")
    label1.grid(row=1, column=0, pady=10, columnspan=2)

    run_button_style = "DemoButton.TButton"
    run_button = ttk.Button(main_frame, text="Run Demo Game", command=lambda: on_run_game(entry_var.get(), is_real=False), style=run_button_style)
    run_button.grid(row=2, column=0, pady=20, columnspan=2)

    # real game
    label = ttk.Label(main_frame, text="To Start The Real Game, Upload Your Opponent's Script:", font=('Helvetica', 14), style="Title.TLabel")
    label.grid(row=3, column=0, pady=10, columnspan=1)

    entry_var = tk.StringVar()
    entry = ttk.Entry(main_frame, textvariable=entry_var, width=40, font=('Helvetica', 12), style="Entry.TEntry")
    entry.grid(row=5, column=0, pady=20, columnspan=2)

    run_button_style = "Competitors.TButton"
    competitors_link = ttk.Button(root, text="But Who is My Opponent?", cursor="hand2",
                                  command=lambda url="https://forms.gle/49FchrWEK4fFDqqV6": open_in_google(url),
                                  style=run_button_style)
    competitors_link.grid(row=4, column=0, pady=10, columnspan=2)

    browse_button_style = "BrowseButton.TButton"
    browse_button = ttk.Button(main_frame, text="Browse", command=lambda: browse_file(entry_var), style=browse_button_style)
    browse_button.grid(row=5, column=0, pady=10, padx=10, sticky="e")

    run_button_style = "RunButton.TButton"
    run_button = ttk.Button(main_frame, text="Run Game", command=lambda: on_run_game(entry_var.get(), is_real=True), style=run_button_style)
    run_button.grid(row=6, column=0, pady=10, columnspan=2)


    # Style configurations
    root.style = ttk.Style()
    root.style.configure("Main.TFrame", background="#006400", foreground="yellow")  # Dark green background, white text
    root.style.configure("Title.TLabel", background="#006400", foreground="white")
    root.style.configure("Title1.TLabel", background="#006400", foreground="yellow")
    root.style.configure("Entry.TEntry", background="white", foreground="black")
    root.style.configure("DemoButton.TButton", padding=(10, 5), font=('Helvetica', 12), background="black", foreground="black")
    root.style.configure("BrowseButton.TButton", padding=(10, 5), font=('Helvetica', 12), background="#8B0000", foreground="red")  # Dark red
    root.style.configure("RunButton.TButton", padding=(10, 5), font=('Helvetica', 12), background="#8B0000", foreground="red")  # Dark red
    root.style.configure("Competitors.TButton", padding=(10, 5), font=('Helvetica', 12), background="purple", foreground="purple")  # Dark red

    def on_run_game(opponent_script_path, is_real):
        # Destroy the GUI window before calling run_game
        if not (is_real and not opponent_script_path):
            root.destroy()
            run_game(opponent_script_path, is_real)

    root.mainloop()


if "__main__" == __name__:
    main()
