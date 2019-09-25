import numpy as np

pi = np.pi
PI = np.pi


def log(z, phi=-np.pi):
    """
    Logarithm with specific branch. Elementvise operation.

    Args:
        z (complex): complex input to the function
        phi (float, optional): Logarithm branch would be (phi..phi+2*pi).
            Defaults to -np.pi.

    Returns:
        complex: log(z)=ro*exp(it) t in range (phi..phi+2*pi)
    """
    delta = (phi+np.pi)
    return np.log(z * np.exp(-1j*delta)) + 1j*delta
