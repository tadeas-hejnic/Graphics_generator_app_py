import tkinter as tk
from gui.my_gui import MyGUI
from src.api import league_sunday
from src.story import Story


def get_stories_list(data):
    m_list = []
    m_list.append("First story")
    for x in data:
        m_list.append(x["competitionName"])
    m_list.append("Last story")
    return m_list


def main():   
    data = league_sunday()
    root = tk.Tk()
    gui = MyGUI(get_stories_list(data), data, root)
    root.mainloop()
    

if __name__ == '__main__':
    main()
