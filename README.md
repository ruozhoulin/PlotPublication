# plot-publication
This repo could automatically adjust **figure/subfigure size** to fit the page that you want to insert the figure. In this way, the figure is presented as intended without being stretched and squeezed.

![](figures\Picture1.png)

# Why do we need this package?

When I write a manuscript, I always have to spend many time and effort adjusting the figure size. This is because the figure is often stretched or squeezed after being inserted into a page, caused by inconsistent size (usually the width) between the figure and the page. One direct negative effect is that the font size of labels, ticks, and legends is changed, as shown in the following figure. Although manually setting the figure size according to the page size can solve this problem, this work is laborious and the verbose code that adjusts figure size hampers the readability. That's why I decided to develop this package.

![](figures\Picture2.svg)

# Getting Started

The easiest way to use this package is to put `plot_publication.py` in your working directory and then import it: 

```python
from plot_publication import *
```

Note:

* `plot_publication` requires `matplotlib`.
* Please use the provided method to import this package. Other import methods like `import plot_publication` could result in errors in the font family.

# Using this package

After importing `plot_publication`, you can create a figure with appropriate size by:

```python
# Create a figure with 6 subplots that fits an A4 page.
Fig = FigurePublication(3, 2)
fig, ax = Fig.fig, Fig.ax
# the following code can be identical to what you do with matplotlib
ax[0][0].plot(x1, y1, label='figure (1,1)')
```

It should be noted that `FigurePublication()` create a figure and set its size according to **an A4 page with a normal margin in default**. If you want to insert your figure into a page with a different page size and margin size, please input these values as parameters.

# Examples

Please refer to `examples.ipynb`.