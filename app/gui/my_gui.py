"""Module for the main GUI class.
"""

import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
from gui.checkbar import Checkbar
from gui.dialog_window import DialogWindow
from src.invite import Invite
from src.web_banner import WebBanner
from src.story import Story
from src.other_story import OtherStory
from src.database import InviteDatabase
from src.constants import (
    INVITE_DONE_PATH,
    WEB_DONE_PATH,
    FINAL_IMG_FOLDER,
    MUST_EXIST_FILES
)


class MyGUI:
    """MyGUI is a Tkinter GUI class for creating a graphical user interface
    for my app.

    Attributes:
        root (tk.TK): Tkinter root.
        icon (tk.PhotoImage): App icon.
        data (list(dict)): List of match data.
        title (tk.Label): Title on main page.
        stories_checkbar (Checkbar): Checkbar with stories options.
        invite_checkbar (Checkbar): Checkbar with invite options.
        dialog_window (DialogWindow): Dialog window for interacting with user.
    """
    def __init__(self, stories_list, data, root = None):
        self.root = root
        if not root:
            self.root = tk.Tk()

        icon = tk.PhotoImage(file = "../Elements/app_icon.png")
        root.iconphoto(False, icon)

        # -----------------------
        root.geometry("1100x700")
        # -----------------------

        self.data = data
        if len(data) > 4 or len(data) < 1:
            self.title = tk.Label(self.root, text="API data error.\n", font=("Arial", 30), fg="red")
            self.title.grid(row=0, column=0)
            tk.Button(self.root, text="Quit", command=self.root.quit).grid(row=1, column=0)
            return

        missing_files = self.files_prepared()
        if missing_files:
            self.title = tk.Label(self.root, text="Data error. Missing files:\n", font=("Arial", 30), fg="red")
            self.title.grid(row=0, column=0)
            self.missing = tk.Label(self.root, text=", ".join(missing_files), font=("Arial", 15), fg="black")
            self.missing.grid(row=1, column=0)
            tk.Button(self.root, text="Quit", command=self.root.quit).grid(row=2, column=0)
            return

        self.title = tk.Label(self.root, text="Choose and press \"Run\".", font=("Arial", 30), fg="black")
        self.title.grid(row=0, column=0, columnspan = 6, sticky = tk.N, pady = 25)

        self.stories_checkbar = self.make_checkbar(stories_list, 0, tk.S)
        self.invite_checkbar = self.make_checkbar(["League sunday invite", "Web banner invite"], 1, tk.N)
        self.dialog_window = DialogWindow(self.root)

        tk.Button(self.root, text="Quit", command=root.quit).grid(row=1, column=5, sticky = tk.NE, pady = 60) #, columnspan=6)
        tk.Button(self.root, text="Run", command=self.run).grid(row=1, column=5, sticky = tk.NE, pady = 30) #, columnspan=6)
        database = InviteDatabase(gui = self.dialog_window)
        tk.Button(self.root, text="Update database", command=database.update).grid(row=1, column=0, sticky = tk.NW, pady = 30) #, columnspan=6)
        tk.Button(self.root, text="Reset database", command=database.reset).grid(row=1, column=0, sticky = tk.NW, pady = 60) #, columnspan=6)

    def make_checkbar(self, m_list, row, side):
        """Creates and places a checkbar with given list of options.

        Parameters:
            m_list (List[str]): List of strings to be used as options.
            row (int): Row in which the checkbar is placed.
            side (str): Side of the frame in which the checkbar is placed.

        Returns:
            Checkbar: created checkbar object
        """

        checkbar = Checkbar(self.root, m_list)
        checkbar.grid(row = row, column = 0, columnspan = 6, sticky = side)

        checkbar.config(relief=tk.GROOVE, bd=2)
        return checkbar

    def run(self):
        """Method for starting processes of creating graphics chosen in checkbars.
        """

        s_list = self.stories_checkbar.state()
        if s_list[0]:
            save_name = "first"
            if self.dialog_window.yes_no("With auto generated text?"):
                s = OtherStory(save_name, self.dialog_window, self.data)
            else:
                save_name = "first_plain"
                s = OtherStory(save_name, self.dialog_window, plain = True)

            s.other_story()
            self.show_img(Path(FINAL_IMG_FOLDER, save_name + ".png"), 0)

        for i, story in enumerate(s_list[1:-1]):
            if story:
                s = Story(i, self.data[i], self.dialog_window)
                s.story()
                self.show_img(s.save_path, i + 1)

        if s_list[-1]:
            if self.dialog_window.yes_no("With auto generated text?"):
                s = OtherStory("last", self.dialog_window)
                save_name = "last"
            else:
                s = OtherStory("last_plain", self.dialog_window, plain = True)
                save_name = "last_plain"
            s.other_story()
            self.show_img(Path(FINAL_IMG_FOLDER, save_name + ".png"), 5)

        i_list = self.invite_checkbar.state()
        if i_list[0]:
            i = Invite(self.dialog_window, self.data)
            i.invite()
            self.show_img(INVITE_DONE_PATH, 3)
        if i_list[1]:
            w = WebBanner(self.data, Image.fromarray(i.base), self.dialog_window)
            w.make_banner()
            self.show_img(WEB_DONE_PATH, 3)

    def show_img(self, path, col):
        """Displays an image at the right place and "OK" button.
        On button click, both are deleted.

        Parameters:
            path (pathlib.Path): File path of image to be displayed.
            col (int): Number of column where the image is placed.
        """

        img = self.prepare_for_display(Image.open(path))
        image = ImageTk.PhotoImage(img)

        # Create a label widget to display the image
        label = tk.Label(self.root, image = image)
        label.image = image

        label.grid(row=3, column=col)

        def my_quit(label, button):
            label.destroy()
            button.destroy()

        button = tk.Button(self.root, text = "OK", command=lambda: my_quit(label, button))
        button.grid(row=4, column=col)

    def prepare_for_display(self, img):
        """Resizes the image to right size to fit in window.

        Parameters:
            img (PIL.Image): Image to be resized.
        """

        if img.height > 1200:
            return img.resize((int(img.width / 5), int(img.height / 5)))

        return img.resize((int(img.width / 2.5), int(img.height / 2.5)))

    def files_prepared(self):
        missing_files = []
        for f in MUST_EXIST_FILES:
            if not f.exists():
                missing_files.append(str(f))
        return missing_files

        
