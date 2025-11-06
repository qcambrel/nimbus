import os
import pickle
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.interpolate as interp
from utils.schemas import ColormapContext

class Colormap:
    def __init__(self, context: ColormapContext):
        self.rgb      = context.rgb_npy if context.rgb_npy is not None else context.rgb_mpl
        self.levels   = context.levels
        self.ticks    = context.ticks
        self.target   = context.target
        self.vmin     = context.vmin
        self.vmax     = context.vmax
        self.filename = context.filename
        self._map()

    def _map(self):
        if self.rgb is None:
            if self.filename and os.path.exists(self.filename):
                with open(self.filename, "rb") as pkl:
                    self.cmap = pickle.load(pkl)
            else:
                raise FileNotFoundError(f"Colormap file {self.filename} not found")
        elif type(self.rgb) is np.ndarray:
                self.cmap = mpl.colors.ListedColormap(self.rgb)
        elif type(self.rgb) is str:
                self.cmap = plt.colormaps[self.rgb]
        else:
            raise TypeError(f"Colormap type {type(self.rgb)} not supported")
        
        if self.vmin is not None and self.vmax is not None:
            self.norm   = mpl.colors.Normalize(vmin=self.vmin, vmax=self.vmax)
        else:     
            self.levels = interpolate_levels(self.ticks, self.target) if self.target else self.levels
            self.norm   = mpl.colors.BoundaryNorm(self.levels, self.cmap.N)

def interpolate_levels(ticks: np.ndarray, target: np.ndarray) -> np.ndarray:
    """
    Interpolate an array of tick values to target color levels

    Args:
        ticks (np.ndarray): The array of tick values
        target (np.ndarray): The target color levels

    Returns:
        np.ndarray: The interpolated color levels
    """
    func   = interp.interp1d(np.arange(len(ticks)), ticks)
    levels = func(np.linspace(0.0, len(ticks) - 1, len(target)))
    return levels