#!/usr/bin/env python3
"""
compute sizes of all connected components.
sort and display.
"""

from sys import argv

class Point:
    """On définit une classe de points un peu mieux"""
    def __init__(self, coordinates, marque = False):
        """constructeur"""
        self.coordinates = coordinates
        self.marque = marque

    def distance_to(self, other):
        """
        euclidean distance between two points.
        """
        if self < other:
            return other.distance_to(self)  # we are now a symmetric function

        total = 0
        for c_1, c_2 in zip(self.coordinates, other.coordinates):
            diff = c_1 - c_2
            total += diff * diff
        return total

    def isInBox(self, other, distance):
        """determine si le point est dans le quadrant de centre other de demicoté distance"""
        xS, yS = self.coordinates
        xO, yO = other.coordinates
        return xO - distance <= xS <= xO + distance and yO - distance <= yS <= yO + distance

    def __lt__(self, other):
        """
        lexicographical comparison
        """
        return self.coordinates <= other.coordinates

    def __eq__(self, other):
        """Eq"""
        return self.coordinates == other.coordinates


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


def print_components_sizes(distance, points): # Je n'ai pas commenté, les commentaires auraient étés trop redondants avec le pseudo-code. Voir "ALgorithme BFS" dans le compte rendu.
    """
    affichage des tailles triees de chaque composante
    """
    distance_carre = distance * distance
    liste_graphes = []
    
    while points != []:
        pile_actuelle = []
        graphe_actuel = []
        point_etudie = points.pop()   
        point_etudie.marque = True
        pile_actuelle.append(point_etudie)
        while pile_actuelle != []: 
            point_test = pile_actuelle.pop()
            graphe_actuel.append(point_test)
            for point in points:
                if point_test.isInBox(point, distance):
                    if point.distance_to(point_test) < distance_carre:
                        pile_actuelle.append(point)
            for point in pile_actuelle:
                if not point.marque:
                    points.remove(point)
                    point.marque = True
        liste_graphes.append(graphe_actuel)
        
    liste_tailles_graphes = [len(graphe) for graphe in liste_graphes]
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