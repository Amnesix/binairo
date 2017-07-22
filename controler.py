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
import time


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
        """
        Fonction permettant de vérifier si un grille est correct
        ainsi que de retourner la liste des erreurs.
        """
        errors = []
        arr, arc = self._m.getArray()
        rows = []
        cols = []
        # Recherche des lignes identiques ou à plus de _dim/2 éléments
        # identiques
        print("verify")
        print(self._m)
        for r in range(self._dim):
            print(arr[r], self._m.getNbInRow(r))
            if self._m.getNbInRow(r) == self._dim:
                if len(rows):
                    for i in rows:
                        if arr[r][0] == arr[i][0]:
                            errors.append(('R', i, r))
                rows.append(r)
                #try:
                if modele.nb1(arr[r][0]) != self._dim // 2:
                    errors.append(('R', r))
                #except:
                    #pass
            row = self._m.getRowStr(r)
            d = None
            # recherche de triplet (ou plus)
            for i in range(self._dim):
                if d is None and row[i] != '.':
                    d, v = i, row[i]
                elif d is not None and v != row[i]:
                    if i - d >= 3:
                        errors.append(('r', r, d, i-1))
                    d, v = (i, row[i]) if row[i] != '.' else (None, 0)
                try:
                    if i - d >= 2:
                        errors.append(('r', r, d, i))
                except:
                    pass
        # Recherche des colonnes identiques
        for c in range(self._dim):
            if self._m.getNbInCol(c) == self._dim:
                if len(cols):
                    for i in cols:
                        if arc[c][0] == arc[i][0]:
                            errors.append(('C', i, c))
                cols.append(c)
                try:
                    if modele.nb1(arc[c][0]) != self._dim // 2:
                        errors.append(('C', c))
                except:
                    pass
            col = self._m.getColStr(c)
            d = None
            # recherche de triplet (ou plus)
            for i in range(self._dim):
                if d is None and col[i] != '.':
                    d, v = i, col[i]
                elif d is not None and v != col[i]:
                    if i - d >= 3:
                        errors.append(('c', c, d, i-1))
                    d, v = (i, col[i]) if col[i] != '.' else (None, 0)
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
            self._m.setArray(self._arrays.pop())
            return True
        return False

    def findSoluce(self):
        """ Recherche d'une solution par force brute """
        debut = time.time()
        self._soluce = []
        def helper():
            if len(self.verify()) > 0:
                return False
            if self._m.getNbInArray() == self._dim ** 2:
                self._soluce = self._m.getArray()
                return True
            arr, arc = self._m.getArray()
            for r in range(self._dim):
                for c in range(self._dim):
                    if arr[r][1] & (1 << c) == 0:
                        self.push()
                        self.modify(r, c)
                        if helper():
                            self.pop()
                            return True
                        self.modify(r, c)
                        if helper():
                            self.pop()
                            return True
                        self.pop()
                        return False
        self.push()
        soluce = helper()
        # self._arrays.clear()
        self._m.setArray(self._soluce)
        fin = time.time()
        return soluce, fin - debut

    def getRow(self):
        return self._row

    def getCol(self):
        return self._col
