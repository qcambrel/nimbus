import os
import shutil
import datetime
import mimetypes
import numpy as np
from PIL import Image
import matplotlib as mpl
from plotting import plots
import cartopy.crs as ccrs
from utils.schemas import PlotterContext

def test_wind_plotter():
    data = np.random.rand(200, 300)
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    context = PlotterContext(
        projection=ccrs.Mercator,
        tag="test",
        resolution=1200,
        interpolation="nearest",
        norm=norm,
        center=(0, 0)
    )
    plotter = plots.WindPlotter(data, context)
    
    temp_dir = os.path.join(os.path.dirname(__file__), "temp")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    year = timestamp[:4]
    month = timestamp[5:7]
    day = timestamp[8:10]
    hour = timestamp[11:13]
    full_path = os.path.join(temp_dir, context.tag, "frames", "10m-winds", year, month, day)
    os.makedirs(full_path, exist_ok=True)
    
    plotter.render(temp_dir, timestamp)
    img_path = os.path.join(full_path, f"{hour}.png")
    assert os.path.exists(img_path)
    assert "png" in mimetypes.guess_file_type(img_path)[0]

    img = Image.open(img_path)
    bbox = img.getbbox()
    assert img.size == bbox[2:]
    assert bbox[:2] == (0, 0)

    shutil.rmtree(temp_dir)
    assert not os.path.exists(img_path)