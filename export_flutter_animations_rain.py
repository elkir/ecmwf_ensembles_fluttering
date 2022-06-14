from matplotlib.pyplot import tight_layout
import xarray as xr
import cartopy.crs as ccrs
from pathlib import Path
import flutter


## Directories
dir_data = Path("data/reduced")
dir_fig = Path("data/fig")
dir_vid = dir_fig/ "vid"

#%% Shared parameters

## variable to animate
var = "tp"

Es=[50,100] 

timesteps = 5
Ts = range(0,11,11//timesteps)

n_repetitions = 2
shuffle = True

params_prec = dict(vmin=0, vmax=0.025, cmap="inferno")
threshold_op = "gt"

tight_layout=False



#%% Plumbing
## Mapping between two different variable naming schemes
var_map = {
    "2t":"t2m",
    "msl":"msl",
    "10fg":"fg10",
    "tp":"tp"
}
var2 = var_map[var]


## generating filenames
f_var_fun = lambda var : f"hundred_members_{var}_pf.nc"
f_var = {var:f_var_fun(var) for var in
    ["2t",
    "msl",
    "10fg",
    "tp"]}


## Load data set
filename = dir_data/f_var[var]
da = xr.load_dataset(filename)
da = da.assign_coords({"longitude": [ i if i <= 180 else i-360 for i in da.longitude.values]})
# reduce spatial range
da = da.sel(longitude=slice(-20,20),latitude=slice(65,35))
# remove cumulative aggregation in total precipitation
da_diff = da.diff("time",label="upper")
da = xr.concat([da.isel(time=0).copy(),da_diff], dim="time")


#%% Animation
## evolving timesteps 
## temperature - no threshold

prec_threshold = None

for E in Es:
    flutter.export_flutter(da,var2,Ts,E,
            filename=dir_vid/f"ensembles_time_prec_all_T{timesteps}_{E}.mp4",
            projection= ccrs.PlateCarree(),
            transform = ccrs.PlateCarree(),
            plot_params=params_prec,
            threshold=prec_threshold,
            threshold_op=threshold_op,
            n_repetitions=n_repetitions, shuffle=shuffle,
            title=f"Precipitation field N_ens:{E:3}",            
            tight_layout=tight_layout
            )


#%% Animation
## evolving timesteps 
## threshold temperature - freezing

prec_threshold = 0.001

## loop through parameters and export
for E in Es:
    flutter.export_flutter(da,var2,Ts,E,
            filename=dir_vid/f"ensembles_time_prec_T{timesteps}_{E}.mp4",
            projection= ccrs.PlateCarree(),
            transform = ccrs.PlateCarree(),
            plot_params=params_prec,
            threshold=prec_threshold,
            threshold_op=threshold_op,
            n_repetitions=n_repetitions, shuffle=shuffle,
            title=f"Precipitation N_ens:{E:3}",
            tight_layout=tight_layout
            )

