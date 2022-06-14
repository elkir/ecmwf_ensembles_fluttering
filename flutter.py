
## Utilities

# import matplotlib
# import xarray as xr
# import numpy as np
# import cartopy.crs as ccrs


import operator

import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation, FFMpegWriter, FuncAnimation

ops = {
    "lt": operator.lt,
    "le": operator.le,
    "eq": operator.eq,
    "ne": operator.ne,
    "ge": operator.ge,
    "gt": operator.gt
}
    

def test_import():
    print("Package flutter imported!")

def datef(X):
    # Format time into date and hour e.g. "2022-01-15 12h"
    return X.time.dt.strftime('%Y-%m-%d %Hh').values


    
def animate_timestep(dt,var, E,ax,
                     threshold=None,
                     threshold_op=None,
                     plot_params=dict(),
                     n_repetitions=1, shuffle=False,
                     title=None):
    """Generate a list of plots for ArtistAnimation each displaying one ensemble. Designed to work with 2D xarray variables where the .plot() method outputs a 2D pcolormesh. 

    Args:
        dt (xarray.DataSet): DataSet with a single time step, several enesemble memebers parametrized by 'number' and 2D variables.
        var (string): String indexing the variable displayed. 
        E (integer): Number of ensembles to use. Should divide 100.
        ax (Axes): matplotlib axes to use
        threshold (float, optional): Upper threshold for the variable. Doesn't plot pixels with values above this. Defaults to None.
        threshold_op (str, optional): Specifies the threshold operator. ('lt', 'le', 'eq', 'ne', 'ge','gt' available)
        plot_params (dict, optional): Parameters passed to the plot function (e.g. cmap, vmin, vmax,...). Defaults to dict().
        n_repetitions (int, optional): Number of times each ensemble is repeated. Defaults to 1.
        shuffle (bool, optional): Are the ensembles shuffled in the repetitions? If not they appear in the same order. Defaults to False.
        title (string, optional): Title of the graph. Defaults to None.

    Returns:
        list of lists of Artist: Returns a list of lists of matplotlib Artist objects, to be used in ArtistAnimation.
    """
    
    
    import random
    artists = []
    artists_T = []
    for E in range(1,101,100//E):
        ds = dt.sel(number=E)[var]
        
        # threshold on freezing 
        if threshold is not None:
            ds = ds.where(ops[threshold_op](ds,threshold)) 
        
        
        im = ds.plot(animated=True,add_colorbar=False,ax=ax,**plot_params)
        # if E==1:
        #    ds.plot(**params, animated=True)
        if title is not None:
            ax.set_title(title) 
        artists_T.append([im])
        
    if shuffle:
        for _ in range(n_repetitions):
            random.shuffle(artists_T)
            artists.extend(artists_T)
    else:
        artists.extend(artists_T*n_repetitions)
            
    return artists
    
def animate_time(da, var, Ts, E, ax,
                 threshold=None,
                threshold_op=None, plot_params=dict(),
                n_repetitions=2,shuffle=False,
                title=None):
    """Generate a list of plots for ArtistAnimation fluttering through the ensembles and stepping forward in time. designed to work with 2D xarray variables. 

    Args:
        da (xarray.DataSet): Dataset with multiple timesteps ('time') and ensemble members ('number'), containing 2d variables.
        var (string): String indexing the variable displayed.
        Ts (list of integers): List of integers indexing the timesteps in the dataset  
        E (integer): Number of ensembles to use. Should divide 100.
        ax (Axes): matplotlib axes to use
        threshold (float, optional): Upper threshold for the variable. Doesn't plot pixels with values above this. Defaults to None.
        threshold_op (str, optional): Specifies the threshold operator. ('lt', 'le', 'eq', 'ne', 'ge','gt' available)
        plot_params (dict, optional): Parameters passed to the plot function (e.g. cmap, vmin, vmax,...). Defaults to dict().
        n_repetitions (int, optional): Number of times each ensemble is repeated. Defaults to 1.
        shuffle (bool, optional): Are the ensembles shuffled in the repetitions? If not they appear in the same order. Defaults to False.
        title (string, optional): Title of the graph. Defaults to None.


     Returns:
        list of lists of Artist: Returns a list of lists of matplotlib Artist objects, to be used in ArtistAnimation.
    """
    

    #returns list of artists
    artists = []
    
    for T in Ts:
        dt = da.isel(time=T)
        artists.extend(animate_timestep(dt,var, E, ax=ax, 
                                        threshold=threshold, threshold_op=threshold_op, plot_params=plot_params,
                                        n_repetitions=n_repetitions,shuffle=shuffle,
                                        title=title))
        if title is not None:
            ax.set_title(title)     
    return artists
    
    

def export_flutter(da,var,Ts,E,filename,
            projection, transform,
            threshold=None,
            threshold_op=None,
            plot_params=dict(),
            n_repetitions=2,shuffle=False,
            title=None,
            tight_layout=False
            ):
    """Generates a flutter animation and exports it to a file.

    Args:
        da (xarray.DataSet): Dataset to use
        var (string): Name of the variable to use
        Ts (list of integers): List in timestep indices to use
        E (integer): Number of Ensembles to use. Should divide 100.
        filename (string or Path object): Filename to save the video to. 
        projection (ccrs.Projection): Projection CRS to use
        transform (ccrs.transform): Transform of the CRS to use
        threshold (float, optional): Upper threshold for the variable. Doesn't plot pixels with values above this. Defaults to None.
        threshold_op (str, optional): Specifies the threshold operator. ('lt', 'le', 'eq', 'ne', 'ge','gt' available)
        plot_params (dict, optional): Parameters passed to the plot function (e.g. cmap, vmin, vmax,...). Defaults to dict().
        n_repetitions (int, optional): Number of times each ensemble is repeated. Defaults to 1.
        shuffle (bool, optional): Are the ensembles shuffled in the repetitions? If not they appear in the same order. Defaults to False.
        title (string, optional): Title of the graph. Defaults to None.
        tight_layout (bool, optional): Export only inner boxes (without titles).
        
    Returns:
        None: doesn't return a value.
    """
    
    plt.close()
    fig, ax = plt.subplots(subplot_kw=dict(projection=projection))
    if tight_layout:
        fig.tight_layout(pad=0)
    ax.coastlines(resolution='50m')
    if title is not None:
        ax.set_title(title) 
        
    plot_params = plot_params.copy()
    plot_params['transform']=transform
    
    artists = animate_time(da,var,Ts,E, ax=ax,
                           threshold=threshold, threshold_op=threshold_op,plot_params=plot_params,
                           n_repetitions=n_repetitions,shuffle=shuffle,
                           title=title)


    ani = ArtistAnimation(fig, artists, interval=1700//E, blit=True,
                                    repeat_delay=1000)
   
    ani.save(filename)
    
    pass



