'''
Templates for plotly.
'''
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
