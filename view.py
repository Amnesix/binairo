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
        self._arrays = []
        self._parent.title("Binairo")
        self.pack(fill=BOTH, expand=True)
        self._canvas = Canvas(self, width=16+50*self._dim,
                              height=16+50*self._dim)
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
        self._arrays.clear()

    def push(self):
        self._c.push()

    def pop(self):
        if self._c.pop():
            self.affiche(self._m.getArray())

    def onMouseClick(self, evt):
        row = (evt.x - OFFSET) // 50
        col = (evt.y - OFFSET) // 50
        if self._c.modify(row=row, col=col):
            self.affiche(self._m.getArray(), row, col, self._c.verify())

    def findSoluce(self):
        if self._c.findSoluce():
            self.affiche(self._m.getArray(), None, None, [])
            self._labelText.set("Solution trouvée :)")
        else:
            self._labelText.set("Solution impossible")

    def affiche(self, ar=None, row=None, col=None, errors=[]):
        self._row = self._row if row is None else row
        self._col = self._col if col is None else col
        self._canvas.delete("all")
        self._labelText.set('')
        if errors is not None:
            for tt in errors:
                if tt[0] == 'R':
                    for i in tt[1:]:
                        self._canvas.create_rectangle(OFFSET+i*50+1, OFFSET+1,
                                                      OFFSET+i*50+50, OFFSET+300,
                                                      fill=LIGHTRED, width=0)
                elif tt[0] == 'C':
                    for i in tt[1:]:
                        self._canvas.create_rectangle(OFFSET+1, OFFSET+i*50+1,
                                                      OFFSET+300, OFFSET+i*50+50,
                                                      fill=LIGHTRED, width=0)
                elif tt[0] == 'r':
                    self._canvas.create_rectangle(OFFSET+tt[1]*50+1,
                                                  OFFSET+tt[2]*50+1,
                                                  OFFSET+tt[1]*50+50,
                                                  OFFSET+tt[3]*50+50,
                                                  fill=LIGHTRED, width=0)
                elif tt[0] == 'c':
                    self._canvas.create_rectangle(OFFSET+tt[2]*50+1,
                                                  OFFSET+tt[1]*50+1,
                                                  OFFSET+tt[3]*50+50,
                                                  OFFSET+tt[1]*50+50,
                                                  fill=LIGHTRED, width=0)
        if row is not None and col is not None:
            self._canvas.create_rectangle(OFFSET+row*50+2, OFFSET+col*50+2,
                                          OFFSET+row*50+48, OFFSET+col*50+48,
                                          width=3, outline='yellow')
        for i in range(7):
            self._canvas.create_line(OFFSET+0, OFFSET+i*50, OFFSET+300, OFFSET+i*50)
            self._canvas.create_line(OFFSET+i*50, OFFSET+0, OFFSET+i*50, OFFSET+300)
        if ar is not None:
            for r in range(len(ar)):
                for c in range(len(ar[r])):
                    v = ar[r][c]
                    if v == 0:
                        self._canvas.create_oval(OFFSET+r*50+10, OFFSET+c*50+10,
                                                 OFFSET+r*50+40, OFFSET+c*50+40,
                                                 fill='blue')
                    elif v == 1:
                        self._canvas.create_line(OFFSET+r*50+25, OFFSET+c*50+10,
                                                 OFFSET+r*50+25, OFFSET+c*50+40,
                                                 width=7, fill='blue')
