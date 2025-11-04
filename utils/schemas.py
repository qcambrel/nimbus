import numpy as np
from typing import Any
import matplotlib as mpl
import cartopy.crs as ccrs
from pydantic import BaseModel
import matplotlib.pyplot as plt

class BandpassContext(BaseModel):
    ideal: bool       = False
    butterworth: bool = False
    gaussian: bool    = False

class PlotterContext(BaseModel):
    projection: ccrs.Projection     = ccrs.PlateCarree()
    transform: ccrs.Projection      = ccrs.PlateCarree()
    cmap: str | mpl.colors.Colormap = plt.cm.viridis
    norm: mpl.colors.Normalize      = None
    vmin: float                     = None
    vmax: float                     = None

class BatchContext(BaseModel):
    fn_args: list[Any] | None   = None
    fn_kwargs: dict[Any] | None = None
    batch_size: int | None      = None
    num_cpus: float | None      = None
    num_gpus: float | None      = None
    concurrency: int | None     = None

class BackgroundContext(BaseModel):
    background: str | None                    = None
    background_name: str | None               = None
    tag: str | None                           = None
    resolution: int | None                    = None
    projection: ccrs.Projection               = ccrs.PlateCarree()
    transform: ccrs.Projection                = ccrs.PlateCarree()
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
    projection: ccrs.Projection               = ccrs.PlateCarree()
    transform: ccrs.Projection                = ccrs.PlateCarree()
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
    projection: ccrs.Projection               = ccrs.PlateCarree()
    transform: ccrs.Projection                = ccrs.PlateCarree()
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
    projection: ccrs.Projection               = ccrs.PlateCarree()
    transform: ccrs.Projection                = ccrs.PlateCarree()
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
