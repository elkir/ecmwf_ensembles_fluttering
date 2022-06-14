import xarray as xr
import cartopy.crs as ccrs
from pathlib import Path
import flutter


## Directories
dir_data = Path("data/reduced")
dir_fig = Path("data/fig")
dir_vid = dir_fig/ "vid"



#%% Shared parameters

## Variable to animate
var = "2t"

Es=[50,100] 

timesteps = 5
Ts = range(0,11,11//timesteps)

n_repetitions = 2
shuffle = True

params_temp = dict(vmin=250, vmax=290, cmap="viridis")
threshold_op = "lt"

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


#%% Animation
## evolving timesteps 
## temperature - no threshold

temp_threshold = None

for E in Es:
    flutter.export_flutter(da,var2,Ts,E,
            filename=dir_vid/f"ensembles_time_temp_T{timesteps}_{E}.mp4",
            projection= ccrs.PlateCarree(),
            transform = ccrs.PlateCarree(),
            plot_params=params_temp,
            threshold=temp_threshold,
            threshold_op=threshold_op,
            n_repetitions=n_repetitions, shuffle=shuffle,
            title=f"Temperatures N_ens:{E:3}",            
            tight_layout=tight_layout
            )


#%% Animation
## evolving timesteps 
## threshold temperature - freezing

temp_threshold = 273.15 

## loop through parameters and export
for E in Es:
    flutter.export_flutter(da,var2,Ts,E,
            filename=dir_vid/f"ensembles_time_freezing_T{timesteps}_{E}.mp4",
            projection= ccrs.PlateCarree(),
            transform = ccrs.PlateCarree(),
            plot_params=params_temp,
            threshold=temp_threshold,
            threshold_op=threshold_op,
            n_repetitions=n_repetitions, shuffle=shuffle,
            title=f"Temperatures <0⁰C N_ens:{E:3}",            
            tight_layout=tight_layout
            )
            

# %% Animation
## evolving timesteps 
## threshold temperature - subfreezing

temp_threshold = 268
for E in Es:
    flutter.export_flutter(da,var2,Ts,E,
            filename=dir_vid/f"ensembles_time_subfreezing_T{timesteps}_{E}.mp4",
            projection= ccrs.PlateCarree(),
            transform = ccrs.PlateCarree(),
            plot_params=params_temp,
            threshold=temp_threshold,
            threshold_op=threshold_op,
            n_repetitions=n_repetitions, shuffle=shuffle,
            title=f"Temperatures <-5⁰C N_ens:{E:3}",            
            tight_layout=tight_layout
            )


