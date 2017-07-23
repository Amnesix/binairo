# binairo
clone de MR. BINAIRO

Lancement de l'application :
> main.py [**6**|8|10|12]

Informations
------------
Pour le moment, l'application est capable de trouver la solution d'une grille,
mais sans aucune optimisation. Résultat, pas loin d'1mn pour une grille 10x10 
préremplie. À partir d'un grille vide, la recherche dépasse 20mn<sup>1</sup>

<sup>1</sup> sur un core 2 Duo T5500 (1.66 GHz, 667 MHz FSB).

Pistes d'optimisation
---------------------
La recherche de la validité d'un coup devrait commencer par la position du coup :
 - recherche de triplet (horizontalement et verticalement) ;
 - si la ligne est complète, vérification de doublon ;
 - idem pour la colonne.
Inutile de vérifier le reste de la grille car il ne devrait pas y avoir d'autres
erreurs. Sinon, il y a un bug dans la vérification !

Utilisation de la mémoïsation
-----------------------------
On peut gagner pas mal de temps en utilisation la mémoïsation sur l'ajout d'une
valeur : la méthode devra enregistrer les patterns de la ligne et de la colonne
concernées et retourner le résultat pour chacun des patterns. Remarque : cette 
solution ne fonctionne que pour la fonction de vérification spécifique à la 
recherche de solution et pas pour la vérification de base qui n'en a pas besoin.
