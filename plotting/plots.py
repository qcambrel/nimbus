import os
import numpy as np
from PIL import Image
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from utils.schemas import PlotterContext

class Plotter(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def render(self):
        pass

class WindPlotter(Plotter):
    """
    10m winds

    The maximum sustained wind associated with a tropical cyclone is a 
    common indicator of the intensity of the storm. The global standard
    is to reflect winds 10 meters above mean sea level.
    """
    def __init__(self, data: np.ndarray, context: PlotterContext):
        pass

    def render(self):
        pass

class T2MPlotter(Plotter):
    """
    2m temperature

    The temperature of the air measured or forecast at a height of approximately
    2 meters above ground surface. The standard closely approximates human
    experience at ground level.
    """
    def __init__(self, data: np.ndarray, context: PlotterContext):
        pass

class WeatherPlotter(Plotter):
    """
    Precipitation
    - rain
    - snow
    - freezing rain
    - ice
    """
    def __init__(self, data: np.ndarray, context: PlotterContext):
        pass

    def render(self):
        pass

class CAPEPlotter(Plotter):
    """
    Convective available potential energy

    CAPE is a measure of the capacity of the atmosphere to support upward air
    movement that can lead to cloud formation and storms.
    """
    def __init__(self, data: np.ndarray, context: PlotterContext):
        pass

    def render(self):
        pass

class Pressurelotter(Plotter):
    """
    Sea level pressure
    
    Mean sea level pressure provides a standard baseline for comparing
    atmospheric pressure across different elevations. Mean sea level pressure
    is approximately 1013 hPa.
    """
    def __init__(self, data: np.ndarray, context: PlotterContext):
        pass

    def render(self):
        pass

class AerosolPlotter(Plotter):
    """
    Aerosols
    - seasalt
    - dust
    - organic carbon
    - black carbon
    - sulfate
    - nonitrate

    An aerosol is a suspension of fine solid particles or liquid droplets
    in a gas such as air.
    """
    def __init__(self, data: np.ndarray, context: PlotterContext):
        pass

    def render(self):
        pass

class LWIRPlotter(Plotter):
    """
    Clean longwave infrared

    Clean longwave infrared (LWIR) refers to a specific wavelength band in
    satellite imaging, primarily around 10.3 micrometers, that is less
    affected by atmospheric water vapor absorption. This band allows for
    more accurate measurements of the temperature of objects at the surface
    and in the atmosphere.
    """
    def __init__(self, data: np.ndarray, context: PlotterContext):
        pass

    def render(self):
        pass

class RadarPlotter(Plotter):
    """
    Radar reflectivity

    Radar reflectivity is a measure of how much power is returned to a weather
    radar by objects in the atmosphere, such as raindrops, snowflakes, and hail.
    It indicates the size, shape, and number of these particles, with brighter
    colors on a radar display representing heavier precipitation and larger particles.
    """
    def __init__(self, data: np.ndarray, context: PlotterContext):
        pass

    def render(self):
        pass

class AccRainPlotter(Plotter):
    """
    Accumulated rainfall

    Accumulated rainfall is the total amount of precipitation that has fallen
    during a specific period of time. It is a measure of the intensity and
    duration of precipitation events.
    """
    def __init__(self, data: np.ndarray, context: PlotterContext):
        pass

    def render(self):
        pass

class AccSnowPlotter(Plotter):
    """
    Accumulated snowfall

    Accumulated snowfall is the total amount of snow that has fallen during
    a specific period of time. It is a measure of the intensity and duration
    of snowfall events.
    """
    def __init__(self, data: np.ndarray, context: PlotterContext):
        pass

    def render(self):
        pass

class TPWPlotter(Plotter):
    """
    Total precipitable water

    Precipitable water is the depth of water in a column of the atmosphere, if
    all the water in that column were precipitated as rain.
    """
    def __init__(self, data: np.ndarray, context: PlotterContext):
        pass

    def render(self):
        pass

class VorticityPlotter(Plotter):
    """
    Vorticity

    The relative vorticity is the vorticity relative to the Earth induced by
    the air velocity field. In the northern hemisphere, positive vorticity is
    called cyclonic rotation, and negative vorticity is anticyclonic rotation.
    In the southern hemisphere, the direction of rotation is reversed. The absolute
    vorticity is computed from the air velocity relative to an inertial frame, and
    therefore includes a term due to the Earth's rotation, the Coriolis parameter.
    """
    def __init__(self, data: np.ndarray, context: PlotterContext):
        pass

    def render(self):
        pass