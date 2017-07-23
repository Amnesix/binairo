#!/usr/bin/env python3
# =============================================
# Etude du modèle MVC avec le programme Binairo
# ---------------------------------------------
# Jean MORLET
# ---------------------------------------------
# view.py
# Gestion des entrées/sorties.
# =============================================
import modele
import controler
from tkinter import *

OFFSET = 5
LIGHTRED = '#FF8080'
CASE = 35


class ViewerBinairo(Frame):

    def __init__(self, parent, dim, m, c):
        self._dim = dim
        self._m = m
        self._c = c
        self._labelText = StringVar()
        Frame.__init__(self, parent, background='grey')
        self._parent = parent
        self.initUI()

    def initUI(self):
        self._parent.title("Binairo")
        self.pack(fill=BOTH, expand=True)
        self._canvas = Canvas(self, width=16+CASE*self._dim,
                              height=16+CASE*self._dim)
        self._canvas.grid(row=0, column=0, sticky="news")

        frame = Frame(self, relief=RAISED, borderwidth=1, background='lightgrey')
        frame.grid(row=1, column=0, sticky="news")

        closeButton = Button(frame, text='Quit', command=lambda : sys.exit())
        closeButton.grid(row=0, column=4, sticky="news")
        soluceButton = Button(frame, text='Soluce', command=lambda :
                              self.findSoluce())
        soluceButton.grid(row=0, column=3, sticky="news")
        pushButton = Button(frame, text='Push', command=lambda: self.push())
        pushButton.grid(row=0, column=0, sticky="news")
        popButton = Button(frame, text='Pop', command=lambda: self.pop())
        popButton.grid(row=0, column=1, sticky="news")
        clearButton = Button(frame, text='Clear', command=lambda : self.clear())
        clearButton.grid(row=0, column=2, sticky="news")

        self._mesLabel = Label(frame, justify='center',
                               textvariable=self._labelText)
        self._mesLabel.grid(row=1, column=0, columnspan=5, sticky="news")

        self._canvas.bind('<Button-1>', self.onMouseClick)

        self.affiche(None, row=0, col=0)

    def clear(self):
        self._m.clear()
        self.affiche()

    def push(self):
        self._c.push()

    def pop(self):
        if self._c.pop():
            self.affiche(self._m.getArray())

    def onMouseClick(self, evt):
        # Calcul de la case clickée
        row = (evt.x - OFFSET) // CASE
        col = (evt.y - OFFSET) // CASE
        if self._c.modify(row=row, col=col):
            self.affiche(self._m.getArray(), row, col, self._c.verify())

    def findSoluce(self):
        self.push()
        ret, temps = self._c.findSoluce()
        if ret:
            self.affiche(self._m.getArray(), None, None, [])
            self._labelText.set("Solution trouvée en %fs" % temps)
        else:
            self._labelText.set("Solution impossible (%fs)" % temps)

    def affiche(self, ar=None, row=None, col=None, errors=[]):
        self._row = self._row if row is None else row
        self._col = self._col if col is None else col
        self._canvas.delete("all")
        self._labelText.set('')
        # Affichage des erreurs
        if errors is not None:
            for tt in errors:
                if tt[0] == 'R':
                    for i in tt[1:]:
                        self._canvas.create_rectangle(OFFSET+i*CASE+1, OFFSET+1,
                                                      OFFSET+i*CASE+CASE,
                                                      OFFSET+self._dim*CASE,
                                                      fill=LIGHTRED, width=0)
                elif tt[0] == 'C':
                    for i in tt[1:]:
                        self._canvas.create_rectangle(OFFSET+1, OFFSET+i*CASE+1,
                                                      OFFSET+self._dim*CASE,
                                                      OFFSET+i*CASE+CASE,
                                                      fill=LIGHTRED, width=0)
                elif tt[0] == 'r':
                    self._canvas.create_rectangle(OFFSET+tt[1]*CASE+1,
                                                  OFFSET+tt[2]*CASE+1,
                                                  OFFSET+tt[1]*CASE+CASE,
                                                  OFFSET+tt[3]*CASE,
                                                  fill=LIGHTRED, width=0)
                elif tt[0] == 'c':
                    self._canvas.create_rectangle(OFFSET+tt[2]*CASE+1,
                                                  OFFSET+tt[1]*CASE+1,
                                                  OFFSET+tt[3]*CASE,
                                                  OFFSET+tt[1]*CASE+CASE,
                                                  fill=LIGHTRED, width=0)
        # Affichage du curseur
        if row is not None and col is not None:
            self._canvas.create_rectangle(OFFSET+row*CASE+2, OFFSET+col*CASE+2,
                                          OFFSET+row*CASE+CASE-2,
                                          OFFSET+col*CASE+CASE-2,
                                          width=3, outline='yellow')
        # Affichage des lignes du plateau
        for i in range(self._dim+1):
            self._canvas.create_line(OFFSET+0, OFFSET+i*CASE,
                                     OFFSET+CASE*self._dim, OFFSET+i*CASE)
            self._canvas.create_line(OFFSET+i*CASE, OFFSET+0, OFFSET+i*CASE,
                                     OFFSET+CASE*self._dim)
        # Affichage des pièces.
        if ar is not None:
            rows, cols = ar
            for r in range(self._dim):
                for c in range(self._dim):
                    v = rows[r][0] & (1 << c) if rows[r][1] & (1 << c) else -1
                    if v == 0:
                        self._canvas.create_oval(OFFSET+r*CASE+8,
                                                 OFFSET+c*CASE+8,
                                                 OFFSET+r*CASE+CASE-8,
                                                 OFFSET+c*CASE+CASE-8,
                                                 width=5, outline='blue')
                    elif v != -1:
                        self._canvas.create_line(OFFSET+r*CASE+CASE//2,
                                                 OFFSET+c*CASE+6,
                                                 OFFSET+r*CASE+CASE//2,
                                                 OFFSET+c*CASE+CASE-6,
                                                 width=7, fill='blue')
