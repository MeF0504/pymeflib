import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def share_plot(fig: plt.Figure,
               row: int, col: int,
               rect=[0.15, 0.12, 0.10, 0.05]) -> plt.Axes:
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
    axes: sequence of axes
    '''
    width = (1-rect[0]-rect[2])/col
    height = (1-rect[1]-rect[3])/row
    axes = []
    for i in range(row):
        for j in range(col):
            left = rect[0]+j*width
            bot = rect[1]+(row-i-1)*height
            axis = fig.add_axes([left, bot, width, height])
            axes.append(axis)
    return axes


def add_1_colorbar(fig: plt.Figure,
                   image: mpl.image.AxesImage,
                   rect=[0.91, 0.1, 0.02, 0.8],
                   **kwargs,
                   ) -> None:
    '''
    plot a colorbar in the figure.

    Parameters
    ----------
    fig: matplotlib.pyplot.Figure
        input figure to plot colorbar.
    image: matplotlib.image.AxesImage
        input image of colorbar.
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
    fig.colorbar(image, cax=cax, **kwargs)


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
    img: the returned value of matplotlib.pyplot.imshow.
    '''

    leny, lenx = X.shape[:2]
    img_asp = float(leny)/lenx
    ret_asp = 1.0/img_asp*aspect
    return axes.imshow(X, aspect=ret_asp, **kwargs)
