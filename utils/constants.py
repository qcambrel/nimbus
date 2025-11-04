import os
import numpy as np
import matplotlib as mpl
import cartopy.crs as ccrs

ROOT_DIR: str                              = os.path.dirname(os.path.abspath(__file__))
NATURAL_EARTH: str                         = "https://shadedrelief.com/natural3/ne3_data/16200/textures/2_no_clouds_16k.jpg"
GSHHS_COASTLINES: str                      = "https://www.ngdc.noaa.gov/mgg/shorelines/data/gshhg/latest/gshhg-shp-2.3.7.zip"
BORDERS: str                               = "https://geodata.ucdavis.edu/gadm/gadm4.1/gadm_410-gpkg.zip"
ROADS: str                                 = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_roads.zip"
CACHE_DIR: str                             = os.path.join(ROOT_DIR, "features", "cache")
TARGET_SHAPE: tuple[int, int]              = (2760, 5760)
PREFERRED_DPI: int                         = 1500
OCEAN_COLOR: str                           = mpl.colors.rgb2hex(np.array([190, 232, 255]) / 255)
PROJECTION_MAP: dict[int, ccrs.Projection] = {
    0: ccrs.PlateCarree,
    1: ccrs.Orthographic,
    2: ccrs.LambertAzimuthalEqualArea,
    3: ccrs.Geostationary,
    4: ccrs.NearsidePerspective
}
VIEWS: tuple[str, ...]                     = (
    "northamerica_proj",
    "westpacific_proj",
    "goeseast_proj",
    "goeswest_proj",
    "meteosat8_proj",
    "meteosat10_proj",
    "himawari_proj",
    "nh_proj",
    "sh_proj",
    "usa_mapset",
    "centralusa_mapset",
    "midatlantic_mapset",
    "maryland_mapset",
    "northatlantic_mapset",
    "europe_mapset",
    "asia_mapset",
    "australia_mapset",
    "africa_mapset",
    "southamerica_mapset",
    "northamerica_mapset",
    "epacific_mapset",
    "indianocean_mapset",
    "westatlantic_mapset",
    "globe"
)
WEATHER_VARIABLES_SHORT: tuple[str, ...]    = (
    "wind",
    "temp",
    "pressure",
    "rain",
    "snow",
    "types",
    "cape",
    "tpw",
    "radar",
    "lwir",
    "aerosols",
    "vort"
)
WEATHER_VARIABLES_LONG: tuple[str, ...]     = (
    "10m winds",
    "2m temperature",
    "sea level pressure",
    "accumulated rainfall",
    "accumulated snowfall",
    "precipitation types",
    "convective available potential energy",
    "total precipitable water",
    "radar reflectivity",
    "clean longwave infrared",
    "aerosols",
    "vorticity"
)
AEROSOLS_EDGECOLOR: np.ndarray              = np.array([50, 50, 50]) / 255
TEMP_DIR: str                               = os.path.join(ROOT_DIR, "features", "tmp")
WEIGHTS_DIR: str                            = os.path.join(ROOT_DIR, "processing", "weights")