'''
Final Project
Course: PHy407 - Computational Physics
By: Tahmeed Shafiq (1004574668)
'''

import numpy as np
import matplotlib.pyplot as plt
import random as rand
import time as time
import Functions as func

Lp = 51  # size of domain; intentionally small so runs efficiently

# arrays to record the trajectory of the particle:
anchored = []

centre_point = (Lp-1)//2  # middle point of domain
anchored.append([centre_point,centre_point]) # anchoring particle in the centre

start = time.time()

#While loop runs while r is less than half the lattice width
r=0
while r<centre_point: #Runs over multiple particles
    z = False
    t =  0
    
    angle = rand.random()*2*np.pi # Random position for particle
    r1 = r+1 # Radius for new particle
    xpp = round(r1*np.cos(angle)) + centre_point
    ypp = round(r1*np.sin(angle)) + centre_point
    
    while t<1: #Moves a single particle
        
        # Initiate random walk and check break conditions
        xpp,ypp = func.nextmove(xpp,ypp)
        z = func.sticky_test(xpp,ypp,anchored)
        r_new = np.sqrt((xpp-centre_point)**2 + (ypp-centre_point)**2)
        
        if r_new > 2*r1:
            angle = rand.random()*2*np.pi # Random position for particle
            xpp = round(r1*np.cos(angle)) + centre_point
            ypp = round(r1*np.sin(angle)) + centre_point
            
        #For particles touching anchored particles
        if z==True:
            anchored.append([xpp,ypp])
            t = 1
            
            if r_new>r:
                r = r_new
        
         
end = time.time()
diff = end - start
print('This program ran in', diff, 's')

#Have to unpack anchored particle coordinates
anchoredx, anchoredy = list(zip(*anchored))

#plotting
plt.figure()
plt.title('DLA: Anchored particles')
plt.scatter(anchoredx, anchoredy,c='orange')
plt.plot(25,25,'vb',markersize=15,label='Anchor: (50,50)')
plt.legend()
plt.xlim(0,51) 
plt.xlabel('X Coordinate')
plt.ylim(0,51)
plt.ylabel('Y Coordinate')
plt.show()
