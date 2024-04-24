'''
Final Project
Course: PHy407 - Computational Physics
By: Tahmeed Shafiq (1004574668)
'''

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit 
import random as rand
import time as time
import Functions as func

Lp = 101  # size of domain

# arrays to record the trajectory of the particle:
anchored = []

centre_point = (Lp-1)//2  # middle point of domain
anchored.append([centre_point,centre_point,centre_point]) # anchoring particle in the centre

start = time.time()

#While loop runs for 1000 particles
r=0
while len(anchored)<1000: #Runs over multiple particles
    z = False
    t =  0
    
    polar = rand.random()*2*np.pi - np.pi # random polar angle
    azimuthal = rand.random()*2*np.pi # random azimuthal angle
    r1 = r+1 # Radius for new particle
    zpp = round(r1*np.cos(polar)) + centre_point
    xpp = round(r1*np.sin(polar)*np.cos(azimuthal)) + centre_point
    ypp = round(r1*np.sin(polar)*np.sin(azimuthal)) + centre_point
    
    theta = rand.random()*2*np.pi - np.pi #Random angles for biased walk
                                          #Fixed for a given particle
    phi = rand.random()*2*np.pi
    
    while t<1: #Moves a single particle
        
        # Initiate random walk and check if new position sticky
        xpp,ypp,zpp = func.biased_walk_3d(xpp,ypp,zpp,theta,phi)
        z = func.sticky_test_3d(xpp,ypp,zpp,anchored)
        
        #new radius
        r_new = np.sqrt((xpp-centre_point)**2 + (ypp-centre_point)**2 + (zpp-centre_point)**2)
        
        #extinction radius check
        if r_new > r1 + 35:
            polar = rand.random()*2*np.pi - np.pi # reposition particle
            azimuthal = rand.random()*2*np.pi 
            zpp = round(r1*np.cos(polar)) + centre_point
            xpp = round(r1*np.sin(polar)*np.cos(azimuthal)) + centre_point
            ypp = round(r1*np.sin(polar)*np.sin(azimuthal)) + centre_point
    
            
        #For particles touching anchored particles
        if z==True:
            anchored.append([xpp,ypp,zpp])
            t = 1
            #increase radius as needed
            if r_new>r:
                r = r_new
         

#Measuring fractal dimensions: 2 methods
#Step 1: implement methods
lattice = func.latt(Lp,3,anchored) # Create binary lattice function
scale = np.linspace(0,101,101,dtype=int) # Choose your scaling
box = func.frac_dimen_3d(scale,lattice,centre_point) #Box method
R_g_array = func.mass_ratio_3d(anchored) #Radius of gyration method
N = np.linspace(0,1000,1000,dtype=int) #Create radius array for gyration method

# #Step 2: calculate D
BoxH, BoxCov = curve_fit(f,np.log(scale[13:25]),np.log(box[13:25]))
RH, RCov = curve_fit(f,np.log(N[500:-1]),np.log(R_g_array[500:]))
RH = 1/RH # taking inverse as required

#Step 3: error calc
BoxErr = np.sqrt(np.diag(BoxCov))
RErr = np.sqrt(np.diag(RCov))

#Last step: final value
D = (RH[0] + BoxH[0])/2
Err = np.sqrt(BoxErr[0]**2 + RErr[0]**2)
print('D is', D, 'with sigma', Err)

#How long did it take?
end = time.time()
diff = end - start
print('This program ran in', diff, 's')

#Have to unpack anchored particle coordinates
anchoredx, anchoredy, anchoredz = list(zip(*anchored))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(anchoredx,anchoredy,anchoredz)
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')
ax.set_title('3D DLA simulation')
plt.show()

plt.figure()
plt.plot(np.log(scale[12:20]),np.log(box[12:20]))
plt.title('3D Boxcounting: Log(count) against Log(scale)')
plt.xlabel('Log(Scale)')
plt.ylabel('Log(count)')
plt.show()

plt.figure()
plt.plot(np.log(N[500:-1]),np.log(R_g_array[500:]))
plt.title('3D Radius of gyration: Log(radius) against Log(growth stage)')
plt.xlabel('Log(Growth stage)')
plt.ylabel('Log(radius)')
plt.show()

