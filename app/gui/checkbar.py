"""Module for Checkbarclass copied from https://python-course.eu/tkinter/checkboxes-in-tkinter.php
"""

import tkinter as tk


class Checkbar(tk.Frame):
    """A class for creating a list of checkboxes in a Tkinter frame.

    Args:
        parent (Frame, optional): The parent frame of the checkbar. Default is None.
        picks (list, optional): A list of strings representing the labels for the checkboxes. Defaults to [].
        side (str, optional): The side of the parent frame to which the checkbar should be packed. Defaults to LEFT.
        anchor (str, optional): The anchor point for the checkbar within the parent frame. Defaults to W.

    Attributes:
        vars (list): A list of IntVar objects representing the state of the checkboxes.
    """
    def __init__(self, parent=None, picks=None, side=tk.LEFT, anchor=tk.W):
        tk.Frame.__init__(self, parent)
        self.vars = []
        if picks is None:
            picks = []
        for pick in picks:
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=tk.YES)
            self.vars.append(var)

    def state(self):
        """Returns the state of the checkbar.

        Returns:
            List[int]: A list of integers representing the state of each option in the checkbar.
        """
        return list(map((lambda var: var.get()), self.vars))
