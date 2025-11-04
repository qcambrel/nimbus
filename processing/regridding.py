import os
import numpy as np
import xesmf as xe
import xarray as xr
from utils.schemas import RegridderContext

def bounds(centers: np.ndarray) -> np.ndarray:
    """
    Computes the cell boundaries of center coordinates for conservative regridding.
    """
    dist: np.ndarray  = np.diff(centers) / 2
    first: np.ndarray = centers[0] - dist[0]
    last: np.ndarray  = centers[-1] + dist[-1]
    return np.concatenate([[first], centers[:-1] + dist, [last]])

def build_regridder(context: RegridderContext) -> xe.Regridder:
    """
    Builds a regridder for conservative, bilinear, or nearest regridding.

    Optional: Save weights for reuse.
    """
    method: str    = context.method
    x0, x1, y0, y1 = context.extent

    shape_in: tuple[int, int]  = context.shape_in
    shape_out: tuple[int, int] = context.shape_out

    lon_in: np.ndarray  = np.linspace(x0, x1, shape_in[1])
    lat_in: np.ndarray  = np.linspace(y0, y1, shape_in[0])
    lon_out: np.ndarray = np.linspace(x0, x1, shape_out[1])
    lat_out: np.ndarray = np.linspace(y0, y1, shape_out[0])

    match method:
        case "conservative":
            lon_b_in: np.ndarray  = bounds(lon_in)
            lat_b_in: np.ndarray  = bounds(lat_in)
            lon_b_out: np.ndarray = bounds(lon_out)
            lat_b_out: np.ndarray = bounds(lat_out)
            
            grid_in = xr.Dataset(
                {
                    "lon": (["lon"], lon_in),
                    "lat": (["lat"], lat_in),
                    "lon_b": (["lon_b"], lon_b_in),
                    "lat_b": (["lat_b"], lat_b_in)
                }
            )

            grid_out = xr.Dataset(
                {
                    "lon": (["lon"], lon_out),
                    "lat": (["lat"], lat_out),
                    "lon_b": (["lon_b"], lon_b_out),
                    "lat_b": (["lat_b"], lat_b_out)
                }
            )
        case "bilinear" | "nearest":
            grid_in = {
                "lon": lon_in,
                "lat": lat_in
            }

            grid_out = {
                "lon": lon_out,
                "lat": lat_out
            }
        case _:
            raise ValueError(f"Invalid regridding method: {method}")
    
    reuse_weights: bool     = context.reuse_weights
    weights_dir: str | None = context.weights_dir
    filename: str | None    = os.path.join(weights_dir, f"{method}-weights.nc") if reuse_weights else None
    
    regridder = xe.Regridder(
        grid_in,
        grid_out,
        method=method,
        filename=filename,
        reuse_weights=reuse_weights
    )
    return regridder