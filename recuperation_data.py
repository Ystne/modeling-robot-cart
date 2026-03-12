from TrajAcommande import *
import numpy as np
from scipy.io import savemat

V0=1
omega_0=1
positions=[(0,0),(1,1),(2,2),(2,3),(3,3),(4,3),(5,3),(6,3),(6,2),(6,1),(5,0),(4,-1),(4,-2),(3,-2),(2,-2),(1,-1),(0,-1),(0,0)]
v,omega,t,x,y=chemin_a_vit_a_traj(positions, V0, omega_0, pas=1/100)







data_v={"t":t, "v":v}
savemat('data_v.mat', {'data_v': data_v})

data_dphi={"t":t, "dphi":omega}
savemat('data_omega.mat', {'data_dphi': data_dphi})


