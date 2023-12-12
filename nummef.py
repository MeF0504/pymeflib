#! /usr/bin/env python3
from typing import Tuple
from copy import copy

import numpy as np


def fft(x: np.ndarray, y: np.ndarray,
        ret_abs: bool = True) -> Tuple[np.ndarray, np.ndarray]:
    """
    Wrapper of numpy.fft module.

    Parameters
    ----------
    x: ndarray
        x variables.
    y: ndarray
        y variables.

    Returns
    -------
    freq: ndarray
        Frequency.
    out: ndarray
        Fourier transformed variables.
    """
    L = len(x)
    ff = np.fft.fft(y)
    ff /= len(ff)/2  # 2 ... +/-
    if ret_abs:
        ff = abs(ff)
    freq = np.fft.fftfreq(L, d=np.diff(x).mean())
    idx = np.where(freq > 1/x.max())
    return freq[idx], ff[idx]


def psd(x: np.ndarray, y: np.ndarray):
    """
    Calculate the Power Spectral Density (PSD) of y.

    Parameters
    ----------
    x: ndarray
        x variables.
    y: ndarray
        y variables.

    Returns
    -------
    freq: ndarray
        Frequency.
    psd: ndarray
        PSD.
    """
    Lx = len(x)
    dx = np.diff(x).mean()
    freq = np.fft.fftfreq(Lx, d=dx)
    idx = np.where(freq > 1/x.max())
    cy = copy(y)
    cy *= np.hamming(len(cy))
    ff = np.fft.fft(cy)
    ff /= len(cy)
    psd = abs(ff)**2
    psd *= dx
    return freq[idx], psd[idx]


if __name__ == '__main__':
    x = np.arange(0, 3, 0.1)
    y = np.sin(3*x*2*np.pi)+4*np.cos(x*2*np.pi)
    import matplotlib.pyplot as plt
    freq, ff = fft(x, y)
    freq2, psd_val = psd(x, y)
    fig1 = plt.figure()
    ax11 = fig1.add_subplot(2, 1, 1)
    ax12 = fig1.add_subplot(2, 1, 2)
    ax11.plot(freq, ff)
    ax12.plot(freq2, psd_val)
    ax12.set_xlabel('frequency')
    ax11.set_ylabel('Fourier Transformed')
    ax12.set_ylabel('PSD')

    plt.show()
