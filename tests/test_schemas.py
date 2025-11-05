import inspect
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from utils import constants
from utils.schemas import (
    PlotterContext,
    RegridderContext,
    BandpassContext,
    BatchContext,
    BackgroundContext,
    CoastlineContext,
    BorderContext,
    RoadContext
)

def test_batch_context():
    context = BatchContext(
        fn_args = [],
        fn_kwargs = {},
        batch_size = 1,
        num_cpus = 1,
        num_gpus = 1,
        concurrency = 1,
        batch_format = "numpy"
    )

    assert context.fn_args == []
    assert context.fn_kwargs == {}
    assert context.batch_size == 1
    assert context.num_cpus == 1
    assert context.num_gpus == 1
    assert context.concurrency == 1
    assert context.batch_format == "numpy"

def test_regridder_context():
    context = RegridderContext(
        method = "conservative",
        shape_in = (720, 1440),
        shape_out = (360, 720)
    )

    assert context.method == "conservative"
    assert context.extent == (-180, 180, -90, 90)
    assert context.shape_in == (720, 1440)
    assert context.shape_out == (360, 720)

def test_plotter_context():
    context = PlotterContext()

    projection_list = constants.PROJECTION_LIST

    projection = str(context.projection.__name__)
    transform  = str(context.transform.__name__)
    assert projection in projection_list
    assert transform in projection_list

    context.cmap = "twilight"
    builtin_colors = list(plt.colormaps)
    assert context.cmap in builtin_colors

    context.cmap = plt.cm.turbo
    assert context.cmap.name in builtin_colors