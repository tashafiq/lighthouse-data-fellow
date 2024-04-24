'''
Final Project
Course: PHy407 - Computational Physics
By: Tahmeed Shafiq (1004574668)
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import random as rand
import time as time
import Functions as func

Lp = 101  # size of domain; larger than base model

# arrays to record the trajectory of the particle:
anchored = []

centre_point = (Lp-1)//2  # middle point of domain
anchored.append([centre_point,centre_point]) # anchoring particle in the centre

start = time.time() # for measuring comp time

#While loop runs for 1000 particles
r=0
while len(anchored)<1001: #Runs over multiple particles
    z = False
    t =  0
    
    angle = rand.random()*2*np.pi # Random angle for particle
    r1 = r+1 # Radius for new particle
    xpp = round(r1*np.cos(angle)) + centre_point # Random position 
    ypp = round(r1*np.sin(angle)) + centre_point # Random position
    
    phi = rand.random()*2*np.pi #Random angle for biased walk
                                #Fixed for a given particle
    
    while t<1: #Moves a single particle
        
        # Initiate random walk and check if new position sticky
        xpp,ypp = func.biased_walk(xpp,ypp,phi)
        z = func.sticky_test(xpp,ypp,anchored)
        
        #compute new radius
        r_new = np.sqrt((xpp-centre_point)**2 + (ypp-centre_point)**2)
        
        #extinction radius check
        if r_new > r1 + 35:
            angle = rand.random()*2*np.pi # Random position for particle
            xpp = round(r1*np.cos(angle)) + centre_point
            ypp = round(r1*np.sin(angle)) + centre_point
            
        #for particles touching anchored particles
        if z==True:
            anchored.append([xpp,ypp])
            t = 1
            #increase radius as needed
            if r_new>r:
                r = r_new
        
#Measuring fractal dimensions: 2 methods
#Step 1: implement methods
lattice = func.latt(Lp,2,anchored) # Create binary lattice function
scale = np.linspace(0,101,101,dtype=int) # Choose your scaling
box = func.frac_dimen(scale,lattice,centre_point)[0] #Box method
R_g_array = func.mass_ratio(anchored) #Radius of gyration method
N = np.linspace(0,1000,1000,dtype=int) #Create radius array for gyration method

# #Step 2: calculate D
BoxH, BoxCov = curve_fit(f,np.log(scale[5:20]),np.log(box[5:20]))
RH, RCov = curve_fit(f,np.log(N[500:999]),np.log(R_g_array[500:999]))
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
anchoredx, anchoredy = list(zip(*anchored))

#Plot figure
plt.figure()
plt.title('Optimized DLA: Anchored particles')
plt.scatter(anchoredx, anchoredy,c='orange')
plt.plot(50,50,'vb',markersize=10,label='Anchor: (50,50)')
plt.legend()
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.show()

#Plot boxcounting
plt.figure()
plt.title('2D Boxcounting: Log(count) against Log(scale)')
plt.plot(np.log(scale[5:20]),np.log(box[5:20]))
plt.xlabel('Log(Scale)')
plt.ylabel('Log(count)')
plt.show()

#Plot gyration method
plt.figure()
plt.title('2D Radius of gyration: Log(radius) against Log(growth stage)')
plt.plot(np.log(N[500:999]),np.log(R_g_array[500:999]))
plt.xlabel('Log(Growth stage)')
plt.ylabel('Log(radius)')
plt.show()