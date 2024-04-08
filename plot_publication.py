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

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib

# * ====================================================================
# * Set font's properties.
# ! You must use from `PLOT_academic import *` to enable font size setting
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

# controls default text sizes
font = {"family": "Times New Roman", "weight": "normal", "size": SMALL_SIZE}  # bold
matplotlib.rc("font", **font)
# fontsize of the axes title, namely title of subplot
plt.rc("axes", titlesize=MEDIUM_SIZE)
plt.rc("axes", labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc("xtick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=SMALL_SIZE)  # legend fontsize
plt.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title
# * =====================================================================
# set latex font
matplotlib.rcParams["mathtext.fontset"] = "cm"
matplotlib.rcParams["mathtext.rm"] = "serif"


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
    def area(cls, length: str) -> str:
        assert length in cls.length_options

        unit_length = "%s" % length
        return "$\mathrm{%s}$" % (unit_length)

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
    def __init__(self, nrows, ncols, page=PageA4(), xrate=None, yrate=None, tightLayout=True) -> None:
        self.__bbox_inches = "tight"
        # 300 is usually minimum requirement for high resolution images, 600 is better
        self.__dpi = 300
        self.page: Page = page
        self.__nrows = nrows
        self.__ncols = ncols
        self.fig, self.ax = plt.subplots(nrows, ncols)
        self.tightLayout = tightLayout
        self.arrange(xrate, yrate)

        # make sure the height of each sub-figure equals the width
        if ncols > 1:
            for ax in self.ax.flatten():  # convert to 1d array
                ax.set_box_aspect(1)

    def arrange(self, xrate=None, yrate=None):
        """Automatically set size of the figure according to the page size and figure content.
        You can also do this manually by setting `xrate` and `yrate`.
        """
        # this rate is for sub-figure with full x-y labels
        # xy = (
        #     ((0.6, 0.30), (1.0, 0.28), (1.0, 0.25), (1.0, 0.25)),
        #     ((1.0, 0.55), (1.0, 0.55), (1.0, 0.55), (1.0, 0.55)),
        #     ((1.0, 0.80), (1.0, 0.80), (1.0, 0.80), (1.0, 0.80)),
        #     ((1.0, 1.00), (1.0, 1.00), (1.0, 1.00), (1.0, 1.00)),
        # )
        # * only need to define width because height will be automatically adjusted by `ax.set_box_aspect(1)`
        xy = (
            ((0.6, 0.30), (1.0, 1.00), (1.0, 1.00), (1.0, 1.00)),
            ((1.0, 0.55), (1.0, 0.55), (1.0, 0.55), (1.0, 0.55)),
            # ((1.0, 1.00), (1.0, 1.00), (1.0, 1.00), (1.0, 1.00)),
            ((1.0, 1.00), (1.0, 1.00), (1.0, 1.00), (1.0, 1.00)),
            ((1.0, 1.00), (1.0, 1.00), (1.0, 1.00), (1.0, 1.00)),
        )
        xrate1, yrate1 = xy[self.__nrows - 1][self.__ncols - 1]
        # Check these parameters are set manully.
        if xrate is not None:
            xrate1 = xrate
        if yrate is not None:
            yrate1 = yrate
        # set figure size
        height, width = self.page.body_size
        width1 = width * xrate1
        height1 = height * yrate1
        self.fig.set_size_inches(width1, height1)

    def save(self, savename: str, bbox_inches=None, dpi=None):
        """Save the figure in .svg format."""
        # format of save name should be "directory/figure.svg"
        format = savename.split(".")[-1]
        assert format == "svg" or format == "png"

        # if dpi is not assigned external, use dpi store in this class
        if dpi is None:
            dpi = self.__dpi

        # ! Warning: only the given portion of the figure is saved
        # ! This will change size of the figure when saving
        if bbox_inches is None:
            bbox_inches = self.__bbox_inches
        self.fig.savefig(savename, bbox_inches=bbox_inches, dpi=dpi)

        # self.fig.savefig(savename, dpi=dpi)

    def change_page(self, newpage=PageSlide()):
        # modify paper size, such as from A4 to a slide in 16:9
        self.page = newpage
        self.arrange()

    def stretch_figure_height(self, ratio: float) -> None:
        width, height = self.fig.get_size_inches()
        self.fig.set_size_inches(width, height * ratio)


def get_default_color(type="rgb") -> list:
    # [u'#1f77b4', u'#ff7f0e', u'#2ca02c', u'#d62728', u'#9467bd',
    # u'#8c564b', u'#e377c2', u'#7f7f7f', u'#bcbd22', u'#17becf']
    lst = matplotlib.rcParams["axes.prop_cycle"].by_key()["color"]  # hex
    if type == "rgb":
        # convert hex to rgb that ranges from 0 to 1
        lst = [list(int(h.lstrip("#")[i : i + 2], 16) / 256 for i in (0, 2, 4)) for h in lst]
    return lst


def legend(ax):
    ax.legend(frameon=False)  # remove legend background


def legend_subplot(fig, lines: list, labels: list[str], height_ratio=1.03, label_per_row=8) -> None:
    # add a legend for all plot
    # https://stackoverflow.com/questions/27016904/matplotlib-legends-in-subplot
    # https://matplotlib.org/stable/gallery/text_labels_and_annotations/legend_demo.html

    fig.legend(
        lines,
        labels,
        loc="upper center",
        frameon=False,
        # distance to center of the text box (both horizontal and vertical)
        bbox_to_anchor=(0.5, height_ratio),
        ncol=label_per_row,
    )


def set_tick_number_x(tick_number: int, ax) -> None:
    loc = MaxNLocator(tick_number)
    ax.xaxis.set_major_locator(loc)


def set_tick_number_y(tick_number: int, ax) -> None:
    loc = MaxNLocator(tick_number)
    ax.yaxis.set_major_locator(loc)


def cornor_annotate(
    ax,
    text: str,
    ratio: float = 0.02,
    text_size: float = 10,
    horizontal: str = "left",
    vertical: str = "top",
):
    # control distance from top left corner

    # get proper position for text
    if horizontal == "left" and vertical == "top":
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        x_range = x_max - x_min
        y_range = y_max - y_min
        # coordinate of top left corner of the text box
        x = x_min + ratio * x_range
        y = y_max - ratio * y_range
    else:
        raise ValueError("Not finished yet.")

    ax.text(x, y, text, size=text_size, horizontalalignment=horizontal, verticalalignment=vertical)


def more_space(ax, direction: str, ratio: float = 0.1) -> None:
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


def set_equal_ylim(ax_list: list):
    # usually for hiding shared y-axis when plotting 3x3, 4x4 figure

    # * find maximum limits of y axis for all axes in ax_list
    ymin = 1e8
    ymax = -1e8
    for ax in ax_list:
        ymin = min(ymin, ax.get_ylim()[0])
        ymax = max(ymax, ax.get_ylim()[1])

    # * set to all
    for ax in ax_list:
        ax.set_ylim(ymin, ymax)


# * check whether font exist
if __name__ == "__main__":
    fontPath = matplotlib.font_manager.findfont("Times New Roman")
    print(fontPath)
