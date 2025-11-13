import os
import ray
import zipfile
import numpy as np
from PIL import Image
import earthaccess as ea
from netCDF4 import Dataset
import earthaccess.exceptions as eax
from processing import preprocessing
from utils import schemas, constants
from plotting import plots, colormaps
from processing.batching import batch_regrid, batch_resample, batch_plot 

def handler(event: dict):
    if (event["end"] - event["start"]).days > 5:
        raise ValueError(
            "Your time delta is too large. Reduce it to 5 days or less."
        )
    
    # print("EARTHDATA_USERNAME" not in os.environ)

    # if "EARTHDATA_USERNAME" not in os.environ:
    #     os.environ["EARTHDATA_USERNAME"] = event["auth_user"]
    
    # if "EARTHDATA_PASSWORD" not in os.environ:
    #     os.environ["EARTHDATA_PASSWORD"] = event["auth_pass"]

    if event["auth_user"]:
        os.environ["EARTHDATA_USERNAME"] = event["auth_user"]

    if event["auth_pass"]:
        os.environ["EARTHDATA_PASSWORD"] = event["auth_pass"]

    # print(os.environ["EARTHDATA_USERNAME"])
    # print(os.environ["EARTHDATA_PASSWORD"])
    # print("EARTHDATA_USERNAME" in os.environ)
    # if not os.environ["EARTHDATA_USERNAME"] or not os.environ["EARTHDATA_PASSWORD"]:
    #     raise ValueError(
    #         "Your EarthData credentials are missing. " \
    #         "Please add them to your environment variables or provide them in the form."
    #     )
    
    try:
        ea.login()
    except eax.LoginAttemptFailure:
        raise ValueError(
            "Your EarthData credentials are incorrect. " \
            "Please check them and try again."
        )

    if event["category"] == "weather types":
        datasets = []
        for short_name in event["dataset"]:
            results = ea.search_data(
                short_name=short_name,
                temporal=(event["start"], event["end"])
            )
            path = short_name[-3:].lower()
            ea.download(results, local_path=path)

        asm_paths = sorted(os.listdir("asm"))
        flx_paths = sorted(os.listdir("flx"))
        slv_paths = sorted(os.listdir("slv"))

        for i in range(len((asm_paths))):
            datasets.append({
                "asm": Dataset(asm_paths[i]),
                "flx": Dataset(flx_paths[i]),
                "slv": Dataset(slv_paths[i])
            })
    else:
        results = ea.search_data(
            short_name=event["dataset"],
            temporal=(event["start"], event["end"])
        )
        ea.download(results, local_path="data")

        datapaths = os.listdir("data")
        datasets  = [Dataset(datapath) for datapath in datapaths]

    match event["category"]:
        case "10m winds":
            preprocessed = preprocessing.preprocess_wind_data(datasets)
        case "weather types":
            preprocessed = preprocessing.preprocess_weather_types(datasets)
        case "accumulated rainfall":
            preprocessed = preprocessing.preprocess_accumulated_rain(datasets)
        case "accumulated snowfall":
            preprocessed = preprocessing.preprocess_accumulated_snow(datasets)
        case _:
            preprocessed = None
