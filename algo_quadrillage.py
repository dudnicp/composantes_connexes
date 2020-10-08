#!/usr/bin/env python3
"""
compute sizes of all connected components.
sort and display.
"""

from sys import argv


class Point:
    """On définit une classe de points"""
    def __init__(self, coordinates, numero_graphe=-1):
        """constructeur"""
        self.x, self.y = coordinates

    def square_distance_to(self, other):
        """
        SQUARE euclidean distance between two points.
        """
        return (self.x - other.x)**2 + (self.y - other.y)**2

    def __eq__(self, other):
        """Eq"""
        return (self.x, self.y) == (other.x, other.y)


def load_instance(filename):
    """
    loads .pts file.
    returns distance limit and points.
    """
    with open(filename, "r") as instance_file:
        lines = iter(instance_file)
        distance = float(next(lines))
        points = [Point([float(f) for f in l.split(",")]) for l in lines]

    return distance, points


def fusion_graphes_cases(dict_cases, dict_graphes, graphe_act, points_case_act, coords_etudie, DIST_CARRE):
    """Fusionne les graphes de deux cases"""
    
    points_case_etudie, graphe_etudie = dict_cases[coords_etudie]
    if points_case_etudie and graphe_etudie != graphe_act: # On ne cherche à fusionner les composantes que si la case étudiée n'est pas vide et si elle n'appartient pas déjà à la même composante que la case actuelle
        for point1 in points_case_act:
            for point2 in points_case_etudie:
                if point1.square_distance_to(point2) < DIST_CARRE:
                    if graphe_etudie is None: # Si la case étudiée n'appartenait à aucune composante connexe, on la rajoute à la composante de la case actuelle
                        dict_cases[coords_etudie][1] = graphe_act
                        dict_graphes[graphe_act].append(coords_etudie)
                    else: # Sinon on fusionne les deux composantes
                        for case in dict_graphes[graphe_etudie]:
                            dict_cases[case][1] = graphe_act # chaque case de l'ancienne composante fait maintenant part de la composante actuelle
                            dict_graphes[graphe_act].append(case)
                        del dict_graphes[graphe_etudie] # on supprime l'ancienne composante
                    return # on arrete les calculs dès qu'on a trouvé un point qui permette de relier les deux composantes


def print_components_sizes(distance, points):
    """
    affichage des tailles triees de chaque composante
    """
    DIST_CARRE = distance**2
    TAILLE_CASE = distance/1.5 # on prend distance/1.5 au lieu de distance/sqrt(2) pour éviter les complications dues à la représentation des nombres en machine. Cela n'affecte pas le fonctionnement de l'algorithme tant qu'on divise par un nombre 2 < x < sqrt(2).
    
    # Construction du dictionnaire contenant tous les points 
    dict_cases = {}
    XY_MAX = int(1/TAILLE_CASE) - (not(1/TAILLE_CASE)%1) # XY_MAX est l'indice max des cases du quadrillage
    for i in range(XY_MAX+1):
        for j in range(XY_MAX+1):
            dict_cases[(i,j)] = [[],None] # Au début chaque case est vide et l'indice de la composante connexe à laquelle elle appartient est None
    for point in points:
        x_case = point.x // TAILLE_CASE
        y_case = point.y // TAILLE_CASE
        dict_cases[(x_case, y_case)][0].append(point) # On rajoute chaque point à la liste des points de la case à laquelle il appartient
            
            
    dict_graphes = {} # on initialise le dictionnaire des composantes connexes vide
    numero_graphe = 0
    for y in range(XY_MAX+1):
        for x in range(XY_MAX+1):
            
            points_case_act, graphe_act = dict_cases[(x,y)]
            if points_case_act: # si la case n'est pas vide (aucune raison d'étudier la connexité des points d'une case vide)
                if graphe_act is None: # Dans le cas ou la case n'appartient pas déjà à une composante connexe, on crée une nouvelle composante contenant cette case
                    dict_graphes[numero_graphe] = [(x,y)]
                    dict_cases[(x,y)][1] = numero_graphe
                    graphe_act = numero_graphe
                    numero_graphe += 1
                    
                # On procède à la fusion de la composante connexe de la case étudiée avec toutes les cases adjacentes 
                # On peut ne pas regarder les cases d'ordonnées supérieures à celle de la case actuelle au vu de l'ordre d'étude des cases
                for j in range(y,y+3):
                    for i in range(x-2,x+3):
                        if 0 <= i <= XY_MAX and 0 <= j <= XY_MAX:
                            fusion_graphes_cases(dict_cases, dict_graphes, graphe_act, points_case_act, (i,j), DIST_CARRE) 
                                
    # Fin de l'algo : on compte le nombre de pts dans chaque composante connexe
    liste_tailles_graphes = []
    for graphe in dict_graphes:
        compteur = 0
        for case in dict_graphes[graphe]:
            for point in dict_cases[case][0]:
                compteur += 1
        liste_tailles_graphes.append(compteur)
                    
    liste_tailles_graphes.sort(reverse=True)
    print(liste_tailles_graphes)
    
    
def main():
    """
    ne pas modifier: on charge une instance et on affiche les tailles
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        print_components_sizes(distance, points)


main()