#! /usr/bin/env python3
from typing import Tuple
from copy import copy, deepcopy

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


def psd(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
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


def pca(data: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculate the PCA (Principal Component Analysis).
    (ref: https://arxiv.org/abs/1404.1100)

    Parameters
    ----------
    data: 2-D ndarray
        input 2-D data.

    Returns
    -------
    2-D ndarray
        represented 2-D data.
    ndarray
        principal components.
    2-D ndarray
       Covariance matrix of represented data.
    """
    data_orig = deepcopy(data)
    for i in range(data_orig.shape[0]):
        data_orig[i] -= np.mean(data_orig[i])
    C_x = np.dot(data_orig, data_orig.T)/len(data_orig[0])
    eig_val, eig_vec = np.linalg.eig(C_x)
    P = eig_vec.T
    Y = np.dot(P, data_orig)
    C_y = np.dot(Y, Y.T)/len(Y[0])
    return Y, P, C_y


if __name__ == '__main__':
    import sys
    import matplotlib.pyplot as plt
    if len(sys.argv) <= 1:
        pass
    elif sys.argv[1] == 'fft':
        x = np.arange(0, 3, 0.1)
        y = np.sin(3*x*2*np.pi)+4*np.cos(x*2*np.pi)
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
    elif sys.argv[1] == 'pca':
        in_freq = 100  # Hz
        time = np.arange(0, 10, 0.001)  # sec
        amp = 3  # ?
        noise = 1.0
        rot_angle = 30  # deg

        # Observe simple harmonic data
        # from a direction orthogonal to a certain direction
        raw_data = amp*np.sin(time/in_freq*2*np.pi)
        rot_mat = np.array([
                [np.cos(rot_angle*np.pi/180), np.sin(rot_angle*np.pi/180)],
                [-np.sin(rot_angle*np.pi/180), np.cos(rot_angle*np.pi/180)],
                ])
        data = np.zeros([2, len(time)])
        data[0] = raw_data
        # rotate by rot_angle
        data = np.dot(rot_mat, data)
        data += noise*np.random.random(data.shape)
        Y, P, C_y = pca(data)
        for i in range(data.shape[0]):
            data[i] -= np.mean(data[i])

        xlim = (np.min([data[0], Y[0]])*1.1, np.max([data[0], Y[0]])*1.1)
        ylim = (np.min([data[1], Y[1]])*1.1, np.max([data[1], Y[1]])*1.1)
        fig1 = plt.figure()
        ax11 = fig1.add_subplot(221)
        ax12 = fig1.add_subplot(222)
        ax11.scatter(data[0], data[1])
        ax11.set_xlim(xlim)
        ax11.set_ylim(ylim)
        ax11.set_title('input data')
        ax12.scatter(Y[0], Y[1])
        ax12.set_xlim(xlim)
        ax12.set_ylim(ylim)
        ax12.set_title('represented data')

        ax13 = fig1.add_subplot(223)
        im13 = ax13.imshow(C_y)
        fig1.colorbar(im13)
        ax13.set_title('Covariance matrix')
        ax14 = fig1.add_subplot(224)
        im14 = ax14.imshow(P)
        fig1.colorbar(im14)
        ax14.set_title('principal components')

        plt.show()
