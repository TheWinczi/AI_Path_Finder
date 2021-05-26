from .gui import *
from tkinter import Tk, PhotoImage


class Application:

    def __init__(self, world, agent):
        self.__world = world
        self.__agent = agent
        self.__gui = None

    def start(self):
        root = Tk()
        root.title("Artificial Intelligence Project")
        root.iconphoto(False, PhotoImage(file='gui_app/img/icon.png'))
        self.__gui = GUI(root, self.__world, self.__agent)
        root.mainloop()
