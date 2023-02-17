import numpy as np
import matplotlib.pyplot as plt

from scipy import stats
from ipywidgets import interactive


plt.style.use(['science', 'notebook'])

def my_plot(image):
    plt.style.use('default')
    fig, ax = plt.subplots(figsize = (6, 6))
    show = ax.imshow(image, origin = 'lower',
                     vmin = np.nanpercentile(image, 5),
                     vmax = np.nanpercentile(image, 95),
                     cmap = 'inferno')
    plt.colorbar(show)
    plt.show() 

def cut_master_frames(master_frame, x1, y1, shape): 
    x1 = int(x1)
    y1 = int(y1)
    if master_frame.shape[0] != shape[0]:
        master_frame = master_frame[x1:x1+shape[0], :]
    else:
        pass
    if master_frame.shape[1] != shape[1]:
        master_frame = master_frame[:, y1:y1+shape[0]]
    else:
        pass
    return master_frame

#row1, row2, comumn1, column2 = 0, 0, 0, 0
def sky_substraction(image):
    #if row2 == 0: row2 = image[0].shape[0]-1; column2 = row2;
    def interactive_plot(row1, row2, column1, column2):
        fig, axes = plt.subplots(1, 2, figsize = (8, 4))
        for i, ax in enumerate(axes):
            show = ax.imshow(image[i], origin = 'lower',
                             vmin = np.nanpercentile(image[i], 50),
                             vmax = np.nanpercentile(image[i], 95),
                             cmap = 'inferno')
            ax.axvline(x = column1, color = 'white')
            ax.axvline(x = column2, color = 'white')
            
            ax.axhline(y = row1, color = 'white')
            ax.axhline(y = row2, color = 'white')    
        
            plt.colorbar(show, ax = ax)
        #plt.show() 
    
    return interactive(interactive_plot, 
                        row1 = (0, image[0].shape[0]-1, 1),
                        row2 = (0, image[0].shape[0]-1, 1), 
                        column1 = (0, image[0].shape[0]-1, 1), 
                        column2 = (0, image[0].shape[0]-1, 1))

def sky_squares_median(row1, row2, column1, column2, image):
    # three bottom rectangles
    sky1 = stats.mode(image[0:row1, 0:column1].flatten())[0]
    sky2 = stats.mode(image[0:row1, column1:column2].flatten())[0]  
    sky3 = stats.mode(image[0:row1, column2:].flatten())[0]
    # two middle rectangles
    sky4 = stats.mode(image[row1:row2, 0:column1].flatten())[0]
    sky5 = stats.mode(image[row1:row2, column2:].flatten())[0]        
    # three top rectangles
    sky6 = stats.mode(image[row2:, 0:column1].flatten())[0]
    sky7 = stats.mode(image[row2:, column1:column2].flatten())[0] 
    sky8 = stats.mode(image[row2:, column2:].flatten())[0]
    
    sky_modes = np.concatenate([sky1, sky2, sky3, sky4, sky6, sky7, sky8])
    sky = np.nanmedian(sky_modes)
    return sky