from .gui import *
from tkinter import Tk


class Application:

    def __init__(self, world, agent):
        self.__world = world
        self.__agent = agent
        self.__gui = None

    def start(self):
        root = Tk()
        root.title("Artifical Inteligence Projekt")
        self.__gui = GUI(root, self.__world, self.__agent)
        root.mainloop()
