import time
import tkinter as tk
from tkinter import ttk, filedialog


def browse_file(entry_var):
    """
    Browses the file from the user's file explorer
    :param entry_var: The entry var to save the file's address at
    :return: None
    """
    file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py"), ("All files", "*.*")])
    entry_var.set(file_path)


def run_game(opponent_script_path):
    """
    Runs the game with the opponent's script
    :param opponent_script_path: The path to the opponent's script python file
    :return: None
    """
    print(f"Running game with opponent's script: {opponent_script_path}")


def upload_opponent_file():
    """
    Runs the GUI that asks the user to enter his / her opponent's script,
    this function should be called first - and it calls the other functions that run the game
    :return: None
    """
    root = tk.Tk()
    root.title("The Snake Game")

    # Styling with dark green background and white text
    root.configure(bg="#006400")  # Dark green background
    root.geometry("400x200")  # Set window size

    main_frame = ttk.Frame(root, padding=(20, 10), style="Main.TFrame")
    main_frame.grid(row=0, column=0)

    label = ttk.Label(main_frame, text="Select Opponent's Script:", font=('Helvetica', 14), style="Title.TLabel")
    label.grid(row=0, column=0, pady=10, sticky="w")

    entry_var = tk.StringVar()
    entry = ttk.Entry(main_frame, textvariable=entry_var, width=40, font=('Helvetica', 12), style="Entry.TEntry")
    entry.grid(row=1, column=0, pady=10, columnspan=2, sticky="w")

    browse_button_style = "BrowseButton.TButton"
    browse_button = ttk.Button(main_frame, text="Browse", command=lambda: browse_file(entry_var), style=browse_button_style)
    browse_button.grid(row=1, column=1, pady=10, padx=10, sticky="e")

    run_button_style = "RunButton.TButton"
    run_button = ttk.Button(main_frame, text="Run Game", command=lambda: on_run_game(entry_var.get()), style=run_button_style)
    run_button.grid(row=2, column=0, pady=20, columnspan=2)

    # Style configurations
    root.style = ttk.Style()
    root.style.configure("Main.TFrame", background="#006400", foreground="white")  # Dark green background, white text
    root.style.configure("Title.TLabel", background="#006400", foreground="white")
    root.style.configure("Entry.TEntry", background="white", foreground="black")
    root.style.configure("BrowseButton.TButton", padding=(10, 5), font=('Helvetica', 12), background="#8B0000", foreground="red")  # Dark red
    root.style.configure("RunButton.TButton", padding=(10, 5), font=('Helvetica', 12), background="#8B0000", foreground="red")  # Dark red

    def on_run_game(opponent_script_path):
        # Destroy the GUI window before calling run_game
        root.destroy()
        run_game(opponent_script_path)

    root.mainloop()

# Uncomment the line below to test the GUI
# upload_opponent_file()
