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

def nb1(value):
    return sum([int(c) for c in str(bin(value)[2:])])

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

    def getRowStr(self, r):
        return ''.join([('1' if self._rows[r][0] & (1 << c) else '0')
                        if self._rows[r][1] & (1 << c) else '.'
                        for c in range(self._dim)])

    def getCol(self, c):
        return self._cols[c][0]

    def getColStr(self, c):
        return ''.join([('1' if self._cols[c][0] & (1 << r) else '0')
                        if self._cols[c][1] & (1 << r) else '.'
                        for r in range(self._dim)])

    def getRows(self):
        return self._rows

    def getCols(self):
        return self._cols

    def getArray(self):
        return (self._rows, self._cols)

    def setArray(self, ar):
        try:
            self._rows, self._cols = ar
        except ValueError:
            print("setArray(", ar, ")")

    def __str__(self):
        return '\n'.join([' '.join([('1' if r[0] & (1 << c) else '0')
                                    if r[1] & (1 << c) else '.' 
                                        for c in range(self._dim)])
                                    for r in self._cols])

if __name__ == '__main__':
    obj = ModeleBinairo()
    obj.clear()
    print(obj._rows)
    print(obj)
