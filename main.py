#!/usr/bin/env python3
# =============================================
# Etude du modèle MVC avec le programme Binairo
# ---------------------------------------------
# Jean MORLET
# ---------------------------------------------
# main.py
# Le jeu
# =============================================

from modele import ModeleBinairo
from controler import ControlerBinairo
from view import ViewerBinairo
from tkinter import *
import sys

DIM = 6


def main():
    global m, v, c

    m = ModeleBinairo(DIM)
    c = ControlerBinairo(DIM, m)

    root = Tk()
    root.geometry("316x366")
    v = ViewerBinairo(root, DIM, m, c)
    root.bind('<Up>', lambda e: up())
    root.bind('<Down>', lambda e: down())
    root.bind('<Left>', lambda e: left())
    root.bind('<Right>', lambda e: right())
    root.bind('x', lambda e: sys.exit())
    root.bind('<space>', lambda e: modify())

    root.mainloop()


def modify():
    c.modify()
    common()


def common():
    v.affiche(m.getArray(), c.getRow(), c.getCol(), c.verify())


def up():
    c.up()
    common()


def down():
    c.down()
    common()


def left():
    c.left()
    common()


def right():
    c.right()
    common()


if __name__ == "__main__":
    main()
