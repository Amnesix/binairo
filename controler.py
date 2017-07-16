#!/usr/bin/env python3
# =============================================
# Etude du modèle MVC avec le programme Binairo
# ---------------------------------------------
# Jean MORLET
# ---------------------------------------------
# controler.py
# Controle les entrées/sorties.
# Met à jour le modèle.
# Vérifie les erreurs.
# Indique la fin du jeu.
# =============================================
import modele


class ControlerBinairo:

    def __init__(self, dim, m):
        self._m = m
        self._dim = dim
        self._row = 0
        self._col = 0
        self._arrays = []

    def up(self):
        self._col = (self._col + self._dim - 1) % self._dim

    def down(self):
        self._col = (self._col + 1) % self._dim

    def right(self):
        self._row = (self._row + 1) % self._dim

    def left(self):
        self._row = (self._row + self._dim - 1) % self._dim

    def modify(self, row=None, col=None):
        return self._m.incRC(self._row if row is None else row,
                             self._col if col is None else col)
    
    def verify(self):
        errors = []
        ar = self._m.getArray()
        cols = []
        rows = []
        # Recherche des lignes identiques ou à plus de _dim/2 éléments
        # identiques
        for r in range(len(ar)):
            if sum([1 if c is not None else 0 for c in ar[r]]) == self._dim:
                if len(rows):
                    for i in rows:
                        if ar[r] == ar[i]:
                            errors.append(('R', i, r))
                rows.append(r)
                try:
                    if sum(ar[r]) != self._dim // 2:
                        errors.append(('R', r))
                except:
                    pass
            row = self._m.getRow(r)
            d = None
            for i in range(self._dim):
                if d is None and row[i] is not None:
                    d, v = i, row[i]
                elif d is not None and v != row[i]:
                    if i - d >= 3:
                        errors.append(('r', r, d, i-1))
                    d, v = (i, row[i]) if row[i] is not None else (None, 0)
                try:
                    if i - d >= 2:
                        errors.append(('r', r, d, i))
                except:
                    pass
        # Recherche des colonnes identiques
        COLS = self._m.getCols()
        for c in range(len(ar[0])):
            if sum([1 if ar[r][c] is not None else 0 for r in range(len(ar))]) == 6:
                if len(cols):
                    for i in cols:
                        if COLS[c] == COLS[i]:
                            errors.append(('C', i, c))
                cols.append(c)
                try:
                    if sum([ar[r][c] for r in range(self._dim)]) != self._dim // 2:
                        errors.append(('C', c))
                except:
                    pass
            col = self._m.getCol(c)
            d = None
            for i in range(self._dim):
                if d is None and col[i] is not None:
                    d, v = i, col[i]
                elif d is not None and v != col[i]:
                    if i - d >= 3:
                        errors.append(('c', c, d, i-1))
                    d, v = (i, col[i]) if col[i] is not None else (None, 0)
                try:
                    if i - d >= 2:
                        errors.append(('c', c, d, i))
                except:
                    pass
        # Recherche d'éventuels triplets
        return errors

    def push(self):
        self._arrays.append(self._m.getArray())
        
    def pop(self):
        if len(self._arrays) > 0:
            self._m.setArray([r[:] for r in self._arrays.pop()])
            return True
        return False

    def findSoluce(self):
        self.push()
        def helper():
            if len(self.verify()) > 0:
                return False
            if self._m.getNbInArray() == self._dim ** 2:
                return True
            ar = self._m.getArray()
            for r in range(self._dim):
                for c in range(self._dim):
                    if ar[r][c] == None:
                        self.push()
                        self.modify(r, c)
                        if helper():
                            return True
                        self.modify(r, c)
                        if helper():
                            return True
                        self.pop()
                        return False
        soluce = helper()
        self._arrays.clear()
        return soluce

    def getRow(self):
        return self._row

    def getCol(self):
        return self._col
