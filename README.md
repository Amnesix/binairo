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

Ne plus utiliser de chaine de caractères : Il faut revoir la recherche des
triplets. Pour les colonnes ou lignes identiques, aucun problème.  
Soit a la valeur d'un colonne et b la valeur des cases renseignées.  
a donne directement la liste des bits à 1.  
<pre>(a & ((1<<dim)-1)^b</pre> donne la liste des bits à 0.
La recherche de triplets peut se faire ensuite par un masque de chaque valeurs
avec 7 et shift à droite de 1 dim-2 fois.  
Bien évidemment, ceci ne concerne que la recherche de solution. Dans le cas de
la vérification en cours de jeu, le temps de calcul importe peu.

Utilisation de la mémoïsation
-----------------------------
On peut gagner pas mal de temps en utilisation la mémoïsation sur l'ajout d'une
valeur : la méthode devra enregistrer les patterns de la ligne et de la colonne
concernées et retourner le résultat pour chacun des patterns. Remarque : cette 
solution ne fonctionne que pour la fonction de vérification spécifique à la 
recherche de solution et pas pour la vérification de base qui n'en a pas besoin.
