import os
import io
import json
import boto3
import pickle
import zipfile
import requests
import numpy as np
import pandas as pd
from PIL import Image
from typing import Any
import geopandas as gpd
import matplotlib as mpl
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
from pyogrio import read_dataframe
from utils import constants
from utils.schemas import (
    BackgroundContext, CoastlineContext, BorderContext, RoadContext
)

def cache_background(cache_dir: str, context: BackgroundContext) -> str:
    """
    Pre-renders and caches high resolution background images.
    """
    fig = plt.figure(dpi=context.resolution)
    ax  = plt.axes(projection=context.projection)
    
    match context.background_name:
        case "natural":
            resp   = requests.get(context.background)
            buffer = io.BytesIO(resp.content)
            img    = Image.open(buffer)
            ax.imshow(img, extent=context.extent, transform=context.transform, regrid_shape=context.shape)
            buffer.close()
        case "white":
            ocean_color = context.background
            if os.path.exists("gshss.pkl"):
                with open("gshss.pkl", "rb") as f:
                    gshss = pickle.load(f)
            else:
                gshhs = cache_coastlines(cache=False)

            shore = cfeature.ShapelyFeature(
                gshhs.boundary,
                context.transform,
                facecolor=context.facecolor,
                edgecolor=context.edgecolor,
                linewidth=context.linewidth
            )

            ax.set_facecolor(ocean_color)
            ax.add_feature(shore)
            for spine in ax.spines.values():
                spine.set_visible(False)

            buffer = io.BytesIO()

            plt.axis("off")
            plt.savefig(buffer, format="png", bbox_inches=context.bbox_inches, pad_inches=context.pad_inches)
            buffer.seek(0)

            img = plt.imread(buffer)
            ax.imshow(img, extent=context.extent, transform=context.transform, regrid_shape=context.shape)
            buffer.close()
        case _:
            plt.close()
            raise ValueError(f"Unknown background: {context.background_name}")
    
    save_dir = os.path.join(cache_dir, f"{context.tag}-{context.background_name}.png")
    plt.axis("off")
    plt.savefig(save_dir, bbox_inches=context.bbox_inches, pad_inches=context.pad_inches)
    plt.close()
    
    return save_dir

def cache_coastlines(cache_dir: str, temp_dir: str, context: CoastlineContext, cache: bool = True) -> gpd.GeoDataFrame | str:
    """
    Pre-renders and caches high resolution GSHHS coastlines.
    Caching the geometric transformation for reuse saves on compute time.
    """
    fig = plt.figure(dpi=context.resolution)
    ax  = plt.axes(projection=context.projection)

    resp = requests.get(context.coastlines)
    resp.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        shp_paths  = [
            z.extract(member) for member in z.namelist() if member.endswith(".shp") and "GSHHS_f" in member
        ]
        shapefiles = [read_dataframe(shp_path) for shp_path in shp_paths]
        gshhs      = gpd.GeoDataFrame(pd.concat(shapefiles), ignore_index=True)
        with open(f"{cache_dir}/gshss.pkl", "wb") as pkl:
            pickle.dump(gshhs, pkl)

    if not cache:
        return gshhs
    
    shore = cfeature.ShapelyFeature(
        gshhs.boundary,
        context.transform,
        facecolor=context.facecolor,
        edgecolor=context.edgecolor,
        linewidth=context.linewidth
    )
    ax.add_feature(shore)
    ax.set_extent(context.extent)

    save_dir = os.path.join(cache_dir, f"{context.tag}-gshhs.png")
    plt.axis("off")
    plt.savefig(save_dir, bbox_inches=context.bbox_inches, pad_inches=context.pad_inches, transform=context.transform)
    plt.close()

    return save_dir

def cache_borders(cache_dir: str, temp_dir: str, context: BorderContext) -> str:
    """
    Pre-renders and caches high resolution state and country borders.
    Caching the geometric transformation for reuse saves on compute time.
    """
    fig = plt.figure(dpi=context.resolution)
    ax  = plt.axes(projection=context.projection)

    url = context.borders

    if os.path.exists("borders.pkl"):
        with open("borders.pkl", "rb") as pkl:
            borders = pickle.load(pkl)
    else:
        resp = requests.get(url)
        resp.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
            gpkg_path = z.extractall(temp_dir)[0]
            countries = read_dataframe(gpkg_path, layer="ADM_0")
            states    = read_dataframe(gpkg_path, layer="ADM_1")
            borders   = gpd.GeoDataFrame(pd.concat([countries, states]), ignore_index=True)
    
        with open("borders.pkl", "wb") as pkl:
            pickle.dump(borders, pkl)

    border = cfeature.ShapelyFeature(
        borders.boundary,
        context.transform,
        facecolor=context.facecolor,
        edgecolor=context.edgecolor,
        linewidth=context.linewidth
    )
    ax.add_feature(border)

    save_dir = os.path.join(cache_dir, f"{context.tag}-borders.png")
    plt.axis("off")
    plt.savefig(save_dir, bbox_inches=context.bbox_inches, pad_inches=context.pad_inches, transparent=context.transparent)
    plt.close()

    return save_dir
    

