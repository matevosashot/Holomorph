import matplotlib


class HoverCursor(object):
    """A simple data cursor widget that displays the x,y location of a
    matplotlib artist when it is selected."""

    def __init__(self, figure, offsets=(-20, 20),
                 formatter=lambda ax, x, y: 'x: %0.2f\ny: %0.2f' % (x, y)):
        """Create the data cursor and connect it to the relevant figure.
        *figure* is the matplotlib figure. 
        *offsets* is a tuple of (x,y) offsets in points from the selected
            point to the displayed annotation box
        *formatter* is the format string to be used. Note: For compatibility
            with older versions of python, this uses the old-style (%) 
            formatting specification. 
        """
        self.format = formatter
        self.offsets = offsets
        self.figure = figure

        self.annotations = {}

        self.figure.canvas.mpl_connect('motion_notify_event', self)

    def get_anotation(self, axis):
        if axis not in self.annotations:
            self.annotations[axis] = self.annotate(axis)
        return self.annotations[axis]

    def set_invisible(self):
        for ax, anot in self.annotations.items():
            anot.set_visible(False)

    def annotate(self, ax, visible=False):
        """Draws the annotation box for the given axis *ax*."""
        annotation = ax.annotate(
            "", xy=(0, 0), ha='right',
            xytext=self.offsets, textcoords='offset points', va='bottom',
            bbox=dict(boxstyle='round,pad=0.2',
                      fc='yellow', alpha=0.5),
            # arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
        )
        annotation.set_visible(visible)
        return annotation

    def __call__(self, event):
        """Update and draw the annotation box for the pick event *event*."""
        # Rather than trying to interpolate, just display the clicked coords
        # This will only be called if it's within "tolerance", anyway.
        if event.inaxes is None:
            self.set_invisible()
            event.canvas.draw()
            return

        ax = event.inaxes
        x, y = event.xdata, event.ydata

        annotation = self.get_anotation(ax)
        annotation.xy = x, y
        annotation.set_text(self.format(ax, x, y))
        self.set_invisible()
        annotation.set_visible(True)
        event.canvas.draw()


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    plt.figure(figsize=(16, 8), dpi=200)
    plt.subplot(2, 1, 1)
    line1, = plt.plot(range(10), 'ro-')
    plt.subplot(2, 1, 2)
    line2, = plt.plot(range(10), 'bo-')

    HoverCursor(plt.gcf(), offsets=(-10, 10))

    plt.show()
