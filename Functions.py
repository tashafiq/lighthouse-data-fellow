'''
Final Project
Course: PHy407 - Computational Physics
By: Tahmeed Shafiq (1004574668)
'''

import numpy as np
import random as rand

def nextmove(x, y):
    """ randomly choose a direction
    0 = up, 1 = down, 2 = left, 3 = right"""
    direction =  rand.randrange(4)# COMPLETE

    if direction == 0:  # move up
        y += 1
    elif direction == 1:  # move down
        y -= 1
    elif direction == 2:  # move right
        x += 1
    elif direction == 3:  # move left
        x -= 1
    else:
        print("error: direction isn't 0-3")

    return x, y

def biased_walk(x,y,phi):
    """
    Choose a biased random direction 
    theta = random angle, lambda = random scaling factor"""
    
    theta = rand.random()*(2*np.pi) - np.pi
    Lambda = rand.random()
    x = x + np.cos(phi + Lambda*theta)
    x = round(x)
    y = y + np.sin(phi + Lambda*theta)
    y = round(y)
    
    return x,y

def biased_walk_3d(x,y,z,polar0,azim0):
    """
    Choose a bias random 3D direction using spherical coords
    polar,azim = random polar, azimuthal angle 
    l1,L2 = random scaling factors"""
    
    polar = rand.random()*(2*np.pi) - np.pi
    azim = rand.random()*2*np.pi
    L1 = rand.random()
    L2 = rand.random()
    x = x + 2*np.sin(polar0 + L1*polar)*np.cos(azim0 + L2*azim)
    x = round(x)
    y = y + 2*np.sin(polar0 + L1*polar)*np.sin(azim0 + L2*azim)
    y = round(y)
    z = z + 2*np.cos(polar0 + L1*polar)
    z =round(z)
    
    return x,y,z
    

def sticky_test(xpp,ypp,pos):
    '''
    Asks the question:
    "Is the particle on a 'sticky' square,
    adjacent to anchored particles?" Returns
    True if true

    Parameters
    ----------
    xpp : x position.
    ypp : y position
    pos : array of anchored particles

    Returns
    -------
    True/False

    '''
    a=False
    for i in range(0,len(pos)):
        if (pos[i][0] - xpp)**2 + (pos[i][1] - ypp)**2 <= 2:
            a=True
    return(a)

def sticky_test_3d(xpp,ypp,zpp,pos):
    '''
    Asks the question:
    "Is the particle on a 'sticky' square,
    adjacent to anchored particles?" Returns
    True if true

    Parameters
    ----------
    xpp : x position.
    ypp : y position
    pos : array of anchored particles

    Returns
    -------
    True/False

    '''
    a=False
    for i in range(0,len(pos)):
        if (pos[i][0] - xpp)**2 + (pos[i][1] - ypp)**2 + (pos[i][2] - zpp)**2 <= 3:
            a=True
    return(a)

def latt(Lp,dim,anchored):
    '''
    Creates a lattice function for an existing DLA shape.

    Parameters
    ----------
    Lp : Lattice width
    dim : Dimension of DLA in range [2,3]
    anchored : Array of anchored particles

    Returns
    -------
    Lattice with binary value 1/0 where particle is anchored/nonexistent respectively
    '''
    if dim==2:
        lattice = np.zeros((Lp,Lp))
        for i in range(0,Lp):
            for j in range(0,Lp):
                if [i,j] in anchored:
                    lattice[j+1,-(i+1)]=1   
    elif dim==3:
        lattice = np.zeros((Lp,Lp,Lp))
        for i in range(0,Lp):
            for j in range(0,Lp):
                for k in range(0,Lp):
                    if [i,j,k] in anchored:
                        lattice[j+1,-(i+1),k+1]=1                   
    return(lattice)

def frac_dimen(scale,lattice,centre_point):
    """ 
    Creates arrays for fractal dimension
    using boxcounting method
    
    Scale = scaling array, lattice = lattice function
    with binary values, centre_point = where central
    particle is fixed """
    
    boxcount_array = []
    for i in range(len(scale)):
        boxcount = 0
        for j in range(int(centre_point-(scale[i]/2)),int(centre_point+(scale[i]/2))+1):
            for k in range(int(centre_point-(scale[i]/2)),int(centre_point+(scale[i]/2))+1):
                if lattice[j,k] == 1:
                    boxcount += 1
    boxcount_array.append(boxcount)
        
    return(boxcount_array[0])

def frac_dimen_3d(scale,lattice,centre_point):
    """ 
    Creates arrays for fractal dimension
    using boxcounting method
    
    Scale = scaling array, lattice = lattice function
    with binary values, centre_point = where central
    particle is fixed """
    
    boxcount_array = []
    for i in range(len(scale)):
        boxcount = 0
        for j in range(int(centre_point-(scale[i]/2)),int(centre_point+(scale[i]/2))+1):
            for k in range(int(centre_point-(scale[i]/2)),int(centre_point+(scale[i]/2))+1):
                for l in range(int(centre_point-(scale[i]/2)),int(centre_point+(scale[i]/2))+1):
                    if lattice[j,k,l] == 1:
                        boxcount += 1
        boxcount_array.append(boxcount)      
    return(boxcount_array)

def mass_ratio(anchored):
    """ 
    Creates arraysfor two fractal dimension
    using radius of gyration (AKA mass-ratio) method.
    
    Anchored = array of anchored particles"""
    anchoredx, anchoredy = list(zip(*anchored))
    CoMx = sum(anchoredx)/len(anchoredx)
    CoMy = sum(anchoredy)/len(anchoredy)
    R_g_array = []
    for i in range(1,len(anchored)):
        a=0
        for j in range(0,i+1):
            a += (anchoredx[j]-CoMx)**2+(anchoredy[j]-CoMy)**2
        b = a/i
        r_g = np.sqrt(b)
        R_g_array.append(r_g)
    return(R_g_array)

def mass_ratio_3d(anchored):
    """ 
    Creates arraysfor two fractal dimension
    using radius of gyration (AKA mass-ratio) method.
    
    Anchored = array of anchored particles"""
    anchoredx, anchoredy, anchoredz = list(zip(*anchored))
    CoMx = sum(anchoredx)/len(anchoredx)
    CoMy = sum(anchoredy)/len(anchoredy)
    CoMz = sum(anchoredz)/len(anchoredz)
    R_g_array = []
    for i in range(1,len(anchored)):
        a=0
        for j in range(0,i+1):
            a += (anchoredx[j]-CoMx)**2+(anchoredy[j]-CoMy)**2 + (anchoredz[j]-CoMz)**2
        b = a/i
        r_g = np.sqrt(b)
        R_g_array.append(r_g)
    return(R_g_array)

def f(x,a,b):
    """ basic linear function formula for curve fitting """
    return(a*x + b)