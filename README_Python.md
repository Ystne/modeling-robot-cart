# Planification de la trajectoire du chariot 

## Introduction

Nos différents codes python ont pour but la planification de trajectoire du chariot, son lissage, puis le calcul des commandes en vitesse pour obtenir la trajectoire, et le recalcul des trajectoires obtenues à partir des commandes en vitesse pour vérifier l'exactitude de la trajectoire réelle de notre robot . 

## Résumé du contenu du code 
Voici les différentes étapes de notre planification de trajectoire 
1. **Génération de l'environnement**: Génération d'une matrice de 0 et de 1, les 1 représentant les obstacles, une fonction permet la génération aléatoire d'un certain nombre d'îlot d'obstacle.

2. **Planification de la trajectoire**: Utilisation de l'algorithme du plus court chemin pour trouver la trajectoire optimale, puis la reconstruire. 
3. **Simplification du chemin**: On a une fonction qui vérifie la nécessité pour éviter les obstacles des virages, et les retire s'ils ne sont pas efficaces. 
4. **Interpolation avec des splines cubiques ou lissage par arc de cercle**: Une fonction permet de réaliser cette interpolation, une autre stratégie proposée est le lissage par arcs de cercle. 
5. **Obtention des commandes en vitesse**: fonction qui permet d'obtenir les commandes en vitesse pour une certaine trajectoire 
6. **Reconstruction finale**: Reconstruction à partir de la commande en vitesse du chemin final 

## Project Structure
```
📦 Project Root
 ├── main.py                  #  Script d'exécution principal
 ├── MAJGraphPonderInterpol.py # Planification de trajectoire et représetnation
 ├── TrajAcommande.py          # Génération des commandes en vitesse et fonction pour la reconstruction de trajectoire
 ├── LissageTrajRomain.py      # Deuxième stratégie de lissage 
 ├── README.md                 # Project documentation
 ├──recuperation_data.py 
```

## Librairies nécessaires
 Python 3.8+ , et : 
```bash
pip install numpy matplotlib scipy
```

## Decription des fichiers 

### `main.py` -  Script d'exécution principal

- Génère un environnement simulé.
- Calcule le chemin le plus court à l'aide d'une représentation graphique.
- Applique le lissage de la trajectoire et calcule les commandes de vitesse.
- Affiche une visualisation animée de la trajectoire.

### `MAJGraphPonderInterpol.py` -Planification de chemin
- Crée un environnement quadrillé avec des obstacles.
- Convertit l'environnement en une représentation graphique.
- Utilise l'algorithme de Dijkstra pour calculer le chemin le plus court.
- Applique l'interpolation spline cubique pour des transitions de chemin plus douces.

### `TrajAcommande.py` -Génération des commandes en vitesse et fonction pour la reconstruction de trajectoire
- Calcul des profils de vitesse linéaire et angulaire à partir de points de repère.
- Simule le contrôle du mouvement en temps réel sur la base des contraintes de vitesse.
- Reconstruit la trajectoire en intégrant la vitesse dans le temps.


### `LissageTrajRomain.py` - Lissage avancé et planification de mouvement
- Applique un lissage de la trajectoire pour supprimer les irrégularités.
- Calcule les contraintes de courbure pour un mouvement optimisé.
- Génère des trajectoires adaptées à la vitesse pour une exécution en douceur.

### recuperation_data.py
- à utiliser pour obtenir à partir des chemins retournés les données dans un format compatible avec matlab.  

## Execution Instructions
Pour exécuter la simulation :

```bash
python main.py
```
Le système génère une visualisation de :
- Le plus court chemin calculé, les trajectoires lissée.
- les graphiques représentant la commande en vitesses 
- Le mouvement final exécuté avec un contrôle basé sur la vélocité.

Attention ! Selon la disposition aléatoire des blocs, il peut être possible que certaines trajectoires n'existent pas, ou qu'aucune existe, une erreur est alors renvoyée. 

## Exemple de résultats
Les résultats de la simulation sont les suivants
1. **Carte des obstacles et trajectoire prévue**
   - Calcul du plus court chemin à l'aide d'algorithmes de recherche de graphes.
   - Trajectoire lissée à l'aide de splines.

2. **Profil de vitesse**
   - Commandes de vitesse linéaire et angulaire en fonction du temps.

3. **Exécution du mouvement final**
   - Trajectoire reconstruite à partir des vitesses calculées.

## Améliorations futures
- Intégration de la détection et de l'évitement des obstacles en temps réel.
- Mise en œuvre d'une replanification dynamique de la trajectoire.



