#!/usr/bin/env python3
"""
compute sizes of all connected components.
sort and display.
"""

import time
from sys import argv
from math import sqrt


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


class Point:
    """
    un point est défini par un vecteur de dimension deux dans notre cas
    """
    def __init__(self, coordinates):
        """
        construit un nouveau point basé sur les coordonnées données
        """
        self.coordinates = coordinates
        self.x = coordinates[0]
        self.y = coordinates[1]

    def distance_carre(self, point2):
        """
        euclidean distance between two points.
        """
        total = 0
        for c_1, c_2 in zip(self.coordinates, point2.coordinates):
            diff = c_1 - c_2
            total += diff * diff
        return total

    def in_quadrant(self, point, distance):
        return self.x - distance <= point.x <= self.x + distance and \
                self.y - distance <= point.y <= self.y + distance


def graphe_connexe_recherche1(distance, dist_calcul, points, centre):
    """
    centre est un point de la liste de points
    centre n'existe plus dans points !!!

    renvoit un graphe connexe remplit, ainsi que les points restants
    """
    maxi = -1
    Graphe = [centre]
    largeur = distance
    while maxi != 0:
        # 1: rechercher tous les points du quadrant de demi_coté:distance
        # en utilisant in_quadrant pour d = distance.
        # 2: les rajouter dans la Pile et dans la liste des suppression à faire
        # au sein de points, si d<distance
        # 3: aggrandir quadrant d'une distance dmax calculée lorsqu'on ajoute
        # un point au graphe.
        point_restant = [] # correspond à notre future Liste de points non marqués
        maxi = 0  # si on ajoute aucun point, on sort du While
        for point_etude in points:  # etape 1:
            if centre.in_quadrant(point_etude, largeur):
                # le point est dans le cadran mais pas forcément
                # relié aux points du graphe
                for point_existant in Graphe:
                    d = point_existant.distance_carre(point_etude)
                    if d <= dist_calcul:  # on est dans le graphe connexe
                        maxi = max(maxi, sqrt(centre.distance_carre(point_etude)))
                        Graphe.append(point_etude)
                        break
                    else:
                        point_restant.append(point_etude)
            else:
                point_restant.append(point_etude)
        if maxi > 0:
            largeur = maxi + distance # on augmenet notre carré d'une courrone maxi

    return (Graphe, point_restant)


def print_components_sizes(distance, points):
    """
    affichage des tailles triees de chaque composante
    """
    """solution avec quadrant"""
    Nuage = [] # Liste des graphes connexes
    dist_calcul = distance * distance # calculée une seule fois
    while points != []: # tant que tous les points ne sont pas marqués
        centre = points.pop()
        # recherche du graphe connexe à partir du point actuel
        # ce point est bien sur soustrait à points
        Graphe, points = graphe_connexe_recherche1(distance,
                                                   dist_calcul,
                                                   points, centre)
        # on a un graphe connexe, on passe au suivant
        # pour cela on prend centre = points[-1]
        Nuage.append(Graphe)
    taille = [len(gr) for gr in Nuage]
    taille.sort(reverse=True)
    print(taille)


def main():
    """
    ne pas modifier: on charge une instance et on affiche les tailles
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        print_components_sizes(distance, points)


main()