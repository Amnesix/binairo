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
from memoize import *
import re


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

        def helper():
            @Memoize
            def testRC(string):
                return re.search(r"000|111", string) is not None

            def testMod(r, c):
                # Vérifier si le coup provoque l'apparition d'un triplet
                # (ou +)
                sr = self._m.getRowStr(r)
                sc = self._m.getColStr(c)
                if testRC(sr) or testRC(sc):
                    return False, 1
                # Si ligne (ou colonne) pleine, vérifier si doublon
                if '.' not in sr:
                    if sum([int(c) for c in sr]) != self._dim // 2:
                        return False, 2
                    for i in range(self._dim):
                        if i != r and self._m._rows[i][0] == self._m._rows[r][0]:
                            return False, 3
                if '.' not in sc:
                    if sum([int(c) for c in sc]) != self._dim // 2:
                        return False, 4
                    for i in range(self._dim):
                        if i != c and self._m._cols[i][0] == self._m._cols[c][0]:
                            return False, 5
                return True, 0

            if self._m.getNbInArray() == self._dim ** 2:
                self._soluce = self._m.getArray()
                return True
            for r in range(self._dim):
                for c in range(self._dim):
                    if self._m._rows[r][1] & (1 << c) == 0:
                        # case non jouée
                        self.push()
                        # On commence par tester avec 0
                        self.modify(r, c)
                        ret, num = testMod(r, c)
                        if ret:
                            if helper():
                                self.pop()
                                return True
                        # On teste maintenant avec 1
                        self.modify(r, c)
                        ret, num = testMod(r, c)
                        if ret:
                            if helper():
                                self.pop()
                                return True
                        self.pop()
                        return False
        self.push()
        soluce = helper()
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
