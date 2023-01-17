"""
Module for DialogWindow class.
"""

import tkinter as tk
from tkinter import filedialog
import shutil
from gui.browser import search_for_logo
from src.constants import (
    EXC_TEXT_COLOR,
    ISSUE_WITH_LOGO_COLOR,
    IMPORT_FILE_COLOR
)


class DialogWindow:
    """This is a class for creating a DialogWindow widget using a tkinter GUI.
    The DialogWindow consists of a text frame and various buttons or entry text field.
    Class can print exceptions or handle other issues as importing images etc.

    Attributes:
        root (tk.TK): Tkinter root.
        frame (tk.Frame): Frame where dialog window is placed.
        text (tk.Text): Text window.
        result (bool): Variable as return value from method using buttons. 
        entry_text (str): Variable as return value from entry text field. 
    """
    def __init__(self, root):
        """Initializes the DialogWindow widget and sets default parameters.

        Parameters:
            root (tkinter.Tk): The parent widget for the DialogWindow.
        """

        self.root = root

        self.frame = tk.Frame(self.root)
        self.frame.grid(row = 0, column = 7, rowspan=4)
        self.frame.configure(width=100, height=200)

        self.text = tk.Text(self.frame, font=("Arial", 14))
        self.text.pack()
        self.text.configure(width=30, height=20)

        self.result = None
        self.entry_text = None

    def print_text(self, text):
        """Simply prints text to the text frame.

        Parameters:
            text (str): The text to be printed.
        """

        self.text.insert(tk.INSERT, text + "\n")

    def print_exception(self, text):
        """Simply prints exception to the text frame
        with changed color.

        Parameters:
            text (str): The text to be printed.
        """

        n = len(text)
        self.text.insert(tk.INSERT, text + "\n")
        start_pos = self.text.index(f"end-{n+2}c")
        self.text.tag_config("red", foreground=EXC_TEXT_COLOR)
        self.text.tag_add("red", start_pos, "end")
        self.text.tag_remove("red", "end-1c", "end")

    def issue_with_logo(self, text, team_name, destination):
        """Prints a message and creates a dialog box with options
        to open a browser, import a logo, or continue without a logo.

        Parameters:
            text (str): The text to be displayed.
            team_name (str): The name of the team.
            destination (str): The file path where the logo should be saved.

        Returns:
            bool: True if the user chooses to continue without a logo, False otherwise.
        """

        self.text.insert(tk.INSERT, "===========================\n")
        n = len(text)
        self.text.insert(tk.INSERT, text + "\n")
        start_pos = self.text.index(f"end-{n+2}c")
        self.text.tag_config("green", foreground=ISSUE_WITH_LOGO_COLOR)
        self.text.tag_add("green", start_pos, "end")
        self.text.tag_remove("green", "end-1c", "end")
        self.text.insert(tk.INSERT, "===========================\n")

        self.result = None
        def browser():
            """Calls the function from browser.py to open the browser.
            """
            search_for_logo(team_name)

        def import_file(tmp_frame):
            """Opens a file dialog for the user to select a file to import.
            If the file is in .png format, it is copied to the specified destination
            and the dialog is destroyed.
            If not, an error message is printed.

            Parameters:
                tmp_frame (tk.Frame): A reference to the temporary frame
                where the buttons are displayed.
            """

            self.result = False
            source = filedialog.askopenfilename()
            if source.endswith(".png"):
                shutil.copy(source, destination)
                tmp_frame.destroy()
            else:
                self.print_text("Imported file is not in .png!")

        def without_logo(tmp_frame):
            """Sets the result to True and destroys the temporary frame.

            Parameters:
                tmp_frame (tk.Frame): A reference to the temporary frame
                where the buttons are displayed.
            """

            self.result = True
            tmp_frame.destroy()

        tmp_frame = tk.Frame(self.frame)
        tmp_frame.pack(side=tk.BOTTOM)
        browser_button = tk.Button(tmp_frame, text="Open browser", command=browser)
        browser_button.pack(side = tk.TOP)
        import_button = tk.Button(tmp_frame, text="Import logo", command=lambda: import_file(tmp_frame))
        import_button.pack(side = tk.TOP)
        continue_button = tk.Button(tmp_frame, text="Continue without logo", command=lambda: without_logo(tmp_frame))
        continue_button.pack(side = tk.TOP)
        self.frame.wait_window(tmp_frame)
        return self.result

    def yes_no(self, text, true = "Yes", false = "No"):
        """This function displays a Yes/No dialog window in the GUI
        and returns a boolean value indicating the user's choice.

        Args:
            text (str): The text to be displayed.
            true (str, optional): The label for the yes_button. Default is "Yes".
            false (str, optional): The label for the no_button. Default is "No".

        Returns:
            bool: True if the yes_button is clicked, False if the no_button is clicked.
        """

        self.print_text(text)
        self.result = None
        def yes_clicked(tmp_frame):
            self.result = True
            tmp_frame.destroy()

        def no_clicked(tmp_frame):
            self.result = False
            tmp_frame.destroy()

        tmp_frame = tk.Frame(self.frame)
        tmp_frame.pack(side=tk.BOTTOM)
        yes_button = tk.Button(tmp_frame, text=true, command=lambda: yes_clicked(tmp_frame))
        yes_button.pack(side = tk.TOP)
        no_button = tk.Button(tmp_frame, text=false, command=lambda: no_clicked(tmp_frame))
        no_button.pack(side = tk.TOP)
        self.root.wait_window(tmp_frame)
        return self.result

    def import_file(self, text, destination):
        """Display a dialog window with two buttons: "Import image"
        and "Continue without image".
        The .png file is be copied to the specified `destination`.

        Parameters:
            text (str): Text to be displayed.
            destination (pathlib.Path): Destination file path for the imported file

        Returns:
            bool: True if the user chose to continue without image, False otherwise.
        """

        self.text.insert(tk.INSERT, "===========================\n")
        n = len(text)
        self.text.insert(tk.INSERT, text + "\n")
        start_pos = self.text.index(f"end-{n+2}c")
        self.text.tag_config("green", foreground=IMPORT_FILE_COLOR)
        # Use this position to specify the start and end of the tag
        self.text.tag_add("green", start_pos, "end")
        self.text.tag_remove("green", "end-1c", "end")
        self.text.insert(tk.INSERT, "===========================\n")

        self.result = None

        def import_file(tmp_frame):
            self.result = False
            source = filedialog.askopenfilename()
            if source.endswith(".png"):
                shutil.copy(source, destination)
                tmp_frame.destroy()
            else:
                self.print_text("Imported file is not in .png!")

        def without_logo(tmp_frame):
            self.result = True
            tmp_frame.destroy()

        tmp_frame = tk.Frame(self.frame)
        tmp_frame.pack(side=tk.BOTTOM)
        import_button = tk.Button(tmp_frame, text="Import image", command=lambda: import_file(tmp_frame))
        import_button.pack(side = tk.TOP)
        continue_button = tk.Button(tmp_frame, text="Continue without image", command=lambda: without_logo(tmp_frame))
        continue_button.pack(side = tk.TOP)
        self.frame.wait_window(tmp_frame)
        return self.result

    def entry_new_text(self, text):
        """Display a dialog window with entry field text.

        Parameters:
            text (str): Text to be displayed.

        Returns:
            str: The text that was inserted.
        """

        self.print_text(text)
        self.entry_text = None
        tmp_frame = tk.Frame(self.frame)
        tmp_frame.pack(side=tk.BOTTOM)
        entry = tk.Entry(tmp_frame)
        entry.pack(side = tk.TOP)

        def get_text(event):
            # Get the text from the Entry widget
            self.entry_text = entry.get()
            tmp_frame.destroy()

        # Bind the Entry widget to a function that is called when the user hits the Return key
        entry.bind("<Return>", get_text)
        self.frame.wait_window(tmp_frame)
        return self.entry_text
