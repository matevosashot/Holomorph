import numpy as np 
from grid_transform import GridTransformer, plt

def linear_function(A):
    """
    A is 2x2 matrix for linear transformation.
    Returns corresponding complex function (not 
    necessarily holomorphic).
    """
    A = np.array(A)
    assert A.shape == (2,2)
    def f(z):
        x, y = np.real(z), np.imag(z)
        result = np.dot(A, np.stack([x,y], axis=0))
        x, y = result
        return x + y * 1j
    return f

f = linear_function([[2,2],
                     [0,2]])

gt = GridTransformer(f, (-4, 4), (-4, 4), 0.1, 0.01,
                     plt_xlim=(-4., 4.), plt_ylim=(-4., 4.)
                     )

gt.add_curve(np.exp(np.pi * 2j * np.linspace(0,1,200, endpoint=True)), lw=4)
gt.add_curve(0.5*np.exp(np.pi * 2j * np.linspace(0,1,200, endpoint=True)), lw=4)
gt.plot_trasformed(t=0, save_path="output/sheer_transformation(t=0).png", figsize=(10, 10), dpi=100)
gt.plot_trasformed(t=0.3, save_path="output/sheer_transformation(t=0.3).png", figsize=(10, 10), dpi=100)
gt.plot_trasformed(t=1, save_path="output/sheer_transformation(t=1).png", figsize=(10, 10), dpi=100)
gt.transform("output/sheer_transformation.mp4", seconds=8, fps=30, 
             figsize=(10, 10), dpi=100, plus_reverse=True)