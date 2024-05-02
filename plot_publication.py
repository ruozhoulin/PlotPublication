# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  : Plot for academic publication
# @Date     : 2021.12.30
# @Author   : Ruozhou Lin
# @Email    : ruozhoulin@zju.edu.cn

    Useful parameters, settings and functions to create high
quality figures for publication
-------------------------------------------------
"""
import numpy as np
from numpy.typing import NDArray

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, MultipleLocator, AutoMinorLocator
import matplotlib.figure
from matplotlib.transforms import ScaledTranslation

# * ====================================================================
# * set default properties
rc = matplotlib.rcParams

# * Set font's properties.
# ! You must use from `PLOT_academic import *` to enable font size setting
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

# set default font
font = {"family": "Times New Roman", "weight": "normal", "size": SMALL_SIZE}  # bold
matplotlib.rc("font", **font)

# set font for other objects
rc["axes.titlesize"] = MEDIUM_SIZE  # title of each sub-figure
rc["axes.labelsize"] = MEDIUM_SIZE
rc["xtick.labelsize"] = SMALL_SIZE
rc["ytick.labelsize"] = SMALL_SIZE
rc["legend.fontsize"] = SMALL_SIZE
rc["figure.titlesize"] = BIGGER_SIZE  # title of the whole figure

# set latex font
rc["mathtext.fontset"] = "cm"
rc["mathtext.rm"] = "serif"

# * Set ...
rc["xtick.minor.width"] = 0.4
# * ====================================================================


class UnitTex:
    # https://en.wikipedia.org/wiki/International_System_of_Units

    length_options = ("mm", "cm", "m", "km")
    time_options = ("s", "min", "h", "d")
    mass_options = ("mg", "g", "kg")

    @classmethod
    def time(cls, time: str) -> str:
        assert time in cls.time_options

        unit_time = "%s" % time
        return "$\mathrm{%s}$" % (unit_time)

    @classmethod
    def length(cls, length: str) -> str:
        assert length in cls.length_options

        unit_length = "%s" % length
        return "$\mathrm{%s}$" % (unit_length)

    @classmethod
    def area(cls, length: str) -> str:
        assert length in cls.length_options

        unit_length = "%s" % length
        return "$\mathrm{%s^{2}}$" % (unit_length)

    @classmethod
    def velocity(cls, length: str, time: str) -> str:
        assert length in cls.length_options
        assert time in cls.time_options

        unit_length = "%s" % length
        unit_time = "%s" % time
        return "$\mathrm{%s/%s}$" % (unit_length, unit_time)

    @classmethod
    def discharge(cls, length: str, time: str) -> str:
        assert length in cls.length_options
        assert time in cls.time_options

        unit_length = "%s" % length
        unit_time = "%s" % time
        return "$\mathrm{%s^{3}/%s}$" % (unit_length, unit_time)

    @classmethod
    def show_options(cls) -> None:
        print("Length:\t", cls.length_options)
        print("Time:\t", cls.time_options)
        print("Mass:\t", cls.mass_options)


class Page:
    """This class define the size of the page/slide that you want to insert your figure.
    Please set the `height`, `width`, and `margin` of the page/slide in inch.

    If you are not familiar with these term, please refer to Word -> Layout -> Page Setup
    section for more information.
    """

    def __init__(self, height, width, margin=(0, 0, 0, 0)) -> None:
        # Define size of the paper in inch
        self.__height = height  # inch
        self.__width = width  # inch
        self.__margin = margin  # (top, bottum, left, right)
        self.validate()  # Check if the above parameters are reasonable.

    def validate(self):
        """Check if page parameters are reasonable, i.e., the margin should be
        positive and should not be larger than the page.
        """
        assert self.__height > 0 and self.__width > 0
        for value in self.margin:
            assert value >= 0
        assert self.margin[0] + self.margin[1] < self.__height
        assert self.margin[2] + self.margin[3] < self.__width

    @property
    def page_size(self):
        return self.__height, self.__width

    @page_size.setter
    def page_size(self, height, width):
        self.__height = height
        self.__width = width
        self.validate()

    @property
    def body_size(self):
        height = self.__height - self.__margin[0] - self.__margin[1]
        width = self.__width - self.__margin[2] - self.__margin[3]
        return height, width

    @property
    def margin(self):
        return self.__margin

    @margin.setter
    def margin(self, values):
        self.__margin = values
        self.validate()  # Check if the above parameters are reasonable.

    def print_page_setting(self):
        print("The size of the page is %.2f * %.2f." % (self.__height, self.__width))
        print(
            """The margin is:
    Top:    %.2f
    Bottom: %.2f
    Left:   %.2f
    Right:  %.2f"""
            % self.__margin
        )

    # set space between subplot
    def set_width_space(self, v=0.25):
        plt.rcParams["figure.subplot.wspace"] = v

    def set_height_space(self, v=0.3):
        plt.rcParams["figure.subplot.hspace"] = v


class PageA4(Page):
    """Create a subclass of `Page` that has a size of A4 and use default margin setting in Word."""

    def __init__(self, height=11.69, width=8.27, margin=(1, 1, 1.25, 1.25)) -> None:
        super().__init__(height, width, margin)

    def print_page_setting(self):
        print("Page A4:")
        super().print_page_setting()


class PageLetter(Page):
    """Create a subclass of `Page` that has a size of Letter and use default margin setting in Word."""

    def __init__(self, height=11, width=8.5, margin=(1, 1, 1.25, 1.25)) -> None:
        super().__init__(height, width, margin)

    def print_page_setting(self):
        print("Page Letter:")
        super().print_page_setting()


class PageSlide(Page):
    """Create a subclass of `Page` that has a size of slide and use default setting in PowerPoint."""

    def __init__(self, height=0, width=0, aspectRatio="4:3", margin=(0, 0, 0, 0)) -> None:
        if aspectRatio == "4:3":
            height, width = 7.5, 10
        elif aspectRatio == "16:9":
            height, width = 7.5, 13.33
        else:
            pass
        super().__init__(height, width, margin)

    def print_page_setting(self):
        print("Page for slides:")
        super().print_page_setting()


class FigurePublication:

    # * only need to define width because height will be automatically adjusted by `ax.set_box_aspect(1)`
    dimension_scale = (
        ((0.6, 0.30), (1.0, 1.00), (1.0, 1.00), (1.0, 1.00)),
        ((1.0, 0.55), (1.0, 0.55), (1.0, 0.55), (1.0, 0.55)),
        # ((1.0, 1.00), (1.0, 1.00), (1.0, 1.00), (1.0, 1.00)),
        ((1.0, 1.00), (1.0, 1.00), (1.0, 1.00), (1.0, 1.00)),
        ((1.0, 1.00), (1.0, 1.00), (1.0, 1.00), (1.0, 1.00)),
    )

    def __init__(
        self,
        row_count,
        col_count,
        page=PageA4(),
        rate_x=None,
        rate_y=None,
        is_constrained_layout_enabled=True,  # if this is enable, fig.tight_layout() is not needed.
    ) -> None:
        self.page: Page = page
        self.__row_count = row_count
        self.__col_count = col_count
        self.fig: matplotlib.figure.Figure
        self.ax: list[plt.Axes]  # it should be an numpy array
        self.fig, self.ax = plt.subplots(
            row_count, col_count, constrained_layout=is_constrained_layout_enabled
        )

        self.set_figure_size(rate_x, rate_y)

        # make sure the height of each sub-figure equals the width
        # note that box aspect is different from axes aspect
        # former is for spines' shape but the latter is for axis value.
        if col_count > 1:
            for ax in self.ax.flatten():  # convert to 1d array
                ax.set_box_aspect(1)

    def get_proper_fig_size(self, rate_x=None, rate_y=None):
        """Automatically set size of the figure according to the page size and figure content.
        You can also do this manually by setting `xrate` and `yrate`.
        """
        # compute rate for x and y
        if self.__row_count <= 4 and self.__col_count <= 4:
            rate_x1, rate_y1 = self.dimension_scale[self.__row_count - 1][self.__col_count - 1]
        else:
            rate_x1, rate_y1 = 1.0, 1.0
        # Check these parameters are set manully.
        if rate_x is not None:
            rate_x1 = rate_x
        if rate_y is not None:
            rate_y1 = rate_y

        # compute figure size
        page_height, page_width = self.page.body_size
        fig_width = page_width * rate_x1
        fig_height = page_height * rate_y1
        return fig_width, fig_height

    def set_figure_size(self, rate_x=None, rate_y=None):
        width, height = self.get_proper_fig_size(rate_x, rate_y)
        self.fig.set_size_inches(width, height)

    def save(self, savename: str, bbox_inches="tight", dpi=300, **kwargs):
        """Save the figure in .svg format."""
        # 300 is usually minimum requirement for high resolution images, 600 is better

        # format of save name should be "directory/figure.svg"
        format = savename.split(".")[-1]
        assert format == "svg" or format == "png"

        # ! Warning: only the given portion of the figure is saved
        # ! bbox_inches will change size of the figure when saving
        self.fig.savefig(savename, bbox_inches=bbox_inches, dpi=dpi, **kwargs)
        # self.fig.savefig(savename, dpi=dpi)

    def change_page(self, newpage=PageSlide()):
        # modify paper size, such as from A4 to a slide in 16:9
        self.page = newpage
        self.set_figure_size()

    def stretch_figure_height(self, ratio: float) -> None:
        width, height = self.fig.get_size_inches()
        self.fig.set_size_inches(width, height * ratio)

    def stretch_figure_width(self, ratio: float) -> None:
        # should be rarely used, only for 1x1 figure.
        width, height = self.fig.get_size_inches()
        self.fig.set_size_inches(width * ratio, height)

    def corner_annotate(
        self,
        ax: plt.Axes,
        content: str,
        pad: float = 0.05,  # unit: inch
        horizontal: str = "left",
        vertical: str = "top",
        **kwargs,
    ) -> None:
        """_summary_

        Args:
            ax (plt.Axes): _description_
            content (str): _description_
            pad (float, optional): _description_. Defaults to 0.05.
            vertical (str, optional): _description_. Defaults to "top".

        Raises:
            ValueError: _description_
        """

        if horizontal == "left" and vertical == "top":
            dx = pad
            dy = -dx
        else:
            raise ValueError("Not finished yet.")

        # * create the transformer to properly place the annotate
        # * https://matplotlib.org/stable/users/explain/artists/transforms_tutorial.html
        # transformer1 will transform the translation (dx, dy) from unit in inch to pixel
        # i.e., from **"figure-inches" coordinate system** from to **display coordinate system**.
        transformer1 = ScaledTranslation(dx, dy, self.fig.dpi_scale_trans)

        # transformer2 firstly applies `ax.transAxes`` to transform a coordinate from **axes coordinate system**
        # to **display coordinate system**, then apply transformer1.
        # Note the unit of the display coordinate is usually **pixel**, but depends on the backend.
        transformer2 = ax.transAxes + transformer1

        # * add annotate to the sub-figure with the transformer
        ax.text(
            0,
            1,
            content,
            size=MEDIUM_SIZE,  # font size
            # weight="bold",
            ha="left",  # horizontal alignment
            va="top",  # vertical alignment
            transform=transformer2,
            **kwargs,
        )


def get_default_color(type="rgb") -> list:
    # [u'#1f77b4', u'#ff7f0e', u'#2ca02c', u'#d62728', u'#9467bd',
    # u'#8c564b', u'#e377c2', u'#7f7f7f', u'#bcbd22', u'#17becf']
    lst = matplotlib.rcParams["axes.prop_cycle"].by_key()["color"]  # hex
    if type == "rgb":
        # convert hex to rgb that ranges from 0 to 1
        lst = [list(int(h.lstrip("#")[i : i + 2], 16) / 256 for i in (0, 2, 4)) for h in lst]
    return lst


def enable_minor_locator(ax: plt.Axes, n=5):
    ax.xaxis.set_minor_locator(AutoMinorLocator(n))
    ax.yaxis.set_minor_locator(AutoMinorLocator(n))


def enable_axes_legend(ax: plt.Axes, **kwargs):
    ax.legend(frameon=False, **kwargs)  # remove legend background


def enable_figure_legend(
    fig, lines: list, labels: list[str], height_ratio=1.0, placeholder_size=0.3, label_per_row=8, **kwargs
) -> None:
    # add a legend for all plot
    # https://stackoverflow.com/questions/27016904/matplotlib-legends-in-subplot
    # https://matplotlib.org/stable/gallery/text_labels_and_annotations/legend_demo.html

    # reserve space for legend by creating an empty figure title
    # Note that for .py, legend will not be shown inside the figure if anchor > 1,
    # but Jupyter will show it by making figure larger.
    font_size = placeholder_size * 70  # convert from inch to font size
    fig.suptitle(" ", alpha=0.0, size=font_size)

    # add the legend
    fig.legend(
        lines,
        labels,
        loc="upper center",
        frameon=False,
        # distance to center of the text box (both horizontal and vertical)
        bbox_to_anchor=(0.5, height_ratio),
        # bbox_transform=fig.transFigure,
        ncol=label_per_row,
        fontsize=MEDIUM_SIZE,
        **kwargs,
    )


def set_tick_number_x(tick_number: int, ax: plt.Axes) -> None:
    loc = MaxNLocator(tick_number)
    ax.xaxis.set_major_locator(loc)


def set_tick_number_y(tick_number: int, ax: plt.Axes) -> None:
    loc = MaxNLocator(tick_number)
    ax.yaxis.set_major_locator(loc)


def more_space(ax: plt.Axes, direction: str, ratio: float = 0.1) -> None:
    # leave more space at certain direction of an ax, usually for add a figure index or legend
    assert direction in ["left", "right", "top", "bottom"]

    xmin, xmax = ax.get_xlim()
    xRange = xmax - xmin
    dx = ratio * xRange
    ymin, ymax = ax.get_ylim()
    yRange = ymax - ymin
    dy = ratio * yRange

    if direction == "left":
        ax.set_xlim(xmin - dx, xmax)
    elif direction == "right":
        ax.set_xlim(xmin, xmax + dx)
    elif direction == "top":
        ax.set_ylim(ymin, ymax + dy)
    elif direction == "bottom":
        ax.set_ylim(ymin - dy, ymax)
    else:
        raise ValueError()


def set_equal_ylim(ax_in_row: list[plt.Axes]) -> None:
    """Set a row of sub-figures with same y limit by sharing their y-axis.
    Usually for hiding shared y-axis when plotting 3x3, 4x4 figure.

    Note: here we assume the left most sub-figure is the main sub-figure, of which y axis is reserved.
    Other sub-figures are attached to the main sub-figures and their y axis are hidden.

    Args:
        ax_in_row (list[plt.Axes]): a row of sub-figures in a matrix of sub-figures.
    """

    ax_main = ax_in_row[0]
    for ax in ax_in_row[1:]:
        ax.sharey(ax_main)  # attach y axis of ax to ax1
        ax.get_yaxis().set_visible(False)  # hide y axis


def set_equal_xlim(ax_in_col: list[plt.Axes]) -> None:
    """Set a column of sub-figures with same x limit by sharing their x-axis.
    Usually for hiding shared x-axis when plotting 3x3, 4x4 figure.

    Note: here we assume the bottom most sub-figure is the main sub-figure, of which x axis is reserved
    Other sub-figures are attached to the main sub-figures and their x axis are hidden.

    Args:
        ax_in_col (list[plt.Axes]): a column of sub-figures in a matrix of sub-figures.
    """
    ax_main = ax_in_col[-1]
    for ax in ax_in_col[:-1]:
        ax.sharex(ax_main)  # attach x axis of ax to ax1
        ax.get_xaxis().set_visible(False)  # hide x axis


def ticks_align_limits_x(ax: plt.Axes, thresholdRatio=0.1) -> None:

    # Call this in the end.

    # Align ticks with end of x & y axis, assume smaller end is already set to 0.
    # Thus, only need to adjust the larger end.

    # If

    # x axis
    # The locations are not clipped to the current axis limits and hence
    # may contain locations that are not visible in the output.
    xTicks: np.ndarray = ax.get_xticks()

    xmin, xmax = ax.get_xlim()
    # print(xTicks)
    if xTicks[-2] < xmax <= xTicks[-1]:
        dx = xTicks[-1] - xTicks[-2]
        if (xmax - xTicks[-2]) / dx < thresholdRatio:
            xmaxNew = xTicks[-2]
            # print('1')
        else:
            xmaxNew = xTicks[-1]
            # print("2")
        # print(xmin, xmaxNew)
        ax.set_xlim(xmin, xmaxNew)
    else:
        message = "Get %f < %f < %f" % (xTicks[-2], xmax, xTicks[-1])
        assert False, message


def ticks_align_limits_y(ax: plt.Axes, thresholdRatio=0.1) -> None:
    yTicks: np.ndarray = ax.get_yticks()

    ymin, ymax = ax.get_ylim()
    # print(yTicks)
    if yTicks[-2] < ymax <= yTicks[-1]:
        dx = yTicks[-1] - yTicks[-2]
        if (ymax - yTicks[-2]) / dx < thresholdRatio:
            ymaxNew = yTicks[-2]
            # print("1")
        else:
            ymaxNew = yTicks[-1]
            # print("2")
        # print(ymin, ymaxNew)
        ax.set_ylim(ymin, ymaxNew)
    else:
        assert False

    # y axis
    # yTicks: np.ndarray = ax.get_yticks()
    # newTick = 2 * yTicks[-1] - yTicks[-2]
    # yTicksNew = np.append(yTicks, newTick)
    # ax.set_yticks(yTicksNew)


# * check whether font exist
if __name__ == "__main__":
    fontPath = matplotlib.font_manager.findfont("Times New Roman")
    print(fontPath)
