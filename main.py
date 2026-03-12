import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
from scipy.interpolate import splprep, splev
from itertools import product
import math 
from MAJGraphPonderInterpol import (
    generate_matrix_with_islands,
    salle_a_graphe,
    shortest_path,
    path,
    simplify_trajectory,
    cubicsplines_trajectory)
from LissageTrajRomain import ( 
    liste_de_caracteristiques,
    lissage,
    lissage_v_phi_point,
    tracer_trajectoire) 

from TrajAcommande import (
     chemin_a_vit_a_traj,
     liste_de_caracteristiques_com,
     liste_signes,
     chemin_a_vit_a_traj
     )

# Initialisation des paramètres
size = 40
num_islands = 7
max_island_size = 12
R = 1
START = (0, 0)
END = (size - 1, size - 1)
#Initialisation vitesses 

V0 = 2  # Vitesse linéaire
omega_0 =  0.5 # Vitesse angulaire

# Génération de la matrice et du graphe
carte = generate_matrix_with_islands(size, num_islands, max_island_size)
try:
    parent = shortest_path(salle_a_graphe(carte, R), START, END)
except ValueError as e:
    print(f"Erreur: {e}")
    exit()

# Calcul des trajectoires
trajectoire_paslisse = path(parent, START, END)
simplified = simplify_trajectory(trajectoire_paslisse, carte)
trajectoire = cubicsplines_trajectory(simplified, carte)
trajectoire_cubic = simplify_trajectory(trajectoire, carte)

# Calcul de la trajectoire lissée finale avec vitesses

L,R=liste_de_caracteristiques(trajectoire_paslisse)
liste = lissage(L,R)
v, phi_point, time = lissage_v_phi_point(L,liste, R)  
y_final,x_final = tracer_trajectoire(v, phi_point)

positions_trajcourb = [(i, j) for i, j in zip(x_final, y_final)]
print(positions_trajcourb)
#A partir de la trajectoire, calcul des vitesses, puis de la trajectoire réelle 
v_trajcourb, omega_trajcourb, t_trajcourb,x_trajcourb, y_trajcourb = chemin_a_vit_a_traj(positions_trajcourb, V0, omega_0)
v_traj_paslisse, omega_traj_paslisse, t_traj_paslisse, x_traj_paslisse, y_traj_paslisse = chemin_a_vit_a_traj(trajectoire_paslisse, V0, omega_0)
v_traj, omega_traj, t_traj, x_traj, y_traj =chemin_a_vit_a_traj(trajectoire, V0, omega_0)
v_traj_cubic, omega_traj_cubic, t_traj_cubic, x_traj_cubic, y_traj_cubic =chemin_a_vit_a_traj(trajectoire_cubic, V0, omega_0)


plt.plot(x_traj, y_traj, marker='o', linestyle='-')
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Trajectoire du robot")
plt.grid()
plt.show()

###################################### Affichage ###########################################

# Création de la figure
fig, ax = plt.subplots(figsize=(8, 8))

# Colormap personnalisée (0 = espace libre en gris, 1 = obstacles en noir)
cmap = mcolors.ListedColormap(['gray', 'black'])
ax.imshow(carte, cmap=cmap, interpolation='nearest')

# Définition des axes
ax.set_xticks(np.arange(0, carte.shape[1], 1))
ax.set_yticks(np.arange(0, carte.shape[0], 1))
ax.grid(which='both', color='black', linestyle='-', linewidth=0.5)

# Initialisation des lignes animées
line_original, = ax.plot([], [], 'bo-', markersize=3, label="Trajectoire originale")
line_simplified, = ax.plot([], [], 'go-', markersize=3, label="Trajectoire simplifiée")
line_smoothed, = ax.plot([], [], 'ro-', markersize=2, label="Trajectoire lissée")
line_smoothedcubic, = ax.plot([], [], 'yo-', markersize=2, label="Trajectoire lissée puis simplifiée")
"""line_final, = ax.plot([], [], 'co-', markersize=2, label="Trajectoire finale")"""

# Fonction d'initialisation pour l'animation
def init():
    line_original.set_data([], [])
    line_simplified.set_data([], [])
    line_smoothed.set_data([], [])
    line_smoothedcubic.set_data([], [])
    """line_final.set_data([], [])"""
    return line_original, line_simplified, line_smoothed, line_smoothedcubic #, line_final

# Fonction d'animation pour mettre à jour les trajectoires
def update(frame):
    if frame < len(trajectoire_paslisse):
        x1, y1 = zip(*trajectoire_paslisse[:frame+1])
        line_original.set_data(y1, x1)

    if frame < len(simplified):
        x2, y2 = zip(*simplified[:frame+1])
        line_simplified.set_data(y2, x2)

    if frame < len(trajectoire):
        x3, y3 = zip(*trajectoire[:frame+1])
        line_smoothed.set_data(y3, x3)

    if frame < len(trajectoire_cubic):
        x4, y4 = zip(*trajectoire_cubic[:frame+1])
        line_smoothedcubic.set_data(y4, x4)

    """if frame < len(positions_trajcourb):
        x5, y5 = zip(*positions_trajcourb[:frame+1])
        line_final.set_data(y5, x5)"""

    return line_original, line_simplified, line_smoothed, line_smoothedcubic

# Création de l'animation
frames_total = max(len(trajectoire_paslisse), len(simplified), len(trajectoire), len(trajectoire_cubic), len(positions_trajcourb))
ani = FuncAnimation(fig, update, frames=frames_total, init_func=init, blit=True, repeat=False)

