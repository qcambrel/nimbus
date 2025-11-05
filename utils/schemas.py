import numpy as np
import matplotlib as mpl
import cartopy.crs as ccrs
from typing import Any, Type
from pydantic import BaseModel
import matplotlib.pyplot as plt

class BandpassContext(BaseModel):
    ideal: bool       = False
    butterworth: bool = False
    gaussian: bool    = False

class PlotterContext(BaseModel):
    projection: Type[ccrs.Projection]               = ccrs.PlateCarree
    transform: Type[ccrs.Projection]                = ccrs.PlateCarree
    tag: str | None                                 = None
    cmap: str | Type[mpl.colors.Colormap]           = "viridis"
    norm: Type[mpl.colors.Normalize] | None         = None
    vmin: float | None                              = None
    vmax: float | None                              = None
    interpolation: str | None                       = None
    extent: tuple[float, float, float, float]       = (-180, 180, -90, 90)
    origin: str | None                              = "lower"
    resolution: int | None                          = None
    limit: tuple[float, float, float, float] | None = None
    bbox_inches: str | None                         = "tight"
    pad_inches: float | None                        = 0
    transparent: bool | None                        = False

class BatchContext(BaseModel):
    fn_args: list[Any] | None        = None
    fn_kwargs: dict[str, Any] | None = None
    batch_size: int | None           = None
    num_cpus: float | None           = None
    num_gpus: float | None           = None
    concurrency: int | None          = None
    batch_format: str | None         = None

class BackgroundContext(BaseModel):
    background: str | None                    = None
    background_name: str | None               = None
    tag: str | None                           = None
    resolution: int | None                    = None
    projection: Type[ccrs.Projection]         = ccrs.PlateCarree
    transform: Type[ccrs.Projection]          = ccrs.PlateCarree
    facecolor: str | None                     = None
    edgecolor: str | None                     = None
    linewidth: float | None                   = None
    shape: tuple[int, int] | None             = None
    extent: tuple[float, float, float, float] = (-180, 180, -90, 90)
    bbox_inches: str | None                   = "tight"
    pad_inches: float | None                  = 0
    transparent: bool | None                  = False
    compress: int | None                      = 9

class CoastlineContext(BaseModel):
    coastlines: str | None                    = None
    tag: str | None                           = None
    resolution: int | None                    = None
    projection: Type[ccrs.Projection]         = ccrs.PlateCarree
    transform: Type[ccrs.Projection]          = ccrs.PlateCarree
    facecolor: str | None                     = None
    edgecolor: str | None                     = None
    linewidth: float | None                   = None
    extent: tuple[float, float, float, float] = (-180, 180, -90, 90)
    bbox_inches: str | None                   = "tight"
    pad_inches: float | None                  = 0
    transparent: bool | None                  = True
    compress: int | None                      = 9

class BorderContext(BaseModel):
    borders: str | None                       = None
    tag: str | None                           = None
    resolution: int | None                    = None
    projection: Type[ccrs.Projection]         = ccrs.PlateCarree
    transform: Type[ccrs.Projection]          = ccrs.PlateCarree
    facecolor: str | None                     = None
    edgecolor: str | None                     = None
    linewidth: float | None                   = None
    extent: tuple[float, float, float, float] = (-180, 180, -90, 90)
    bbox_inches: str | None                   = "tight"
    pad_inches: float | None                  = 0
    transparent: bool | None                  = True
    compress: int | None                      = 9

class RoadContext(BaseModel):
    roads: str | None                         = None
    tag: str | None                           = None
    resolution: int | None                    = None
    projection: Type[ccrs.Projection]         = ccrs.PlateCarree
    transform: Type[ccrs.Projection]          = ccrs.PlateCarree
    facecolor: str | None                     = None
    edgecolor: str | None                     = None
    linewidth: float | None                   = None
    extent: tuple[float, float, float, float] = (-180, 180, -90, 90)
    bbox_inches: str | None                   = "tight"
    pad_inches: float | None                  = 0
    transparent: bool | None                  = True
    compress: int | None                      = 9

class RegridderContext(BaseModel):
    extent: tuple[float, float, float, float] = (-180, 180, -90, 90)
    method: str | None                        = "conservative"
    shape_in: tuple[int, int] | None          = None
    shape_out: tuple[int, int] | None         = None
    reuse_weights: bool | None                = False
    weights_dir: str | None                   = None

class ColormapContext(BaseModel):
    vmin: float | None               = None
    vmax: float | None               = None
    levels: Type[np.ndarray] | None  = None
    rgb_npy: Type[np.ndarray] | None = None
    rgb_mpl: str | None              = None
    filename: str | None             = None
    target: Type[np.ndarray] | None  = None
    ticks: Type[np.ndarray] | None   = None