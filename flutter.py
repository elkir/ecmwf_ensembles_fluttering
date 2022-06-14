
## Utilities

# import matplotlib
# import xarray as xr
# import numpy as np
# import cartopy.crs as ccrs


import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, ArtistAnimation, FFMpegWriter

def test_import():
    print("Package flutter imported!")

def datef(X):
    # Format time into date and hour
    return X.time.dt.strftime('%Y-%m-%d %Hh').values


    
def animate_timestep(dt,var, E,ax,
                     threshold=None,
                     plot_params=dict(),
                     n_repetitions=1, shuffle=False,
                     title=None):
    #returns list of artists
    
    import random
    artists = []
    artists_T = []
    for E in range(1,101,100//E):
        ds = dt.sel(number=E)[var]
        
        # threshold on freezing 
        if threshold is not None:
            ds = ds.where(ds<threshold) 
        
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
    
def animate_time(da, var, Ts, E, ax, threshold, plot_params,
                n_repetitions=2,shuffle=False,
                title=None):
    #returns list of artists
    artists = []
    
    for T in Ts:
        dt = da.isel(time=T)
        artists.extend(animate_timestep(dt,var, E, ax=ax, 
                                        threshold=threshold, plot_params=plot_params,
                                        n_repetitions=n_repetitions,shuffle=shuffle,
                                        title=title))
        if title is not None:
            ax.set_title(title)     
    return artists
    
    

def export_flutter(da,var,Ts,E,filename,
            projection, transform,
            plot_params=dict(),
            threshold=None,
            n_repetitions=2,shuffle=False,
            title=None
            ):
    # Generate flutter video given dataset, timesteps and ensembles
    
    plt.close()
    fig, ax = plt.subplots(subplot_kw=dict(projection=projection))
    fig.tight_layout(pad=0)
    ax.coastlines(resolution='50m')
    if title is not None:
        ax.set_title(title) 
        
    plot_params = plot_params.copy()
    plot_params['transform']=transform
    
    artists = animate_time(da,var,Ts,E, ax=ax,
                           threshold=threshold,plot_params=plot_params,
                           n_repetitions=n_repetitions,shuffle=shuffle,
                           title=title)


    ani = ArtistAnimation(fig, artists, interval=1700//E, blit=True,
                                    repeat_delay=1000)
   
    ani.save(filename)
    
    # generates flutter video and saves it
    pass



