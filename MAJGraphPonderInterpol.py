import random
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
from scipy.interpolate import CubicSpline
from itertools import product 
from scipy.interpolate import splprep, splev
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from matplotlib.animation import FuncAnimation

size = 58
num_islands = 10
max_island_size = 15
R = 1
START = (0, 0)
END = (size - 1, size - 1)


###############################################Functions##############################################################

def generate_matrix_with_islands(size=58, num_islands=10, max_island_size=5):
    """
    Génère une matrice de dimensions `size x size` avec des îlots d'obstacles.

    Args:
        size (int): Taille de la matrice (par défaut 58x58).
        num_islands (int): Nombre d'îlots à générer.
        max_island_size (int): Taille maximale (côté) de chaque îlot carré.

    Returns:
        np.array: Matrice avec des îlots d'obstacles.
    """
    # Initialiser une matrice de zéros
    matrix = np.zeros((size, size), dtype=int)

    for _ in range(num_islands):
        # Générer une position de départ aléatoire pour l'îlot
        start_row = random.randint(0, size - max_island_size)
        start_col = random.randint(0, size - max_island_size)

        # Générer une taille aléatoire pour l'îlot
        island_height = random.randint(1, max_island_size)
        island_width = random.randint(1, max_island_size)

        # Limiter l'îlot à ne pas dépasser les bords de la matrice
        end_row = min(start_row + island_height, size)
        end_col = min(start_col + island_width, size)

        # Placer l'îlot dans la matrice (valeur 1 pour les obstacles)
        matrix[start_row:end_row, start_col:end_col] = 1

    return matrix

def is_path_clear(i, j, ni, nj, carte):
    """Vérifie si un chemin entre (i, j) et (ni, nj) est libre."""
    di, dj = ni - i, nj - j
    steps = max(abs(di), abs(dj))  # Nombre de points intermédiaires à vérifier
    for step in range(1, steps + 1):
        intermediate_i = int(round(i + (di * step) / steps))
        intermediate_j = int(round(j + (dj * step) / steps))
        if carte[intermediate_i, intermediate_j] == 1:  # Obstacle trouvé
            return False
    return True

def salle_a_graphe(carte, R=1):
    """Crée une liste d'adjacence avec poids en tenant compte des diagonales."""
    
    largeur, longueur = carte.shape
    Dico_adj = {}

    # Générer les déplacements (inclut diagonales)
    offsets = [(di, dj, 1 if abs(di) + abs(dj) == 1 else np.sqrt(2)) 
               for di, dj in product(range(-R, R + 1), repeat=2) 
               if (di != 0 or dj != 0)]


    # Construire la liste d'adjacence avec coûts
    for i, j in zip(*np.where(carte == 0)):
        voisins = []
        for di, dj, cost in offsets:
            ni, nj = i + di, j + dj
            if 0 <= ni < largeur and 0 <= nj < longueur and carte[ni, nj] == 0:
                if is_path_clear(i, j, ni, nj,carte):
                    voisins.append(((ni, nj), cost))  # Stocker le voisin avec son coût
        Dico_adj[(i, j)] = voisins

    return Dico_adj

# Shortest path en prenant en compte le poids des diagonales 
def extract_min_dist(frontier, dist):
    """Extrait le sommet avec la plus petite distance dans la frontière"""
    min_node = min(frontier, key=lambda node: dist.get(node, float('inf')))
    frontier.remove(min_node)
    return min_node

def shortest_path(graph, s, t):
    """
    Trouve le plus court chemin entre s et t dans un graphe pondéré, en utilisant la sortie de `salle_a_listedadj_vectorise`.
    
    Args:
        graph (dict): Liste d'adjacence sous forme {sommet: [(voisin1, coût1), (voisin2, coût2)]}.
        s (tuple): Point de départ (x, y).
        t (tuple): Point d'arrivée (x, y).
        
    Returns:
        dict: Dictionnaire des parents permettant de reconstruire le chemin.
    """
    # Initialisation
    frontier = [s]  # Liste des sommets à explorer
    parent = {s: None}  # Parent de chaque sommet dans le chemin
    dist = {s: 0}  # Distance minimale pour atteindre chaque sommet
    
    # Tant qu'il reste des sommets à explorer
    while frontier:
        # Extraire le sommet avec la plus petite distance
        x = extract_min_dist(frontier, dist)

        # Si on atteint la cible, on retourne les parents
        if x == t:
            return parent

        # Explorer les voisins
        for y, cost in graph.get(x, []):  # Chaque voisin y et son coût
            new_dist = dist[x] + cost  # Nouveau coût pour atteindre y
            if y not in dist or new_dist < dist[y]:  # Met à jour si meilleure distance
                dist[y] = new_dist
                parent[y] = x
                if y not in frontier:  # Ajouter y à la frontière s'il n'y est pas déjà
                    frontier.append(y)
    
    # Si aucun chemin n'a été trouvé
    raise ValueError("Aucun chemin trouvé")
    return False


def path(parent, s, t):
    """Reconstruit le chemin à partir du dictionnaire des parents."""
    if t not in parent:
        raise ValueError("Aucun chemin trouvé entre le point de départ et le point d'arrivée.")
    chemin = []
    sommet = t
    while sommet != s:
        chemin.append(sommet)
        sommet = parent[sommet]
    chemin.reverse()
    return chemin

 
