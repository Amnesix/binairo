# binairo
clone de MR. BINAIRO

Lancement de l'application :
> main.py [**6**|8|10|12]

Informations
------------
Pour le moment, l'application est capable de trouver la solution d'une grille,
mais sans aucune optimisation. Résultat, pas loin d'1mn pour une grille 10x10 
préremplie. À partir d'une grille vide, la recherche dépasse 20mn<sup>1</sup>.

<sup>1</sup> sur un core 2 Duo T5500 (1.66 GHz, 667 MHz FSB).

Recherche des zones à optimiser
-------------------------------
L'utilisation de cProfile permet de facilement trouver les bouts de codes
prenant un temps trop important. Cf main.py.

Pistes d'optimisation
---------------------
La recherche de la validité d'un coup devrait commencer par la position du coup :
 - recherche de triplet (horizontalement et verticalement) ;
 - si la ligne est complète, vérification de doublon ;
 - idem pour la colonne.
Inutile de vérifier le reste de la grille car il ne devrait pas y avoir d'autres
erreurs. Sinon, il y a un bug dans la vérification !

Ne plus utiliser de chaine de caractères : Il faut revoir la recherche des
triplets. Pour les colonnes ou lignes identiques, aucun problème.  
Soit a la représentation d'une colonne et b la valeur représentant les cases
renseignées (1 case renseignée, 0 case non renseignée).  
**a** donne directement la liste des bits à 1.  
**(a & ((1&lt;&lt;dim)-1)^b** donne la liste des bits à 0.
La recherche de triplets peut se faire ensuite par un masque de chaque valeurs
avec 7 et shift à droite de 1 dim-2 fois.  
Bien évidemment, ceci ne concerne que la recherche de solution. Dans le cas de
la vérification en cours de jeu, le temps de calcul importe peu.

Grace à la suppression de l'usage de chaînes de caractères, le temps de calcul
d'une solution à partir d'une grille vide de 10x10 passe de plus de 20mn à 3mn
et 20s environ ! La recherche d'un solution sur 12x12 préremplie devient
supportable.

L'optimisation de la fonction rechTriplet permet de passer à 1mn 51s pour une
grille 10x10 vide.

Utilisation de la mémoïsation
-----------------------------
Je l'utilise sur la fonction de recherche de triplet (je ne sais pas si c'est
réellement utile, il faut que je fasse des tests).  
Je l'utilise aussi pour la conversion d'une ligne ou d'une colonne en chaine de
caractère... Comme cette fonction n'est pas utilisée par la recherche de
solution, ce n'est absolument par utile.
