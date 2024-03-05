'''
Templates for matplotlib.
'''
from typing import Optional, List, Literal

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def share_plot(fig: plt.Figure,
               row: int, col: int,
               rect=[0.15, 0.12, 0.10, 0.05]) -> List[plt.Axes]:
    '''
    make axes that sharing x-axis and y-axis.

    Parameters
    ----------
    fig: matplotlib.pyplot.Figure
        input figure to add axes.
    row, col: int
        row and collum number of axes
    rect: sequence of float
        margin of new axes, [left, bottom, right, top].

    Returns
    -------
    axes: Axes
        sequence of axes
    '''
    width = (1-rect[0]-rect[2])/col
    height = (1-rect[1]-rect[3])/row
    axes = []
    for i in range(row):
        for j in range(col):
            left = rect[0]+j*width
            bot = rect[1]+(row-i-1)*height
            axis = fig.add_axes((left, bot, width, height))
            axes.append(axis)
    return axes


def add_1_colorbar(fig: plt.Figure,
                   mappable: mpl.cm.ScalarMappable,
                   rect=[0.91, 0.1, 0.02, 0.8],
                   **kwargs,
                   ) -> None:
    '''
    plot a colorbar in the figure.

    Parameters
    ----------
    fig: matplotlib.pyplot.Figure
        input figure to plot colorbar.
    mappable: matplotlib.cm.ScalarMappable
        input mappable object.
        return value of plt.plot, plt.imshow etc.
    rect: sequence of float
        The dimensions [left, bottom, width, height] of the colorbar.
    **kwargs:
        options to pass to fig.colorbar.

    Returns
    -------
    None
    '''
    cax = fig.add_axes(rect)
    fig.colorbar(mappable, cax=cax, **kwargs)


def rotate_labels(axes: plt.Axes, angle: float, labels, axis='x') -> None:
    '''
    rotate the labels

    Parameters
    ----------
    axes: matplotlib.pyplot.Axes
        input axes to rotate the labels.
    angle: float
        rotation angle.
    labels: sequence of labels.
        labels of the axis.
    axis: {'x', 'y'}
        The axis to apply the changes on.

    Returns
    -------
    None
    '''
    if axis == 'x':
        if angle % 360 <= 180:
            axes.set_xticklabels(labels, ha='right')
        else:
            axes.set_xticklabels(labels, ha='left')
        plt.setp(axes.get_xticklabels(), rotation=angle)
    elif axis == 'y':
        axes.set_yticklabels(labels, ha='right')
        plt.setp(axes.get_xticklabels(), rotation=angle)


def change_im_aspect(X: np.ndarray, axes: plt.Axes, aspect: float = 1.0,
                     **kwargs) -> mpl.image.AxesImage:
    '''
    display data as an image at given aspect ratio.

    Parameters
    ----------
    X: array-like or PIL image
        this is passed to the matplotlib.pyplot.imshow.
    aspect: the aspect ratio of the image.
        vertical length over horizontal length.
    kwargs: key ward arguments to pass to matplotlib.pyplot.imshow.

    Returns
    -------
    img: AxesImage
        the returned value of matplotlib.pyplot.imshow.
    '''

    leny, lenx = X.shape[:2]
    img_asp = float(leny)/lenx
    ret_asp = 1.0/img_asp*aspect
    return axes.imshow(X, aspect=ret_asp, **kwargs)


def get_fig_w_pixels(xpixel: int, ypixel: int,
                     dpi: Optional[float] = None,
                     *args, **kwargs) -> plt.Figure:
    """
    create a figure with any pixel values.

    Parameters
    ----------
    xpixel, ypixel: int
        Pixel values of each axis.

    dpi Optional[float]
        Dot per inch for the figure. If None is set, use the default value.

    args:
        arguments passed to the plt.figure.

    kwargs:
        keyword arguments passed to the plt.figure.

    Returns
    -------
    figure: Figure
        the created Figure object
    """
    if dpi is None:
        dpi = plt.rcParams['figure.dpi']
    figx = xpixel/dpi
    figy = ypixel/dpi
    if 'figsize' in kwargs:
        del kwargs['figsize']
    if 'dpi' in kwargs:
        del kwargs['dpi']
    return plt.figure(figsize=(figx, figy), dpi=dpi, *args, **kwargs)


def make_table(axes: plt.Axes, data: np.ndarray,
               colLabels: List[str], rowLabels: List[str],
               color: Optional[np.ndarray] = None,
               cellLoc: Literal['left', 'center', 'right'] = 'center',
               colLoc: Literal['left', 'center', 'right'] = 'right',
               rowLoc: Literal['left', 'center', 'right'] = 'center',
               ) -> None:
    """
    create a (looks natural) table image using matplotlib.

    Parameters
    ----------
    axes: matplotlib.pyplot.Axes
        An axes object that is uesd to create the table.
    data: 2D-ndarray
        The data shown in the table. The shape should be (n_row, n_col).

    colLabels: list of strings
        A list of strings shown at the first collum of the table.
        The length should be same as n_col.

    rowLabels: list of strings
        A list of strings shown at the first row of the table.
        The length should be same as n_row.

    color: 2D-list of colors or None
        2D list of background colors of the cells.

    cellLoc: 'left', 'center' or 'right'
        The alignment of the text within the cells.

    colLoc: 'left', 'center' or 'right'
        The text alignment of the column header cells.

    rowLoc: 'left', 'center' or 'right'
        The text alignment of the row header cells.

    Returns
    -------
    None
    """
    assert data.shape[0] == len(rowLabels)
    assert data.shape[1] == len(colLabels)

    axes.axis('off')
    table = axes.table(cellText=data, loc='center',
                       colLabels=colLabels, rowLabels=rowLabels,
                       cellColours=color, cellLoc=cellLoc,
                       colLoc=colLoc, rowLoc=rowLoc)
    for pos, cell in table.get_celld().items():
        cell.set_height(1/len(rowLabels))