def simplify_trajectory(trajectory, carte):
    """Simplifie une trajectoire en éliminant les virages inutiles."""
    simplified = [trajectory[0]]
    for i in range(1, len(trajectory) - 1):
        A = simplified[-1]
        C = trajectory[i + 1]
        if is_path_clear(A[0], A[1], C[0], C[1], carte):
            continue
        simplified.append(trajectory[i])
    simplified.append(trajectory[-1])
    return simplified



def cubicsplines_trajectory(path, carte, smoothness=1, step_factor=10):
    """
    Lisse une trajectoire discrète avec des splines cubiques tout en respectant les obstacles.

    Args:
        path (list): Liste des points discrets de la trajectoire [(x1, y1), (x2, y2), ...].
        carte (np.array): Matrice des obstacles (0 = libre, 1 = obstacle).
        smoothness (float): Contrôle le degré de lissage (valeur plus grande = plus lisse).
        step_factor (int): Contrôle la densité des points interpolés.

    Returns:
        list: Liste des coordonnées lissées (trajet valide sans obstacle).

    """
    if len(path) <= 3:  # Vérification si le nombre de points est suffisant
        return path  
    # Extraire les coordonnées X et Y
    x = [p[0] for p in path]
    y = [p[1] for p in path]

    # Interpolation avec les splines cubiques
    tck, u = splprep([x, y], s=smoothness)
    u_fine = np.linspace(0, 1, len(path) * step_factor)  # Densité des points interpolés
    smooth_x, smooth_y = splev(u_fine, tck)

    # Vérification et filtrage des coordonnées lissées
    carte_coords = []
    last_valid = None  # Dernière coordonnée valide ajoutée
    for i in range(len(smooth_x) - 1):
        sx, sy = smooth_x[i], smooth_y[i]
        sx_next, sy_next = smooth_x[i + 1], smooth_y[i + 1]

        # Arrondir les coordonnées pour les placer dans la matrice 
        ix, iy = int(round(sx)), int(round(sy))
        ix_next, iy_next = int(round(sx_next)), int(round(sy_next))

        # Vérifier les limites de la matrice
        if 0 <= ix < carte.shape[0] and 0 <= iy < carte.shape[1]:
            if 0 <= ix_next < carte.shape[0] and 0 <= iy_next < carte.shape[1]:
                # Vérifier que le segment entre (ix, iy) et (ix_next, iy_next) ne traverse pas d'obstacle
                if carte[ix, iy] == 0 and carte[ix_next, iy_next] == 0:
                    if is_path_clear(ix, iy, ix_next, iy_next, carte):  
                        if not last_valid or last_valid != (ix, iy):  
                            carte_coords.append((ix, iy))
                            last_valid = (ix, iy)

    # Forcer le premier et le dernier point pour être sûr qu'il soit inclus dans le chemin 
    if carte_coords and carte_coords[0] != path[0]:
        carte_coords.insert(0, path[0]) 

    if carte_coords and carte_coords[-1] != path[-1]:
        carte_coords.append(path[-1])   

    return carte_coords

######################################Main###########################################
carte = generate_matrix_with_islands(size, num_islands, max_island_size)
parent = shortest_path(salle_a_graphe(carte, R),START, END)
trajectoire_paslisse = path(parent,START, END)
simplified = simplify_trajectory(trajectoire_paslisse, carte)
trajectoire = cubicsplines_trajectory(simplified, carte)
trajectoire_cubic = simplify_trajectory(trajectoire, carte)


"""######################################Affichage###########################################

# Création de la figure
fig, ax = plt.subplots(figsize=(8, 8))

# Colormap personnalisée (0 = espace libre en gris, 1 = obstacles en noir)
cmap = mcolors.ListedColormap(['gray', 'black'])
ax.imshow(carte, cmap=cmap, interpolation='nearest')

# Initialisation des lignes pour chaque trajectoire
line_original, = ax.plot([], [], 'bo-', markersize=3, label="Trajectoire originale")
line_simplified, = ax.plot([], [], 'go-', markersize=3, label="Trajectoire simplifiée")
line_smoothed, = ax.plot([], [], 'ro-', markersize=2, label="Trajectoire lissée")
line_smoothedcubic, = ax.plot([], [], 'yo-', markersize=2, label="Trajectoire lissée puis simplifiée")

# Définir l'échelle des axes
ax.set_xticks(np.arange(0, carte.shape[1], 1))
ax.set_yticks(np.arange(0, carte.shape[0], 1))
ax.grid(which='both', color='black', linestyle='-', linewidth=0.5)
ax.legend()

# Fonction d'initialisation pour l'animation
def init():
    line_original.set_data([], [])
    line_simplified.set_data([], [])
    line_smoothed.set_data([], [])
    line_smoothedcubic.set_data([], [])
    return line_original, line_simplified, line_smoothed, line_smoothedcubic

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

    return line_original, line_simplified, line_smoothed, line_smoothedcubic

# Création de l'animation
frames_total = max(len(trajectoire_paslisse), len(simplified), len(trajectoire), len(trajectoire_cubic))
ani = FuncAnimation(fig, update, frames=frames_total, init_func=init, blit=True, repeat=False)

# Affichage
plt.show()
"""