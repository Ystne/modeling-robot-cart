import math
import matplotlib.pyplot as plt
import numpy as np

def liste_de_caracteristiques_com(positions):
    caracteristiques = []
    orientation_actuelle = 0  # On suppose que le chariot commence avec une orientation de 0 degrés
    premiere_action_est_rotation = False
    
    for i in range(len(positions) - 1):
        dx = positions[i+1][0] - positions[i][0]
        dy = positions[i+1][1] - positions[i][1]
        distance = math.sqrt(dx**2 + dy**2)
        angle = (math.atan2(dy, dx))
        
        # Calculer la rotation nécessaire pour aligner le chariot avec la nouvelle direction
        rotation = (angle - orientation_actuelle)
        if i == 0 and rotation != 0:
            premiere_action_est_rotation = True
            orientation_actuelle=angle
            caracteristiques.append((1, rotation))
        
        if i>0 and rotation != 0:
            caracteristiques.append((1, rotation))
            orientation_actuelle = angle
        
        caracteristiques.append((0, distance))
    
    return caracteristiques, premiere_action_est_rotation
    

"""def calcul_intervalles_temps(caracteristiques, V0, omega_0):
    intervalles_temps = []
    temps_translation = 0
    temps_rotation = 0
    for caracteristique in caracteristiques:
        if caracteristique[0] == 0:  # Translation
            distance = caracteristique[1]
            temps_translation = distance / V0
            intervalles_temps.append(temps_translation)  # On stocke chaque translation séparément
        else:  # Rotation
            angle = caracteristique[1]
            temps_rotation = abs(angle) / omega_0
            intervalles_temps.append(temps_rotation)  # On stocke chaque rotation séparément

    return intervalles_temps"""

def calcul_intervalles_temps(caracteristiques, V0, omega_0):
    intervalles_temps = []

    for caracteristique in caracteristiques:
        if caracteristique[0] == 0:  # Translation
            distance = caracteristique[1]
            temps_translation = distance / V0
            intervalles_temps.append(temps_translation)  
        else:  # Rotation
            angle = caracteristique[1]
            temps_rotation = abs(angle) / omega_0   
            intervalles_temps.append(temps_rotation)

    return intervalles_temps





def liste_signes(caracteristiques): 
    liste = []
    for elt in caracteristiques: 
        if elt[0] == 1:  # C'est une rotation
            if elt[1] > 0:
                liste.append(1)  # Rotation positive
            elif elt[1] < 0:
                liste.append(-1)  # Rotation négative
            else:
                liste.append(0)  # Rotation nulle (évite les index incorrects)
        else:
            liste.append(0)  # Translation → on met 0 pour éviter les décalages

    return liste


def chemin_a_vit_a_traj(positions, V0, omega_0, pas=1/50):
    """
    Trace la trajectoire du chariot en fonction des positions et des vitesses données.
    """
    caracteristiques, premiere_action_est_rotation = liste_de_caracteristiques_com(positions)
    intervalles_temps = calcul_intervalles_temps(caracteristiques, V0, omega_0)
    

    signes_rotations = liste_signes(caracteristiques)  # Liste des signes des rotations

    temps = 0  # Initialisation du temps

    omega = []
    v = []
    t = []

    for i in range(len(intervalles_temps)):
        temps_discret=np.arange(temps,temps+intervalles_temps[i],pas)
        # Vérifier si on est sur une rotation ou une translation
        if caracteristiques[i][0] == 1:  # Rotation
                signe_rotation = signes_rotations[i]
                
                for j in temps_discret:
                    omega.append(signe_rotation * omega_0)
                    v.append(0)

        else:

                for j in temps_discret:
                    omega.append(0)
                    v.append(V0)


        temps += intervalles_temps[i] 
        t.extend(temps_discret)
    # Intégration des vitesses pour obtenir la trajectoire
    x = [positions[0][0]]
    y = [positions[0][1]]
    orientation = 0  # Orientation initiale en radians

    for i in range(len(t)):
        x.append(x[-1] + v[i] *pas  * math.cos(orientation))
        y.append(y[-1] + v[i]  *pas *  math.sin(orientation))
        orientation += omega[i] * pas 
    
    return v, omega, t, x, y







# Exemple de positions
positions = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2), (3, 3)]
V0 = 10  # Vitesse linéaire
omega_0 = 30  # Vitesse angulaire

# Tracer la trajectoire du chariot
chemin_a_vit_a_traj(positions, V0, omega_0)
