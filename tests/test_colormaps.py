import numpy as np
import matplotlib.pyplot as plt
from utils.schemas import ColormapContext
from plotting.colormaps import Colormap, interpolate_levels

def test_extrema():
    context = ColormapContext(
        vmin = 0.0,
        vmax = 1.0,
        levels = None,
        rgb_npy = None,
        rgb_mpl = "viridis",
        filename = None,
        target = None,
        ticks = None
    )

    cmap = Colormap(context)
    assert cmap.norm.vmin == 0.0
    assert cmap.norm.vmax == 1.0
    assert cmap.cmap.name == "viridis"

def test_color_arrays():
    context = ColormapContext(
        vmin = 0.0,
        vmax = 1.0,
        levels = None,
        rgb_npy = np.array([-110, -59, -20, 6, 31, 57]).astype(np.float64),
        rgb_mpl = None,
        filename = None,
        target = None,
        ticks = None
    )

    cmap = Colormap(context)
    assert cmap.norm.vmin == 0.0
    assert cmap.norm.vmax == 1.0
    assert cmap.cmap.name == "from_list"

def test_interpolation():
    ticks  = np.array([-110, -59, -20, 6, 31, 57]).astype(np.float64)
    target = 5 * np.arange(256) / 255
    levels = interpolate_levels(ticks, target)
    assert levels.shape == target.shape
        