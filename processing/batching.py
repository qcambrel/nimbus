import os
import ray
import datetime
import numpy as np
import xesmf as xe
import matplotlib.pyplot as plt
from plotting.plots import Plotter
from utils.schemas import PlotterContext

def batch_regrid(batch: dict[str, np.ndarray], regridder: xe.Regridder) -> dict[str, np.ndarray]:
    """
    Batch process for regridding.

    Args:
        batch (dict[str, np.ndarray]): Batch of data to regrid
        regridder (xe.Regridder): Regridder to use for regridding

    Returns:
        dict[str, np.ndarray]: Batch of regridded data
    """
    batch["data"] = regridder(batch["data"])
    return batch

def batch_plot(batch: dict[str, np.ndarray], plotter_cls: Plotter, cache_dir: str, context: PlotterContext) -> dict[str, list[dict[str, str]]]:
    """
    Batch process for plotting.

    Args:
        batch (dict[str, np.ndarray]): Batch of data to plot
        plotter_cls (Plotter): Plotter class to use for plotting
        cache_dir (str): Directory to save plots to
        context (PlotterContext): Plotter context

    Returns:
        list[dict[str, str]]: List of plot data
    """
    result = []

    for image in batch["data"]:
        plotter   = plotter_cls(image, context)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        year  = timestamp[:4]
        month = timestamp[5:7]
        day   = timestamp[8:10]
        hour  = timestamp[11:13]
        
        full_path = os.path.join(cache_dir, context.tag, "frames", "10m-winds", year, month, day)
        os.makedirs(full_path, exist_ok=True)

        plotter.render(cache_dir, timestamp)
        img_path = os.path.join(full_path, f"{hour}.png")
        plt.savefig(img_path)
        plt.close()

        result.append({"path": img_path, "status": "created"})

    return {"image": result}