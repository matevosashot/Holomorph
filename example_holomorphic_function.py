from matplotlib import pyplot as plt
import numpy as np

from plot_colors import ColorPlot
from grid_transform import GridTransformer

def f(z):
    return 0.5*(z + 1/z)

# ColorPlot(f, (-2, 2), (-2, 2), 0.005, 
#     color_power=(1/4), color_clip=4).show("output/sample_function_colors.png")


gt = GridTransformer(f, (-4, 4), (-4, 4), 0.1, 0.01,
                     plt_xlim=(-2., 2.), plt_ylim=(-2., 2.))

#add some curves to the plane
gt.add_curve(np.exp(np.pi * 2j * np.linspace(0,1,200, endpoint=True)), lw=4)
gt.add_curve(0.5*np.exp(np.pi * 2j * np.linspace(0,1,200, endpoint=True)), lw=4)
gt.add_curve( 1j+0.1*np.exp(np.pi * 2j * np.linspace(0,1,200, endpoint=True)), lw=2)

# snapshots during transformation
gt.plot_trasformed(t=0, save_path="output/sample_function(t=0).png", figsize=(10, 10), dpi=100)
gt.plot_trasformed(t=0.3, save_path="output/sample_function(t=0.3).png", figsize=(10, 10), dpi=100)
gt.plot_trasformed(t=1, save_path="output/sample_function(t=1).png", figsize=(10, 10), dpi=100)

gt.transform("output/sample_function.mp4", seconds=16, fps=60, 
             figsize=(10, 10), dpi=200, plus_reverse=True)