# Holomorph

Tools for visualizing Complex functions.
See examples in look at `example_*.py` files.

## ColorPlot
This is very powerful method for visualising **complex valued** functions. And it becomes more powerful with interactive Matplotlib plot, where you can gat function value at any point:

<img src="https://github.com/ashmat98/Holomorph/blob/master/output/screenshot.jpg?raw=true">

On the left axis
 is ploted input values to the function, which is same as ouotput of _identity_ function.
On the right axis is ploted function values.
On the yelow box you see function input and output at cursor point.
- Color corresponds to argument of the function value evaluated at the corresponding point: _Red_ for $0$, _Cyan_ for $\pi$, etc.
- Brightness coresponds to the magnitude/absolute value of the function value evaluated at the corresponding point: _Black_ for 0, _Brighter_ - higher absolute value.
```python
# see `example_holomorphic_function.py`
from plot_colors import ColorPlot

ColorPlot(lambda z: 0.5*(z +  1/z), 
	(-2, 2), (-2, 2), 0.005,
	color_power=(1/4), color_clip=4).show()
# this will open interactive window, with _annotation_ feature
```
## GridTransform
This is another method for visualizig complex valued (of any 2d-to-2d function), by viewing trajectory of each point of the input domain during transformation.
This transformation is **homeomorphism** between $h(z, t=0)=z$ and $h(z, t=1)=f(z)$ given by:
$$ h(z, t) = z (1-t) + f(z) t \quad \quad \text{for} ~~~ 0 \le t \le 1$$
<p align="center">
 <img src="https://github.com/ashmat98/Holomorph/blob/master/output/sample_function.gif?raw=true"  class="center"> </p>
 (this is low resolution gif sample image)
By default, input 2d-plane grid-lines are added to transformable objects (or paths). In the example above, 3 circular paths are also added to the transformable objects.
this is the sample code:

```python
# see `example_holomorphic_function.py`
from grid_transform import GridTransformer
import numpy as np

gt = GridTransformer(lambda z: 0.5*(z +  1/z),
	(-4, 4), (-4, 4), 0.1, 0.01,
	plt_xlim=(-2., 2.), plt_ylim=(-2., 2.))

# add some curves
gt.add_curve(np.exp(np.pi * 2j * np.linspace(0,1,200, endpoint=True)), lw=4)
gt.add_curve(0.5*np.exp(np.pi * 2j * np.linspace(0,1,200, endpoint=True)), lw=4)
gt.add_curve( 1j+0.1*np.exp(np.pi * 2j * np.linspace(0,1,200, endpoint=True)), lw=2)

gt.transform("output/sample_function.mp4", seconds=16, fps=60,
	figsize=(10, 10), dpi=200, plus_reverse=True)
```

Note that any 2d-to-2d function can be made into complex-valued, not necessarly holomorphic function. For example, we can visualize linear transformations as well.

```python
# see `example_linear_transformation.py`
def  linear_function(A):
	A = np.array(A)
	def  f(z):
		x, y = np.real(z), np.imag(z)
		result = np.dot(A, np.stack([x,y], axis=0))
		x, y = result
		return x + y * 1j
	return f
```