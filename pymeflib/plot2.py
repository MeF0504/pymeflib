'''
Templates for plotly.
'''
from typing import Optional, Union

import numpy as np
import plotly.graph_objects as go
from plotly.graph_objects import Figure


def put_text(fig: Figure, x: int, y: int, text: str, **kwargs) -> None:
    """
    put a text at (x, y) point in the figure.

    Parameters
    ----------
    fig: plotly.graph_objects.Figure
        figure file of plotly.
    x: int
        x-coordinate of the figure.
    y: int
        y-coordinate of the figure.
    text: str
        text shown in the figure.
    **kwargs
        other keyword arguments passed to the fig.add_annotation function.

    Returns
    -------
    None
    """
    if 'showarrow' in kwargs:
        showarrow = kwargs['showarrow']
        kwargs.pop('showarrow')
    else:
        showarrow = False
    fig.add_annotation(text=text, x=x, y=y, showarrow=showarrow, **kwargs)


def hist_np(fig: Figure, data: np.ndarray,
            xmin: Optional[float] = None,
            xmax: Optional[float] = None,
            xbins: int = 100,
            row: Optional[Union[int, str]] = None,
            col: Optional[Union[int, str]] = None,
            secondary_y: Optional[bool] = None,
            exclude_empty_subplots: bool = False,
            **kwargs) -> None:
    """
    plot a histgram using Numpy module.

    Parameters
    ----------
    fig: Figure
        Figure object the histogram is plotted on.

    data: ndarray
        Input data histogram is computed.

    xmin, xmax: Optional[float]
        The minimum and maximum values of the histogram.

    xbins: int
        The number of bin.

    **kwargs:
        Other keyword arguments passed to the go.Bar function.

    Returns
    -------
    None
    """
    # https://plotly.com/python/histograms/
    if xmin is None:
        xmin = np.min(data)
    if xmax is None:
        xmax = np.max(data)
    counts, bins = np.histogram(data, bins=np.linspace(xmin, xmax, xbins))
    bins = 0.5 * (bins[:-1] + bins[1:])

    fig.add_trace(go.Bar(x=bins, y=counts, **kwargs),
                  row=row, col=col, secondary_y=secondary_y,
                  exclude_empty_subplots=exclude_empty_subplots)
