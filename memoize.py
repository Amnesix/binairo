#!/usr/bin/env python3
# =============================================
# Classe de mémoïsation.
# ---------------------------------------------
# Jean MORLET
# ---------------------------------------------
# memoize.py
# cette classe permet d'accélérer les calcules
# répétitif au détriment de l'occupation 
# mémoire.
# =============================================
import collections
import functools

class Counter:
    def __init__(self):
        self._number = 0
    def increment(self):
        self._number += 1
    def __str__(self):
        return str(self._number)
    def __getattr__(self, attr):
        return getattr(self.f, attr)


class Memoize(object):
    '''
    Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, fn):
        self.memo = {}
        self.count = Counter() if c is None else c
        self.fn = fn
    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.fn(*args)
        return self.memo[args]
    def __repr__(self):
        '''Return the function's docstring'''
        return self.func.__doc__
    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)

class MemoizeCpt(object):
    '''
    Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''
    def __init__(self, c):
        self.memo = {}
        self.count = Counter() if c is None else c
    def __call__(self, fn, *args):
        def helper(*args):
            if args not in self.memo:
                self.memo[args] = fn(*args)
            else:
                self.count.increment()
            return self.memo[args]
        return helper
    def __repr__(self):
        '''Return the function's docstring'''
        return self.func.__doc__
    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)
    def __str__(self):
        return "compteur = %s" % c

c = Counter()

@MemoizeCpt(c)
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


if __name__ == "__main__":
    print('fibonacci(100) = %d' % fib(100))
    print('Compteur =', c)
