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
# Recheche d'une solution.
# =============================================
import modele
import time
from memoize import *
import re

invBin = lambda x: ''.join([c for c in bin(x)[:1:-1]])

class ControlerBinairo:

    def __init__(self, dim, m):
        self._m = m
        self._dim = dim
        self._row = 0
        self._col = 0
        self._arrays = []
        self._compl = (1 << dim) - 1
        self._memo = {}

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
        exp = r"0{3,5}|1{3,5}"
        errors = []
        rows = self._m.getRows()
        cols = self._m.getCols()
        for val in range(self._dim):
            # Recherche d'éventuels triplets
            strrow = self._m.getRowStr(val)
            ret = re.search(exp, strrow)
            if ret:
                ret = ret.span()
                errors.append(('r', val, ret[0], ret[1]))
            strcol = self._m.getColStr(val)
            ret = re.search(exp, strcol)
            if ret:
                ret = ret.span()
                errors.append(('c', val, ret[0], ret[1]))
            # Recherche de colonnes et lignes identiques:
            if self._m.getNbInRow(val) == self._dim:
                if sum([c == '1' for c in strrow]) != self._dim // 2:
                    errors.append(('R', val))
                for i in range(val+1, self._dim):
                    if rows[val][0] == rows[i][0]:
                        errors.append(('R', val, i))
            if self._m.getNbInCol(val) == self._dim:
                if sum([c == '1' for c in strcol]) != self._dim // 2:
                    errors.append(('C', val))
                for i in range(val+1, self._dim):
                    if cols[val][0] == cols[i][0]:
                        errors.append(('C', val, i))
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

        def helper(row, col):
            def rechTriplet(value):
                if value not in self._memo:
                    self._memo[value] = False
                    for i in range(self._dim-2):
                        if (value >> i) & 7 == 7:
                            self._memo[value] = True
                return self._memo[value]

            def testMod(r, c):
                # Vérifier si le coup provoque l'apparition d'un triplet
                # (ou +)
                rm = self._m._rows[r][1]
                r1 = self._m._rows[r][0]
                r0 = (r1 ^ self._compl) & rm
                cm = self._m._cols[c][1]
                c1 = self._m._cols[c][0]
                c0 = (c1 ^ self._compl) & cm
                if rechTriplet(r1) or rechTriplet(r0):
                    #print('1 :', invBin(r1), '- 0 :', invBin(r0))
                    return False, 10
                if rechTriplet(c1) or rechTriplet(c0):
                    return False, 11
                # Si ligne (ou colonne) pleine, vérifier si doublon
                if rm ^ self._compl == 0:
                    if modele.nb1(r1) != self._dim // 2:
                        return False, 2
                    for i in range(self._dim):
                        if i != r and self._m._rows[i][0] == r1:
                            return False, 3
                if cm ^ self._compl == 0:
                    if modele.nb1(c1) != self._dim // 2:
                        return False, 4
                    for i in range(self._dim):
                        if i != c and self._m._cols[i][0] == c1:
                            return False, 5
                return True, 0
            def testCase(r, c):
                # On commence par tester avec 0
                self._m.resetRC(r, c)
                #print("test 0 en %d,%d :\n%s" % (r, c, self._m))
                ret, num = testMod(r, c)
                if ret:
                    if helper(r, c):
                        return True
                # On teste maintenant avec 1
                self._m.setRC(r, c)
                #print("test 1 en %d,%d (%d) :\n%s" % (r, c, num, self._m))
                ret, num = testMod(r, c)
                if ret:
                    if helper(r, c):
                        return True
                # On remet tout à 0 dans cette case.
                self._m.clearRC(r, c)
                #print("Retour en %d,%d (%d) :\n%s" % (r, c, num, self._m))
                #print('pop')
                #print(self._m)
                return False
            # 1- Si tout est rempli, c'est la solution !
            if self._m.getNbInArray() == self._dim ** 2:
                self._soluce = self._m.getArray()
                return True
            # 2- Recherche des cases non jouées.
            for r in range(row, self._dim):
                for c in range(self._dim):
                    if self._m._rows[r][1] & (1 << c) == 0:
                        return testCase(r, c)
        self.push()
        soluce = helper(0, 0)
        # self._arrays.clear())
        # print(soluce, self._soluce)
        if soluce:
            self._m.setArray((self._soluce[0].copy(), self._soluce[1].copy()))
        fin = time.time()
        return soluce, fin - debut

    def getRow(self):
        return self._row

    def getCol(self):
        return self._col
