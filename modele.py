#!/usr/bin/env python3
# =============================================
# Etude du modèle MVC avec le programme Binairo
# ---------------------------------------------
# Jean MORLET
# ---------------------------------------------
# modele.py
# Description du modèle du jeu.
# =============================================

VALUES = (0, 1)

class ModeleBinairo:

    def __init__(self, dim=6):
        self._dim = dim
        self.clear()

    def incRC(self, row, col):
        try:
            v = self._array[row][col]
            self._array[row][col] = None if v == 1 else 1 if v == 0 else 0
        except:
            return False
        return True

    def setRC(self, row, col, value):
        if 0 <= row < self._dim and 0 <= col < self._dim and value in VALUES:
            self._array[row][col] = value

    def resetRC(self, row, col):
        if 0 <= row < self._dim and 0 <= col < self._dim:
            self._array[row][col] = None

    def clear(self):
        self._array = [[None]*self._dim for _ in range(self._dim)]

    def getNbInRow(self, r):
        return sum([1 if self._array[r][c] is not None else 0 for c in range(self._dim)])

    def getNbInCol(self, c):
        return sum([1 if self._array[r][c] is not None else 0 for r in range(self._dim)])

    def getNbInArray(self):
        return sum([self.getNbInRow(r) for r in range(self._dim)])

    def getRow(self, r):
        return self._array[r]

    def getCol(self, c):
        return [r[c] for r in self._array]

    def getRows(self):
        rows = []
        for r in range(self._dim):
            v = 0
            for c in range(self._dim):
                v += 1<<c if self._array[r][c] == 1 else 0
            rows.append(v)
        return rows

    def getCols(self):
        cols = []
        for c in range(self._dim):
            v = 0
            for r in range(self._dim):
                v += 1<<r if self._array[r][c] == 1 else 0
            cols.append(v)
        return cols

    def getArray(self):
        return [r[:] for r in self._array]

    def setArray(self, ar):
        self._array = ar

    def __str__(self):
        return [' '+' '.join(['.' if c is None else str(c) for c in row])+' '
                for row in self._array]
