from matplotlib import pyplot as plt
import os
from matplotlib.animation import FuncAnimation, FFMpegWriter
import numpy as np
from tqdm import tqdm


class GridTransformer:
    def __init__(self, f,  xlim, ylim, grid_separation, step=0.01, 
        plt_xlim=None, plt_ylim=None):
        """
        Class for making 2d space transformations by given function.
        By default grid lines are added. You can additionally add curves
        by calling `add_curve` with coordinates and style.
        
        
        Args:
            f (complex function): function that maps complex number to complex number
            xlim (tuple): limits for input space, x coordinate
            ylim (tuple): limits for input space, y coordinate
            grid_separation (float): grid lines separation for minor grid.
                major grid lines have integer coordinates.
            step (float, optional): point density on curves. Defaults to 0.01.
            plt_xlim (tuple, optional): limits for output space, x coordinate. Area 
                shown by matplotlib. Defaults to None, i.e. maximum visible area, 
                bad idea for infinities.
            plt_ylim (tuple, optional): limits for output space, x coordinate.
                Defaults to None.
        """
        self.f = f
        self.xlim = xlim[0], xlim[1]+1e-8
        self.ylim = ylim[0], ylim[1]+1e-8
        self.sep = grid_separation
        self.step = step
        self.curves = []
        
        self.add_grid_to_curves()
        self.plt_xlim, self.plt_ylim = self._init_limits(plt_xlim, plt_ylim)
        
    
    def add_curve(self, z, fz=None, **style):
        """
        Add curve with points in input and output space.
        
        Args:
            z (list, ndarray): Complex points in input space.
            fz (list, ndarray, optional):  Complex points in output space space. 
                Defaults to None, i.e. will be coputed by function.
        """
        z = np.array(z)
        if fz is None:
            fz = self.f(z)
        self.curves.append(((z, fz), style))
        
    def add_grid_to_curves(self):
        """
        Add grid lines to curves.
        """
        for x in np.arange(self.xlim[0], self.xlim[1], self.sep):        
            x = round(x, 4)
            color, alpha, lw = "blue", 0.2, 1 
            if int(x) == x:
                alpha = 1
            if x == 0:
                color = "black"
                lw=2
            self.add_curve(self._get_x_axis(x, self.ylim, self.step),
                color=color, lw=lw, alpha=alpha)
        for y in np.arange(self.ylim[0], self.ylim[1], self.sep):
            y = round(y, 4)
            color, alpha, lw = "red", 0.2, 1        
            if int(y) == y:
                alpha = 1
            if y == 0:
                color = "black"
                lw=2
            self.add_curve(self._get_y_axis(y, self.xlim, self.step),
                color=color, lw=lw, alpha=alpha)
    
    @staticmethod
    def transition(z, fz, t):
        """
        Smooth transition from identity function to given function.
        t=0 -> identity ( i.e. x )
        t=1 -> self.f   ( i.e. fz )
        """
        return z * (1-t) + fz*t
        
    def plot_trasformed(self,t=1,save_path=None, **fig_kwargs):
        """
        Plot curves on a figure.
        
        Args:
            t (int, optional): Plot at intermediate point. Defaults to 1.
            save_path (str, optional): Save figure if not None.
        Returns:
            matplotlib figure object
        """
        fig = plt.figure(**fig_kwargs)
        plt.xlim(self.plt_xlim)
        plt.ylim(self.plt_ylim)
        plt.gca().set_aspect("equal")
        for (z, fz), style in self.curves:
            p = self.transition(z, fz, t)
            plt.plot(np.real(p), np.imag(p), **style)
        if save_path is not None:
            if os.path.splitext(save_path)[1] != ".png":
                save_path += '.png'
            plt.savefig(save_path)
            print(f"Figure saved in {save_path}.")
        return fig
    
    @staticmethod    
    def _get_x_axis(x, lim, step):
        return x + np.arange(lim[0], lim[1], step) * 1j
    
    @staticmethod    
    def _get_y_axis(y, lim, step):
        return np.arange(lim[0], lim[1], step) + y*1j
        
    def _init_limits(self, xlim=None, ylim=None):
        """
        Calculates unboundedlimits for output space.
        """
        # First set up the figure, the axis, and the plot element we want to animate
        margin = 0.05
        if xlim is None:
            xmin = np.min([np.min(np.real(p)) for p,_ in self.curves])
            xmax = np.max([np.max(np.real(p)) for p,_ in self.curves])
            dx = (xmax-xmin)*margin
            xlim = (xmin-dx, xmax+dx)
        if ylim is None:
            ymin = np.min([np.min(np.imag(p)) for p,_ in self.curves])
            ymax = np.max([np.max(np.imag(p)) for p,_ in self.curves])
            dy = (ymax-ymin)*margin
            ylim = (ymin-dy, ymax+dy)
        return xlim, ylim
    
    @staticmethod
    def get_frame_times(seconds, fps, plus_reverse):
        """
        Returns list of numbers, containing transformation stage 
        (i.e. t in self.transition) for each frame
        
        Args:
            seconds (float): seconds for animation
            fps (int): fps of the writes
            plus_reverse (bool): reverse played animation
        Returns:
            list of floats
        """
        frames = []
        frames.append(np.linspace(0, 1,int(seconds * fps), endpoint=True))
        frames.append(np.ones((int(fps*0.5))))
        
        if plus_reverse:
            frames.append(np.linspace(1, 0,int(seconds * fps), endpoint=True))
            frames.append(np.zeros((int(fps*0.5))))
        frames = np.concatenate(frames, axis=0)
        return frames
        
    def transform(self, fname, seconds, plus_reverse=False, fps=25, **fig_kwargs):
        """
        Creates animation and saves in mp4 video file.

        Args:
            fname (str): File name for saving.
            seconds (float): Transformation duration
            plus_reverse (bool, optional): append reverse animation 
                (backward transformation). Defaults to False.
            fps (int, optional): Frames per second. Defaults to 25.
        
        Returns:
            Matplotlib animation abject.
        """
        n_frames = fps * seconds

        fig = plt.figure(**fig_kwargs)
        ax = plt.axes(xlim=self.plt_xlim, ylim=self.plt_ylim, aspect="equal")
        
        def init_plot():
            lines = []
            for (z, fz), style in self.curves:
                line, = ax.plot(np.real(z), np.imag(z), **style)
                lines.append(line)
            return lines
        lines = init_plot()
        
        frames = self.get_frame_times(seconds, fps, plus_reverse)
        progress_bar = tqdm(range(len(frames)+1))

        def animate(t):
            progress_bar.update(1)
            t = 1 - (t-1)**2
            for line, data in zip(lines, self.curves):
                (z, fz), _ = data
                p = self.transition(z, fz, t)
                line.set_data(np.real(p), np.imag(p))
            return lines

        # call the animator.  blit=True means only re-draw the parts that have changed.
        anim = FuncAnimation(fig, animate,
                             frames=frames, interval=25, blit=True)
        FFwriter = FFMpegWriter(fps=fps)
        if os.path.splitext(fname)[1] != ".mp4":
            fname += ".mp4"
        anim.save(fname, writer=FFwriter)
        print(f"\nAnimation saved in {fname}.")
        return anim

        