#%%
from fileinput import filename
import matplotlib
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

#%%
figsize = (15,5)
matplotlib.rcParams['figure.figsize'] = figsize

#%%
dir_data = Path("../data/reduced")

f_var_fun = lambda var : f"hundred_members_{var}_pf.nc"
f_var = {var:f_var_fun(var) for var in
    ["2t",
    "msl",
    "10fg",
    "tp"]}
#%%
filename = dir_data/f_var["2t"]
# %%
da = xr.load_dataset(filename)
da = da.assign_coords({"longitude": [ i if i <= 180 else i-360 for i in da.longitude.values]})
# %%‘
da.sel(number=1).isel(time=1).t2m.plot(figsize=figsize)
# %%
(da.sel(number=1).isel(time=1)-da.sel(number=3).isel(time=1)).t2m.plot(figsize=figsize)

# %% Ensemble mean calculation
da_mean = da.mean(dim="number")

# %% Evolution of difference from mean
(da.sel(number=1)-da_mean).isel(time=10).t2m.plot(figsize=figsize)
# %%
