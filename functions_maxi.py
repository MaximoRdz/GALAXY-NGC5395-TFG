import numpy as np
import matplotlib.pyplot as plt

from scipy import stats
from ipywidgets import interactive


#plt.style.use(['science', 'notebook'])

def my_plot(image, figsize = (6, 6), percentiles = (0.25, 99.75)):
    fig, ax = plt.subplots(figsize = figsize)
    show = ax.imshow(image, origin = 'lower',
                     vmin = np.nanpercentile(image, percentiles[0]),
                     vmax = np.nanpercentile(image, percentiles[1]),
                     cmap = 'inferno')
    plt.colorbar(show)
    plt.show() 
    
def my_plot_log(image):
    fig, ax = plt.subplots(figsize = (10, 7))
    show = ax.imshow(np.log10(image), origin = 'lower',
                     vmin = np.nanpercentile(np.log10(image), 15),
                     vmax = np.nanpercentile(np.log10(image), 99.9),
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

# TODO preinicializar el corte con los valores anteriores
class SkyInteractive():
    def __init__(self, data):
        self.data = data
        self.fig, self.axes = plt.subplots(1, len(data), figsize = (8, 4))
        self.widget = interactive(self.update, 
                                  x1 = (0,1023,1), 
                                  x2 = (0,1023,1), 
                                  y1 = (0,1023,1), 
                                  y2 = (0,1023,1))
        display(self.widget)
        
    def sky_cut(self, x1, x2, y1, y2):
        for i, ax in enumerate(self.axes):
            ax.clear()
            ax.imshow(self.data[i], origin = 'lower', 
                      vmin = np.nanpercentile(self.data[i], 50),
                      vmax = np.nanpercentile(self.data[i], 95),
                      cmap = 'inferno')

            ax.vlines([x1, x2], 0, 1023, color = 'w')
            ax.hlines([y1, y2], 0, 1023, color = 'w')
            ax.set_title('Frame: ' + str(i+1))
    
    def update(self, x1 = 200, x2 = 900, y1 = 200, y2 = 750):         
        self.sky_cut(x1, x2, y1, y2)
        self.fig.canvas.draw_idle()
        
    def get_cuts(self):
        return   self.widget.kwargs.values()