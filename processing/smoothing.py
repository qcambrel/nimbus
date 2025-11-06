import numpy as np
import scipy.signal as signal
from scipy.fft import fftshift, ifftshift, fftn, ifftn
from utils.schemas import BandpassContext

def savitzky_golay2d(z: np.ndarray, window_size: int, order: int, derivative: str = None) -> np.ndarray:
    """
    Applies a low pass Savitzky-Golay filter to a 2D array.
    Savitzky-Golay reduces noise while preserving important features.

    Args:
        z (np.ndarray): Input array
        window_size (int): Size of the window
        order (int): Order of the polynomial
        derivative (str): Optional derivative to apply

    Returns:
        np.ndarray: Filtered array
    """
    # number of polynomial terms
    n_terms = (order + 1) * (order + 2) / 2

    if window_size % 2 == 0:
        raise ValueError("window_size must be odd")

    if window_size ** 2 < n_terms:
        raise ValueError("order is too high for the window size")

    half_size = window_size // 2

    # polynomial exponents
    exps = [(k - n, n) for k in range(order + 1) for n in range(k + 1)]

    # coordinates
    ind = np.arange(-half_size, half_size + 1, dtype=np.float64)
    dx  = np.repeat(ind, window_size)
    dy  = np.tile(ind, [window_size, 1]).reshape(window_size ** 2)

    # system of equations
    A = np.empty((window_size ** 2, len(exps)))
    for i, (x, y) in enumerate(exps):
        A[:, i] = (dx ** x) * (dy ** y)

    # pad input array
    new_shape = (z.shape[0] + half_size * 2, z.shape[1] + half_size * 2)
    Z         = np.zeros(new_shape)

    # top band
    band                                = z[0, :]
    Z[:half_size, half_size:-half_size] = band - np.abs(np.flipud(z[1:half_size + 1, :]) - band)

    # bottom band
    band                                 = z[-1, :]
    Z[-half_size:, half_size:-half_size] = band + np.abs(np.flipud(z[-half_size - 1:-1, :]) - band)

    # left band
    band                                = np.tile(z[:, 0].reshape(-1, 1), [1, half_size])
    Z[half_size:-half_size, :half_size] = band - np.abs(np.fliplr(z[:, 1:half_size + 1]) - band)

    # right band
    band                                 = np.tile(z[:, -1].reshape(-1, 1), [1, half_size])
    Z[half_size:-half_size, -half_size:] = band + np.abs(np.fliplr(z[:, -half_size - 1:-1]) - band)

    # centeral band
    Z[half_size:-half_size, half_size:-half_size] = z

    # top left corner
    band                      = z[0, 0]
    Z[:half_size, :half_size] = band - np.abs(np.flipud(np.fliplr(z[1:half_size + 1, 1:half_size + 1])) - band)

    # bottom right corner
    band                        = z[-1, -1]
    Z[-half_size:, -half_size:] = band + np.abs(np.flipud(np.fliplr(z[-half_size - 1:-1, -half_size - 1:-1])) - band)

    # top right corner
    band                       = z[half_size, -half_size:]
    Z[:half_size, -half_size:] = band - np.abs(np.flipud(Z[half_size + 1:-half_size * 2 + 1, -half_size:]) - band)

    # bottom left corner
    band                       = z[-1, 0]
    Z[-half_size:, :half_size] = band + np.abs(np.fliplr(Z[-half_size:, half_size + 1:half_size * 2 + 1]) - band)

    # solve system and convolve
    match derivative:
        case None:
            m = np.linalg.pinv(A)[0].reshape((window_size, -1))
            return signal.fftconvolve(Z, m, mode="valid")
        case "col":
            c = np.linalg.pinv(A)[1].reshape((window_size, -1))
            return signal.fftconvolve(Z, -c, mode="valid")
        case "row":
            r = np.linalg.pinv(A)[2].reshape((window_size, -1))
            return signal.fftconvolve(Z, -r, mode="valid")
        case "both":
            c = np.linalg.pinv(A)[1].reshape((window_size, -1))
            r = np.linalg.pinv(A)[2].reshape((window_size, -1))
            return signal.fftconvolve(Z, -r, mode="valid"), signal.fftconvolve(Z, -c, mode="valid")
        case _:
            raise ValueError(f"invalid derivative: {derivative}")



def bandpass_filter(data: np.ndarray, low: float, high: float, context: BandpassContext) -> np.ndarray:
    """
    Applies a bandpass filter to a 2D array.
    Bandpass filters out frequencies outside of a specific range.
    """
    pass