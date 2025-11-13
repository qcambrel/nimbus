import numpy as np
from netCDF4 import Dataset
from processing.resampling import resample

def preprocess_wind_data(datasets: list[Dataset]) -> list[np.ndarray]:
    """
    Preprocesses wind data from a netCDF4 dataset.
    Applies fill value, masking, and wind vector calculation.

    Args:
        dataset (list[Dataset]): The netCDF4 dataset containing wind data

    Returns:
        list[np.ndarray]: The preprocessed wind data
    """
    preprocessed = []
    for dataset in datasets:
        uwnd = dataset.variables["uwnd"][0].data
        vwnd = dataset.variables["vwnd"][0].data
        fill = -9999.0
        u    = np.ma.masked_where(uwnd == fill, uwnd)
        v    = np.ma.masked_where(vwnd == fill, vwnd)
        w    = np.sqrt(u ** 2 + v ** 2)
        preprocessed.append(w)

    return preprocessed

def preprocess_weather_types(datasets: list[dict[str, Dataset]]) -> list[tuple[np.ndarray, ...]]:
    """
    Preprocesses weather type data from a netCDF4 dataset.
    Applies scale factors, elevation factor, and masking.

    Args:
        dataset (list[Dataset]): The netCDF4 dataset containing weather type data

    Returns:
        list[tuple[np.ndarray]]: The preprocessed weather type data
    """
    preprocessed = []

    scale_factors = {
        "PHIS": 1 / 9.81,
        "PRECSNO": 3600 / 25.4,
        "PRECTOT": 3600 / 25.4,
        "T2M": 1,
        "H1000": 1,
        "H500": 1,
        "SLP": 1 / 100
    }
    
    for dataset in datasets:
        data = {}
        asm  = dataset["asm"]
        flx  = dataset["flx"]
        slv  = dataset["slv"]

        wxtypes = ("PHIS", "PRECSNO", "PRECTOT", "T2M", "H1000", "H500", "SLP")

        for wxtype in wxtypes:
            if wxtype in asm.variables.keys():
                data[wxtype] = asm.variables[wxtype][0].data
            elif wxtype in flx.variables.keys():
                data[wxtype] = flx.variables[wxtype][0].data
            elif wxtype in slv.variables.keys():
                data[wxtype] = slv.variables[wxtype][0].data
        
        phis  = data["PHIS"]
        snow  = data["PRECSNO"]
        rain  = data["PRECTOT"]
        t2m   = data["T2M"]
        h1000 = data["H1000"]
        h500  = data["H500"]
        slp   = data["SLP"]

        for wxtype in data:
            data[wxtype] *= scale_factors[wxtype]

        ice         = snow * 0
        frzr        = snow * 0
        thick       = h500 - h1000
        elev_factor = (phis - 305) / 915

        elev_factor[np.where(elev_factor < 0)] = 0.0
        elev_factor[np.where(elev_factor > 1)] = 1.0

        elev_factor = elev_factor * 100
        low         = 5400 + elev_factor

        height_mask       = np.where((thick.any() >= low.any()) and (snow > 0))
        ice[height_mask]  = snow[height_mask]
        snow[height_mask] = 0.0

        rain[np.where(snow >= 0.1)] = 0.0
        rain[np.where(ice >= 0.1)]  = 0.0

        preprocessed.append((snow, ice, frzr, rain, t2m, slp))

    return preprocessed

def preprocess_accumulated_rain(datasets: list[Dataset]) -> list[np.ndarray]:
    """
    Preprocesses accumulated precipitation (rain) data from a netCDF4 dataset.
    Applies scale factor, fill value, cumulative sum, and masking.

    Args:
        dataset (list[Dataset]): The netCDF4 dataset containing accumulated precipitation data

    Returns:
        list[np.ndarray]: The preprocessed accumulated precipitation data
    """
    preprocessed = []

    scale_factor = 3600 / 25.4
    fill_value   = 1e15

    data = []

    for dataset in datasets:
        prec = dataset.variables["PRECTOT"][0].data
        prec = np.ma.masked_where(prec == fill_value, data)
        prec = prec * scale_factor
        data.append(prec)

    acc_data = np.cumsum(data, axis=0)
    acc_data = np.ma.masked_where(acc_data < 0.1, acc_data)

    preprocessed.append(acc_data)

    return preprocessed

def preprocess_accumulated_snow(datasets: list[Dataset]) -> list[np.ndarray]:
    """
    Preprocesses accumulated precipitation (snow) data from a netCDF4 dataset.
    Applies scale factor, fill value, cumulative sum, and masking.

    Args:
        dataset (list[Dataset]): The netCDF4 dataset containing accumulated precipitation data

    Returns:
        list[np.ndarray]: The preprocessed accumulated precipitation data
    """
    preprocessed = []

    scale_factor = 3600 / 25.4
    fill_value   = 1e15

    data = []

    for dataset in datasets:
        prec = dataset.variables["PRECSNO"][0].data
        prec = np.ma.masked_where(prec == fill_value, data)
        prec = prec * scale_factor
        data.append(prec)

    acc_data = np.cumsum(data, axis=0)
    acc_data = np.ma.masked_where(acc_data < 0.1, acc_data)

    preprocessed.append(acc_data)

    return preprocessed

def preprocess_vorticity_data(datasets: list[Dataset]) -> list[np.ndarray]:
    """
    Preprocesses vorticity data from a netCDF4 dataset.
    Applies fill value, masking, and coriolis effect.

    Args:
        dataset (list[Dataset]): The netCDF4 dataset containing vorticity data

    Returns:
        list[np.ndarray]: The preprocessed vorticity data
    """
    preprocessed = []

    rad      = np.pi / 180
    re       = 6371220.0
    rr       = re * rad
    lats     = 2 * (np.arange(720) / (720 - 1) - 0.5) * 90 * rad
    omeg     = 7.0721e-5
    coriolis = 2 * omeg * np.sin(lats * rad)
    deg_m    = 2 * re * np.pi / 720
    dlon_m   = deg_m * np.cos(lats * np.pi / 180)
    dlat_m   = deg_m
    dvdx     = np.zeros((720, 720))
    dudy     = np.zeros((720, 720))
    data     = np.zeros((720, 720))
    
    for dataset in datasets:
        heights = dataset.variables["H500"][0].data
        u       = dataset.variables["U500"][0].data
        v       = dataset.variables["V500"][0].data

        u = resample(u, (720, 720))
        v = resample(v, (720, 720))

        for j in range(720):
            for i in range(720):
                ip1 = i + 1
                if (i == 719):
                    ip1 = 0

                dvdx[j, i] = (v[j, ip1] - v[j, i]) / dlon_m[j]

                jp1 = j + 1
                if (j == 719):
                    jp1 = j

                dudy[j, i] = (u[jp1, i] - u[j, i]) / dlat_m
                data[j, i] = (dvdx[j, i] - dudy[j, i])

            data = data * 1.e5

        for j in range(720):
            if lats[j] <= 0:
                data[j, :] = -1 * data[j, :]

        data = data + coriolis

        preprocessed.append(data)

    return preprocessed