def cache_roads(context: RoadContext) -> str:
    """
    Pre-renders and caches high resolution road network for the map.
    Caching the geometric transformation for reuse saves on compute time.
    """
    pass

def cache_rivers(context: RoadContext) -> str:
    """
    Pre-renders and caches high resolution river network for the map.
    Caching the geometric transformation for reuse saves on compute time.
    """
    pass

if __name__ == "__main__":
    views: tuple[str, ...]                     = constants.VIEWS
    projection_map: dict[int, ccrs.Projection] = constants.PROJECTION_MAP

    with open("views.json", "r") as f:
        views_spec: dict[str, dict[str, Any]]  = json.load(f)

    for bg_name in ("natural", "white"):
        linewidth: float = 0.125
        facecolor: str   = "none"
        edgecolor: str   = "black"

        match bg_name:
            case "natural":
                bg: str = constants.NATURAL_EARTH
            case "white":
                bg: str = constants.OCEAN_COLOR
            case _:
                raise ValueError(f"Unknown background: {bg}")
            
        for view in views:
            spec: dict[str, Any]                      = views_spec[view]
            extent: tuple[float, float, float, float] = spec["extent"]
            proj_code: int                            = spec["proj"]
            x, y = center                             = spec["center"]
            projection: ccrs.Projection               = projection_map[proj_code](x, y)
            bg_context: BackgroundContext             = BackgroundContext(
                tag=view,
                background=bg,
                extent=extent,
                facecolor=facecolor,
                edgecolor=edgecolor,
                linewidth=linewidth,
                projection=projection,
                background_name=bg_name,
                shape=constants.TARGET_SHAPE,
                resolution=constants.PREFERRED_DPI
            )
            cache_dir: str                            = constants.CACHE_DIR
            cache_background(cache_dir, bg_context)

    weather_variables: tuple[str, ...] = constants.WEATHER_VARIABLES
    aerosols_edgecolor: str            = constants.AEROSOLS_EDGECOLOR

    for weather_variable in weather_variables:
        match weather_variable:
            case "10m winds":
                linewidth: float = 0.125
                facecolor: str   = "none"
                edgecolor: str   = "black"
            case "2m temperature":
                linewidth: float = 0.125
                facecolor: str   = "none"
                edgecolor: str   = "black"
            case "sea level pressure":
                linewidth: float = 0.125
                facecolor: str   = "none"
                edgecolor: str   = "black"
            case "precipitation types":
                linewidth: float = 0.125
                facecolor: str   = "none"
                edgecolor: str   = "white"
            case "clean longwave infrared":
                linewidth: float = 0.125
                facecolor: str   = "none"
                edgecolor: str   = "white"
            case "radar reflectivity":
                linewidth: float = 0.125
                facecolor: str   = "none"
                edgecolor: str   = "black"
            case "aerosols":
                linewidth: float = 0.125
                facecolor: str   = "none"
                edgecolor: str   = aerosols_edgecolor
            case "accumulated rainfall":
                linewidth: float = 0.125
                facecolor: str   = "none"
                edgecolor: str   = "black"
            case "accumulated snowfall":
                linewidth: float = 0.125
                facecolor: str   = "none"
                edgecolor: str   = "black"
            case "convective available potential energy":
                linewidth: float = 0.125
                facecolor: str   = "none"
                edgecolor: str   = "black"
            case "total precipitable water":
                linewidth: float = 0.125
                facecolor: str   = "none"
                edgecolor: str   = "black"
            case _:
                raise ValueError(f"Unknown weather variable: {weather_variable}")
            
        for view in views:
            spec: dict[str, Any]                      = views_spec[view]
            extent: tuple[float, float, float, float] = spec["extent"]
            proj_code: int                            = spec["proj"]
            x, y = center                             = spec["center"]
            projection: ccrs.Projection               = projection_map[proj_code](x, y)
            gshhs_context: CoastlineContext           = CoastlineContext(
                tag=view,
                extent=extent,
                facecolor=facecolor,
                edgecolor=edgecolor,
                linewidth=linewidth,
                projection=projection,
                resolution=constants.PREFERRED_DPI,
                coastlines=constants.GSHHS_COASTLINES
            )
            cache_dir: str                            = constants.CACHE_DIR
            temp_dir: str                             = constants.TEMP_DIR
            cache_coastlines(cache_dir, temp_dir, gshhs_context)

            border_context: BorderContext             = BorderContext(
                tag=view,
                extent=extent,
                facecolor=facecolor,
                edgecolor=edgecolor,
                linewidth=linewidth,
                projection=projection,
                borders=constants.BORDERS,
                resolution=constants.PREFERRED_DPI
            )
            cache_borders(cache_dir, temp_dir, border_context)