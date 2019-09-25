from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

import numpy as np
from datacursor import HoverCursor


def plot(f, xlim, ylim, step, 
    color_power=1, color_clip=None, figsize=(16, 8), dpi=200, save_path=None):
    xlim = xlim[0], xlim[1]+1e-8
    ylim = ylim[0], ylim[1]+1e-8
    
    # make meshgrid
    d = np.mgrid[xlim[0]:xlim[1]:step, ylim[0]:ylim[1]:step]
    plane = d[0] + d[1] * 1j
    Z = plane
    # evaluate
    W = f(Z)

    def colors(W, color_power):
        argW = (np.angle(W)) % (2*np.pi)
        # argW[np.isnan(argW)] = 0
        colors = cm.hsv(argW/(np.pi*2))

        absW = np.abs(W)
        if color_clip is not None:
            absW = np.minimum(absW, color_clip)
      
        colors[:, :, :3] *= (absW[:, :, np.newaxis] / np.nanmax(absW))**(color_power)
                    
        # colors[:, :, :3] *= np.tanh(absW[:, :, np.newaxis] / np.max(absW)*2)
        return colors
    
    def transform(x, lim, step, dtype="int"):
        return ((-lim[0] + x) / step).astype(dtype)
    def inverse_transform(x, lim, step, dtype="float"):
        return (x * step + lim[0]).astype(dtype)
    
    def label_pos(lim, step):
        labels = np.arange(lim[0], lim[1]+1e-8, 1)
        positions = transform(labels, lim, step, "int")
        return positions, labels

    
    
    plt.figure(figsize=figsize, dpi=150)
    ax_id = plt.subplot(121)
    plt.title("Input")
    plt.imshow(colors(Z.T, color_power), origin="lower")
    plt.xticks(*label_pos(xlim, step))
    plt.yticks(*label_pos(ylim, step))
    plt.grid(alpha=0.2)
    
    ax_f = plt.subplot(122)
    plt.title("Output")   
    plt.imshow(colors(W.T, color_power), origin="lower")
    plt.xticks(*label_pos(xlim, step))
    plt.yticks(*label_pos(ylim, step))
    plt.grid(alpha=0.2)

    def formatter(ax, x, y):
        x = inverse_transform(x, xlim, step)
        y = inverse_transform(y, ylim, step)
        if ax == ax_id:
            z = x + 1j*y
        elif ax == ax_f:
            z = f(x + 1j*y)
        ro = np.abs(z)
        phi = ((np.angle(z)) % (2*np.pi)) / np.pi
        return 'x: %0.2f\ny: %0.2f\n$\\rho$: %0.2f\n$\\phi$: %0.2f$\\pi$' %(x, y, ro, phi)
    
    HoverCursor(plt.gcf(), formatter=formatter)
    if save_path is not None:
        plt.savefig(save_path, dpi=dpi)
    return plt.gcf()
