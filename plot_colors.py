from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

import numpy as np
from datacursor import HoverCursor


class ColorPlot:
    def __init__(self, f, xlim, ylim, step,
                 color_power=1, color_clip=None, figsize=(16, 8), dpi=200):
        """
        Plots "colorful" picture:
        - Color corresponds to argument of the function value evaluated at the
            corresponding point.
        - Brightness coresponds to the magnitude/absolute value of the function
            value evaluated at the corresponding point.
        Args:
            f (complex valued function): Function C -> C
            xlim (tuple): x-range of input domain
            ylim (tuple): y-range of input domain
            step (float): density of points.
            color_power (int, optional): scaler for the brightness. When function 
                has sharp maximum, this helps to see gradient of the brightness. 
                Defaults to 1.
            color_clip ([type], optional): clips function magnitude at that value. 
                When function have poles, this helps to avoid infinities. 
                Defaults to None.
            figsize (tuple, optional): Figure size. Defaults to (16, 8).
            dpi (int, optional): dpi for saving figure. Defaults to 200.
            save_path (str, optional): Path to save figure, if not none. 
                Defaults to None.

        Returns:
            (pyplot.figure): figure object
        """
        self.f = f
        self.xlim = xlim[0], xlim[1]+1e-8
        self.ylim = ylim[0], ylim[1]+1e-8
        self.step = step
        self.color_power, self.color_clip = color_power, color_clip
        self.figsize = figsize
        self.dpi = dpi

        self.Z, self.W = self._evaluate()
        self.fig, (self._ax_id, self._ax_f) = self._plot()
        self._hover_cursor = self._anotate()
        self.fig.tight_layout()

    def _evaluate(self):
        # make meshgrid
        d = np.mgrid[self.xlim[0]:self.xlim[1]:self.step,
                     self.ylim[0]:self.ylim[1]:self.step]
        plane = d[0] + d[1] * 1j
        Z = plane
        # evaluate
        W = self.f(Z)
        return Z, W

    def _plot(self):
        fig = plt.figure(figsize=self.figsize, dpi=150)
        ax_id = plt.subplot(121)
        plt.title("Input")
        plt.imshow(self._colors(self.Z.T, self.color_power, self.color_clip),
                   origin="lower")
        plt.xticks(*self._label_pos(self.xlim, self.step))
        plt.yticks(*self._label_pos(self.ylim, self.step))
        plt.grid(alpha=0.2)

        ax_f = plt.subplot(122)
        plt.title("Output")
        plt.imshow(self._colors(self.W.T, self.color_power, self.color_clip),
                   origin="lower")
        plt.xticks(*self._label_pos(self.xlim, self.step))
        plt.yticks(*self._label_pos(self.ylim, self.step))
        plt.grid(alpha=0.2)
        return fig, (ax_id, ax_f)

    def _anotate(self):
        def formatter(ax, x, y):
            x = self._inverse_transform(x, self.xlim, self.step)
            y = self._inverse_transform(y, self.ylim, self.step)
            z = x + 1j*y
            if ax == self._ax_id:
                w = z
            elif ax == self._ax_f:
                w = self.f(z)
            return self.formatter(z, w)

        return HoverCursor(self.fig, formatter=formatter)

    @staticmethod
    def _colors(W, color_power, color_clip):
        argW = (np.angle(W)) % (2*np.pi)
        # argW[np.isnan(argW)] = 0
        colors = cm.hsv(argW/(np.pi*2))
        absW = np.abs(W)

        # clip
        if color_clip is not None:
            absW = np.minimum(absW, color_clip)

        # rise to power
        colors[:, :, :3] *= (absW[:, :, np.newaxis] /
                             np.nanmax(absW))**(color_power)
        # colors[:, :, :3] *= np.tanh(absW[:, :, np.newaxis] / np.max(absW)*2)
        return colors

    @staticmethod
    def _transform(x, lim, step, dtype="int"):
        return ((-lim[0] + x) / step).astype(dtype)

    @staticmethod
    def _inverse_transform(x, lim, step, dtype="float"):
        return (x * step + lim[0]).astype(dtype)

    @staticmethod
    def _label_pos(lim, step):
        labels = np.arange(lim[0], lim[1]+1e-8, 1)
        positions = ColorPlot._transform(labels, lim, step, "int")
        return positions, labels

    @staticmethod
    def formatter(z, w):
        """
        Returns string, which will be in the annotation box.

        Args:
            z (complex): function input
            w (complex): function output

        Returns:
            str: annotation text
        """
        def complex_to_str(z):
            return f"{z:.2f}"[:-1] + "$i$"

        def complex_to_exp(z):
            rho = np.abs(z)
            phi = np.angle(z)
            sign, phi = "-+"[phi > 0], abs(phi/np.pi)
            return f"{rho:.2f}"+"$\\cdot e^{" + sign + f"{phi:.2f} i \pi " + "}$"
        return f"$z$:  {complex_to_str(z)}\n{complex_to_exp(z)}\n$f(z)$: {complex_to_str(w)}\n{complex_to_exp(w)}"

    def show(self, save_path=None):
        # for fullscreen
        self.fig.canvas.manager.full_screen_toggle()

        if save_path is not None:
            self.save(save_path)
        plt.show()

    def save(self, save_path, dpi=None):
        if dpi is None:
            dpi = self.dpi
        plt.savefig(save_path, dpi=dpi)
