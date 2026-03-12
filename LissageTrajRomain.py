

#MODULES ET BIB
import math 
import matplotlib.pyplot as plt

#PARAMETRES
Vmin = 0.01 
Mmax = 0.1 
l = 0.3  # Écart entre les roues 
pas = 1/100
V0 = 0.5
omega_0 = 30

# Calcul du rayon de courbure minimal 
R_min = Vmin**2 * 2 / (9.81 * l)


#LISTES DE DISTANCES ET D'ANGLES
def liste_de_caracteristiques(positions):
    dist_parcourue = 0
    distances = []
    orientation_actuelle = None  # Orientation initiale (None pour ne pas forcer une rotation initiale)
    angles = []  # Liste des rotations
    for i in range(len(positions) - 1):
        dx = positions[i + 1][0] - positions[i][0]
        print(dx)
        dy = positions[i + 1][1] - positions[i][1]
        distance = math.sqrt(dx**2 + dy**2)
        angle = math.degrees(math.atan2(dy, dx))
        print(i,angle, "angle")

        # Première orientation
        if orientation_actuelle is None : 
            orientation_actuelle = angle
       
        
        rotation = angle - orientation_actuelle
        print(orientation_actuelle, "orientation" )
        orientation_actuelle += rotation 
        
        
       
        if rotation != 0: 
            
            angles.append(rotation)
            distances.append(dist_parcourue)
            dist_parcourue = distance
            
            
        else : 
            print("boucle 2", i)
            dist_parcourue += distance
            
    distances.append(dist_parcourue)   
    return distances, angles

#LISSAGE : 
def lissage(distances,angles): 
    # R : une liste contenant : (indice du sommet où il y a rotation, angle de rotation, d'avant, d'après)
    # liste : une liste contenant : 0 si il faut s'arrêter au sommet i, (d, RC, signe) sinon : 
    # d : distance à laquelle on déclenche la courbe, RC : rayon de courbure  
    liste = []
    
    
    for i in range(len(distances)-1): 
        
        alpha = angles[i]
        d1, d2 = distances[i],distances[i+1]
        signe = alpha / abs(alpha)
        alpha = abs(alpha) 
        alpha = 180 - alpha
        
        d_max =  0.5*min(d1, d2)
        if R_min > d_max / abs(math.tan(math.radians(alpha / 2))): 
            liste.append((0, 0, 0, signe))
        else: 
            beta = (1 / math.tan(math.radians(alpha / 2)) + math.tan(math.radians((180 - alpha) / 2))) * math.cos(math.radians(alpha / 2)) -1
            RC = min(abs(Mmax / beta), d_max * abs(math.tan(math.radians(alpha / 2)))) 
            
            d = RC / abs(math.tan(math.radians(alpha / 2)))
            liste.append((1, d, RC, signe))
    return liste 


def lissage_v_phi_point(distances,liste, angles): 
    """_summary_

    Args:
        liste (list): la liste renvoyée par lissage, contenant les distances auxquelles on déclenche la rotation
    """
    v = []
    phi_point = []
    time = []
    temps = 0
    
    for i in range(len(liste)):
        # Cas numéro 1 : si pas la place :     
        if liste[i][0] == 0: 
            print("je suis un gros bouffon")
            alpha = angles[i]
            d1  = distances[i]
            tau1=(d1) / (V0)
            N1 = int((d1 ) / (V0 * pas))
            for k in range(N1):
                v.append(V0)
                phi_point.append(0)
                time.append(k * pas + temps)
            temps += tau1 
            vit_angulaire = omega_0 * liste[i][3]
            tau2 =  abs((alpha)) / (vit_angulaire)
            N2 = int(abs((alpha) / (vit_angulaire * pas)))
            for k in range(N2): 
                v.append(0)
                phi_point.append(vit_angulaire)
                time.append(k * pas + temps)
            temps += tau2
        else:
            if not i :  
                
                #translation rectiligne numéro 0 : 
                d1 = distances[i]
                tau1 = (d1  - liste[i][1]) / (V0)
               
                N1 = int(abs((d1  - liste[i][1]) / (V0 * pas)))
                for k in range(N1):
                    v.append(V0)
                    phi_point.append(0)
                    time.append(k * pas + temps)
                temps += tau1
                
                 #arc de cercle numéro 0 : 
                alpha = angles[i]
                alpha = math.radians(alpha)
                vit_angulaire = V0 / liste[i][2]*liste[i][3]
                tau2 = abs((alpha) / (vit_angulaire))
                
                
                N2 = int(abs((alpha) / (vit_angulaire * pas)))
                for k in range(N2):
                    v.append(V0)
                    phi_point.append(vit_angulaire)
                    time.append(k * pas + temps)
                temps += tau2
            
                 
            elif i :  
                
                #translation rect i : 
                
                d1 = distances[i]
                tau1 = (d1 - liste[i-1][1] - liste[i][1]) / (V0)
                N1 = int(abs((d1 - liste[i-1][1] - liste[i][1]) / (V0 * pas)))
                for k in range(N1):
                    v.append(V0)
                    phi_point.append(0)
                    time.append(k * pas + temps)
                temps += tau1
                
                #rotation i : 
                alpha = angles[i]
                alpha = math.radians(alpha)
                vit_angulaire = V0 / liste[i][2]*liste[i][3]
                tau2 = abs((alpha) / (vit_angulaire))
                
                
                N2 = int(abs((alpha) / (vit_angulaire * pas)))
                for k in range(N2):
                    v.append(V0)
                    phi_point.append(vit_angulaire)
                    time.append(k * pas + temps)
                temps += tau2
            """if  i== len(liste) - 1:  
                
                t, alpha, d1, d2 = R[i]
                d1, d2 = distances[i],None
                alpha = math.radians(alpha)
                
                tau1 = (d1*2 - liste[i-1][1] ) / (V0)
               
                
                N1 = int(abs((d1*2 - liste[i-1][1]) / (V0 * pas)))
                for k in range(N1):
                    v.append(V0)
                    phi_point.append(0)
                    time.append(k * pas + temps)
                temps += tau1
                
                vit_angulaire = V0 / liste[i][2]*liste[i][3]
                
                
                tau2 = abs((alpha) / (vit_angulaire))"""
                
                
                
    return v, phi_point, time

#tests 
positions =[(0,0), (0,1),(1,1),(1,2),(3,4),(4,6),(6,7)]
L,R=liste_de_caracteristiques(positions)
liste = lissage(L,R)
v, phi_point, time = lissage_v_phi_point(L,liste, R)  


#imprimante : 
print(L)





# Tracé : 
plt.plot(time, v, label='Vitesse de translation')
plt.plot(time, phi_point, label='Vitesse de rotation')
plt.xlabel('Temps (s)')
plt.ylabel('Vitesse')
plt.legend()
plt.show()
def tracer_trajectoire(v, phi_point, pas=1/100):
    x = [0]  
    y = [0]  
    orientation = 0  
    
    for i in range(len(v)):
        orientation += -phi_point[i] * pas  
        x.append((x[-1] + V0 * pas * math.cos(orientation)))
        y.append(y[-1] + V0 * pas * math.sin(orientation))

        

    return x,y 

# Tracer la trajectoire du chariot

tracer_trajectoire(v, phi_point)

#TEST : 

print(liste_de_caracteristiques(positions))
