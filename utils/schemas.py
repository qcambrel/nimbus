import numpy as np
import matplotlib as mpl
import cartopy.crs as ccrs
from pydantic import BaseModel
from pydantic.types import conint
from typing import Any, Type, Optional, TypeAlias, Annotated, Callable

NormType: TypeAlias = Optional[Type[mpl.colors.BoundaryNorm] | Type[mpl.colors.Normalize]]
CmapType: TypeAlias = Optional[str | Type[mpl.colors.Colormap]]
ProjType: TypeAlias = Optional[Type[ccrs.Projection]]
ExtentType: TypeAlias = Optional[tuple[float, float, float, float]]
ArrayType: TypeAlias = Optional[Type[np.ndarray]]
# Channel = Annotated[int, Ge(0), Le(3)]
Channel = Annotated[int, conint(ge=0, le=3)]

class BandpassContext(BaseModel):
    ideal: bool       = False
    butterworth: bool = False
    gaussian: bool    = False

class PlotterContext(BaseModel):
    projection: ProjType | None        = ccrs.PlateCarree
    transform: ProjType | None         = ccrs.PlateCarree
    tag: str | None                    = None
    center: tuple[float, float] | None = None
    scale: float | None                = None
    cmap: CmapType | None              = "viridis"
    norm: NormType | None              = None
    vmin: float | None                 = None
    vmax: float | None                 = None
    interpolation: str | None          = None
    extent: ExtentType | None          = (-180, 180, -90, 90)
    origin: str | None                 = "lower"
    resolution: int | None             = None
    limit: ExtentType | None           = None
    bbox_inches: str | None            = "tight"
    pad_inches: float | None           = 0
    transparent: bool | None           = False
    inplace: bool | None               = False

class BatchContext(BaseModel):
    fn_args: list[Any] | None        = None
    fn_kwargs: dict[str, Any] | None = None
    batch_size: int | None           = None
    num_cpus: float | None           = None
    num_gpus: float | None           = None
    concurrency: int | None          = None
    batch_format: str | None         = None

class BackgroundContext(BaseModel):
    background: str | None        = None
    background_name: str | None   = None
    tag: str | None               = None
    resolution: int | None        = None
    projection: ProjType | None   = ccrs.PlateCarree
    transform: ProjType | None    = ccrs.PlateCarree
    facecolor: str | None         = None
    edgecolor: str | None         = None
    linewidth: float | None       = None
    shape: tuple[int, int] | None = None
    extent: ExtentType | None     = (-180, 180, -90, 90)
    bbox_inches: str | None       = "tight"
    pad_inches: float | None      = 0
    transparent: bool | None      = False
    compress: int | None          = 9

class CoastlineContext(BaseModel):
    coastlines: str | None      = None
    tag: str | None             = None
    resolution: int | None      = None
    projection: ProjType | None = ccrs.PlateCarree
    transform: ProjType | None  = ccrs.PlateCarree
    facecolor: str | None       = None
    edgecolor: str | None       = None
    linewidth: float | None     = None
    extent: ExtentType | None   = (-180, 180, -90, 90)
    bbox_inches: str | None     = "tight"
    pad_inches: float | None    = 0
    transparent: bool | None    = True
    compress: int | None        = 9

class BorderContext(BaseModel):
    borders: str | None         = None
    tag: str | None             = None
    resolution: int | None      = None
    projection: ProjType | None = ccrs.PlateCarree
    transform: ProjType | None  = ccrs.PlateCarree
    facecolor: str | None       = None
    edgecolor: str | None       = None
    linewidth: float | None     = None
    extent: ExtentType | None   = (-180, 180, -90, 90)
    bbox_inches: str | None     = "tight"
    pad_inches: float | None    = 0
    transparent: bool | None    = True
    compress: int | None        = 9

class RoadContext(BaseModel):
    roads: str | None           = None
    tag: str | None             = None
    resolution: int | None      = None
    projection: ProjType | None = ccrs.PlateCarree
    transform: ProjType | None  = ccrs.PlateCarree
    facecolor: str | None       = None
    edgecolor: str | None       = None
    linewidth: float | None     = None
    extent: ExtentType | None   = (-180, 180, -90, 90)
    bbox_inches: str | None     = "tight"
    pad_inches: float | None    = 0
    transparent: bool | None    = True
    compress: int | None        = 9

class RegridderContext(BaseModel):
    extent: ExtentType | None         = (-180, 180, -90, 90)
    method: str | None                = "conservative"
    shape_in: tuple[int, int] | None  = None
    shape_out: tuple[int, int] | None = None
    reuse_weights: bool | None        = False
    weights_dir: str | None           = None

class ColormapContext(BaseModel):
    vmin: float | None        = None
    vmax: float | None        = None
    levels: ArrayType | None  = None
    rgb_npy: ArrayType | None = None
    rgb_mpl: str | None       = None
    filename: str | None      = None
    target: ArrayType | None  = None
    ticks: ArrayType | None   = None

class BlendContext(BaseModel):
    scale: Callable | None  = None
    channel: Channel | None = None
    norm: NormType | None   = None
    cmap: CmapType | None   = None
    low: float | None       = None
    high: float | None      = None