# Suppression des entrées en double dans la légende
handles, labels = ax.get_legend_handles_labels()
unique_labels = dict(zip(labels, handles))  # Supprime les doublons
ax.legend(unique_labels.values(), unique_labels.keys())  # Affiche une légende unique

plt.show()


# Création des figures pour chaque vitesse linéaire
fig, ax_v1 = plt.subplots(figsize=(10, 5))
ax_v1.plot(t_traj_paslisse, v_traj_paslisse, 'b-', label="Vitesse - Traj. originale")
ax_v1.set_xlabel("Temps (s)")
ax_v1.set_ylabel("Vitesse (m/s)")
ax_v1.set_title("Vitesse - Trajectoire originale")
ax_v1.legend()
ax_v1.grid()
plt.show()

fig, ax_v2 = plt.subplots(figsize=(10, 5))
ax_v2.plot(t_traj, v_traj, 'r-', label="Vitesse - Traj. lissée")
ax_v2.set_xlabel("Temps (s)")
ax_v2.set_ylabel("Vitesse (m/s)")
ax_v2.set_title("Vitesse - Trajectoire lissée")
ax_v2.legend()
ax_v2.grid()
plt.show()

fig, ax_v3 = plt.subplots(figsize=(10, 5))
ax_v3.plot(t_traj_cubic, v_traj_cubic, 'g-', label="Vitesse - Traj. lissée puis simplifiée")
ax_v3.set_xlabel("Temps (s)")
ax_v3.set_ylabel("Vitesse (m/s)")
ax_v3.set_title("Vitesse - Trajectoire lissée puis simplifiée")
ax_v3.legend()
ax_v3.grid()
plt.show()

fig, ax_v4 = plt.subplots(figsize=(10, 5))
ax_v4.plot(t_trajcourb, v_trajcourb, 'y-', label="Vitesse - Traj. finale")
ax_v4.set_xlabel("Temps (s)")
ax_v4.set_ylabel("Vitesse (m/s)")
ax_v4.set_title("Vitesse - Trajectoire finale")
ax_v4.legend()
ax_v4.grid()
plt.show()

# Création des figures pour chaque vitesse angulaire
fig, ax_w1 = plt.subplots(figsize=(10, 5))
ax_w1.plot(t_traj_paslisse, omega_traj_paslisse, 'b-', label="Omega - Traj. originale")
ax_w1.set_xlabel("Temps (s)")
ax_w1.set_ylabel("Vitesse angulaire (rad/s)")
ax_w1.set_title("Vitesse angulaire - Trajectoire originale")
ax_w1.legend()
ax_w1.grid()
plt.show()

fig, ax_w2 = plt.subplots(figsize=(10, 5))
ax_w2.plot(t_traj, omega_traj, 'r-', label="Omega - Traj. lissée")
ax_w2.set_xlabel("Temps (s)")
ax_w2.set_ylabel("Vitesse angulaire (rad/s)")
ax_w2.set_title("Vitesse angulaire - Trajectoire lissée")
ax_w2.legend()
ax_w2.grid()
plt.show()

fig, ax_w3 = plt.subplots(figsize=(10, 5))
ax_w3.plot(t_traj_cubic, omega_traj_cubic, 'g-', label="Omega - Traj. lissée puis simplifiée")
ax_w3.set_xlabel("Temps (s)")
ax_w3.set_ylabel("Vitesse angulaire (rad/s)")
ax_w3.set_title("Vitesse angulaire - Trajectoire lissée puis simplifiée")
ax_w3.legend()
ax_w3.grid()
plt.show()

fig, ax_w4 = plt.subplots(figsize=(10, 5))
ax_w4.plot(t_trajcourb, omega_trajcourb, 'y-', label="Omega - Traj. finale")
ax_w4.set_xlabel("Temps (s)")
ax_w4.set_ylabel("Vitesse angulaire (rad/s)")
ax_w4.set_title("Vitesse angulaire - Trajectoire finale")
ax_w4.legend()
ax_w4.grid()
plt.show()

# --------------------------------------------

# Exemple de positions


# Création de la figure pour les trajectoires obtenues à partir des vitesses
fig, ax2 = plt.subplots(figsize=(8, 8))

# Vérification que la matrice 'carte' existe
if 'carte' in globals():
    cmap = mcolors.ListedColormap(['gray', 'black'])
    ax2.imshow(carte, cmap=cmap, interpolation='nearest')

    # Tracé des trajectoires obtenues
    ax2.plot(y_traj_paslisse, x_traj_paslisse, 'b-', label="Traj. originale")
    ax2.plot(y_traj, x_traj, 'r-', label="Traj. lissée")
    ax2.plot(y_traj_cubic, x_traj_cubic, 'g-', label="Traj. lissée puis simplifiée")
    """ax2.plot(y_trajcourb, x_trajcourb, 'y-', label="Traj. finale")"""

    ax2.set_xticks(np.arange(0, carte.shape[1], 1))
    ax2.set_yticks(np.arange(0, carte.shape[0], 1))
    ax2.grid(which='both', color='black', linestyle='-', linewidth=0.5)
    ax2.legend()
    ax2.set_title("Trajectoires obtenues à partir des vitesses calculées")
else:
    print("Erreur : La matrice 'carte' n'existe pas.")
plt.axis("equal")  # Assurer une échelle cohérente entre X et Y

plt.show()
