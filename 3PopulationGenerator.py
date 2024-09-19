# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 09:46:33 2024

@author: Alejandro
"""
from skimage.io import imread
import matplotlib.pyplot as plt
import numpy as np

def getChannelCoords(im, channel, cellwidth, strip=10):
    '''
    Extract coordinates from channels
    R=0, G=1, B=2
    and resizes them to desi
    '''
    im_H, im_W = np.shape(im[:,:,0])
    im_C = im[:,:,channel]
    ys_C, xs_C = np.where(im_C>0)
    # center around 0
    ys_C, xs_C = ys_C-int(im_H/2), xs_C-int(im_W/2)
    # strip and invert Y
    xs_C, ys_C = xs_C[::strip], -ys_C[::strip]
    # normalize to new size
    cellheight = (im_H/im_W)*cellwidth
    ys_C, xs_C = ys_C/im_H*cellheight*2, xs_C/im_W*cellwidth*2
    return (xs_C, ys_C)

#%%
def ParseCym(impath, outputname=None,strip=100, cellwidth=10, NT=(1,1,1), 
             LT=(1,1,1), WT=(0.1,0.1,0.1), simtime=(200,1000)):
    '''
    Creates a .cym file to pattern up to three populations
    of microtubuli based on an RGB image.
    The user can change:
        - number of tubes NT
        - length ot tubes LT
        - width of tubes WT
    always following the RGB convention (red, green, blue)
    for the order of the channels
    '''
    # Get params
    NT_R, NT_G, NT_B = NT
    LT_R, LT_G, LT_B = LT
    WT_R, WT_G, WT_B = WT
    sim_brown, sim_pattern = simtime
    
    # Load image and get coords
    im = imread(impath)
    coords_R = getChannelCoords(im, channel=0, cellwidth=10, strip=strip)
    coords_G = getChannelCoords(im, channel=1, cellwidth=10, strip=strip)
    coords_B = getChannelCoords(im, channel=2, cellwidth=10, strip=strip)
    
    # Load template and parse accordingly
    with open('./ThreePopulations_template.txt', 'r') as f:
        file = [l for l in f.readlines()]
        
    # replace cell size
    idx = file.index('\tlength = cellwidth, cellheight\n')
    file[idx] = f'\tlength = {cellwidth*1.4}, {cellwidth*1.4}\n'
    
    # replace tubuli width
    idx = file.index('    display = ( line_width=WT_R; color=red; )\n')
    file[idx] = f'    display = ( line_width={WT_R}; color=red; )\n'
    
    idx = file.index('    display = ( line_width=WT_G; color=green; )\n')
    file[idx] = f'    display = ( line_width={WT_G}; color=green; )\n'
    
    idx = file.index('    display = ( line_width=WT_B; color=blue; )\n')
    file[idx] = f'    display = ( line_width={WT_B}; color=blue; )\n'
    
    
    
    # replace amount of tubuli
    idx = file.index('new NT_R TUBE_R\n')
    file[idx] = f'new {NT_R} TUBE_R\n'
    
    idx = file.index('new NT_G TUBE_G\n')
    file[idx] = f'new {NT_G} TUBE_G\n'
    
    idx = file.index('new NT_B TUBE_B\n')
    file[idx] = f'new {NT_B} TUBE_B\n'
    
    # replace length of tubuli
    idx = file.index('    length = LT_R\n')
    file[idx] = f'    length = {LT_R}\n'
    
    idx = file.index('    length = LT_G\n')
    file[idx] = f'    length = {LT_G}\n'
    
    idx = file.index('    length = LT_B\n')
    file[idx] = f'    length = {LT_B}\n'

    # replace simulation times
    idx = file.index('    nb_steps = sim_brown\n')
    file[idx] = f'    nb_steps = {sim_brown}\n'
    
    idx = file.index('    nb_steps = sim_pattern\n')
    file[idx] = f'    nb_steps = {sim_pattern}\n'
      
    # Create file adding the coordinates of glue instances
    separator = file.index('% INSTANCES OF GLUE OBJECTS: skeletonized for parser\n')
    firsthalf = file[0:separator]
    secondhalf = file[separator+1:]
    
    with open(outputname, 'w') as f:
        # INITIALIZATION
        for line in firsthalf:
            f.write(line)
        # RED GLUE
        for x,y in zip(coords_R[0], coords_R[1]):
            f.write(f'new GRAFT_R ({x} {y})\n')
        # GREEN GLUE
        for x,y in zip(coords_G[0], coords_G[1]):
            f.write(f'new GRAFT_G ({x} {y})\n')
        # BLUE GLUE
        for x,y in zip(coords_B[0], coords_B[1]):
            f.write(f'new GRAFT_B ({x} {y})\n')
        # SECOND PART
        for line in secondhalf:
            f.write(line)
    print('Done')    
    
impath = 'C:/Users/Alejandro/Desktop/Hackathon2024/I2C_Heart.png'
ParseCym(impath, outputname='3h.cym', strip=30, NT=(20,20,20,))





#%% Test runs 
if __name__ == "__main__":
    impath = 'C:/Users/Alejandro/Desktop/Hackathon2024/I2C_Heart.png'
    im = imread(impath)
    coords_R = getChannelCoords(im, channel=0, cellwidth=10)
    coords_G = getChannelCoords(im, channel=1, cellwidth=10)
    coords_B = getChannelCoords(im, channel=2, cellwidth=10)
    
    plt.close('all')
    fig = plt.figure(figsize=(4,4))
    ax = fig.subplots(1)
    ax.scatter(coords_R[0], coords_R[1], c='red', s=0.1)
    ax.scatter(coords_G[0], coords_G[1], c='green', s=0.1)
    ax.scatter(coords_B[0], coords_B[1], c='blue', s=0.1)
#%%
for x,y in zip(coords_R[0], coords_R[1]):
    print(x,y)