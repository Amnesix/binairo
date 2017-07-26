#!/usr/bin/env python3
# =============================================
# Etude du modèle MVC avec le programme Binairo
# ---------------------------------------------
# Jean MORLET
# ---------------------------------------------
# modele.py
# Description du modèle du jeu.
# ---------------------------------------------
# Historique
# V2.0 Remplacement de la table de valeur par
#      deux tables de mots binaires.
# =============================================
from copy import deepcopy
from memoize import Memoize
from array import array


def nb1c(value):
    c = 0
    while value:
        c += value & 1
        value >>= 1
    return c

NB1 = array('I', [nb1c(x) for x in range(2**12)])
nb1 = lambda value: NB1[value]


class ModeleBinairo:

    def __init__(self, dim=6):
        self._dim = dim
        self.clear()

    def incRC(self, row, col):
        try:
            if self._rows[row][1] & (1 << col):
                if self._rows[row][0] & (1 << col):
                    self.clearRC(row, col)
                else:
                    self.setRC(row, col)
            else:
                self.resetRC(row, col)
        except:
            return False
        return True

    def setRC(self, row, col):
        if 0 <= row < self._dim and 0 <= col < self._dim:
            self._rows[row][0] |= 1 << col
            self._cols[col][0] |= 1 << row
            self._rows[row][1] |= 1 << col
            self._cols[col][1] |= 1 << row

    def resetRC(self, row, col):
        if 0 <= row < self._dim and 0 <= col < self._dim:
            self._rows[row][0] &= ~(1 << col)
            self._cols[col][0] &= ~(1 << row)
            self._rows[row][1] |= 1 << col
            self._cols[col][1] |= 1 << row

    def clearRC(self, row, col):
        if 0 <= row < self._dim and 0 <= col < self._dim:
            self._rows[row][1] &= ~(1 << col)
            self._cols[col][1] &= ~(1 << row)

    def clear(self):
        self._rows = [[0, 0] for _ in range(self._dim)]
        self._cols = [[0, 0] for _ in range(self._dim)]

    def getNbInRow(self, r):
        return nb1(self._rows[r][1])

    def getNbInCol(self, c):
        return nb1(self._cols[c][1])

    def getNbInArray(self):
        return sum([self.getNbInRow(r) for r in range(self._dim)])

    def getRow(self, r):
        return self._rows[r][0]

    def getCol(self, c):
        return self._cols[c][0]

    @Memoize
    def val2str(self, a, b):
        """Conversion d'une ligne ou d'une colonne en chaine."""
        return ''.join([('1' if a & (1 << c) else '0')
                        if b & (1 << c) else '.'
                        for c in range(self._dim)])

    def getRowStr(self, r):
        return self.val2str(self._rows[r][0], self._rows[r][1])

    def getColStr(self, c):
        return self.val2str(self._cols[c][0], self._cols[c][1])

    def getRows(self):
        return self._rows

    def getCols(self):
        return self._cols

    def getArray(self):
        return deepcopy(self._rows), deepcopy(self._cols)

    def setArray(self, ar):
        try:
            self._rows = deepcopy(ar[0])
            self._cols = deepcopy(ar[1])
        except ValueError:
            print("Error: setArray(", ar, ")")

    def __str__(self):
        return ' '+ '\n '.join([' '.join([('1' if r[0] & (1 << c) else '0')
                                          if r[1] & (1 << c) else '.'
                                          for c in range(self._dim)])
                                          for r in self._cols])+'\n-'+'-'*self._dim*2
