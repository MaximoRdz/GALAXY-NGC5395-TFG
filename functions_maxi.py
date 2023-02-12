import numpy as np
import matplotlib.pyplot as plt

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