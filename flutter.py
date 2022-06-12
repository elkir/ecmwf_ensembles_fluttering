
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


    
def animate_time(da, Ts, E, ax, threshold, plot_params,
                n_repetitions=2,shuffle=False):
    #returns list of artists
    artists = []
    
    for T in Ts:
        dt = da.isel(time=T)
        artists.extend(animate_timestep(dt,E, ax, 
                                        threshold=threshold, plot_params=plot_params,
                                        n_repetitions=n_repetitions,shuffle=shuffle))
    return artists
    
def animate_timestep(dt, E,ax,
                     threshold=None,
                     plot_params=dict(),
                     n_repetitions=1, shuffle=False
                     ):
    #returns list of artists
    
    import random
    artists = []
    artists_T = []
    for E in range(1,101,100//E):
        ds = dt.sel(number=E).t2m
        
        # threshold on freezing 
        if threshold is not None:
            ds = ds.where(ds<threshold) 
        
        im = ds.plot(animated=True,add_colorbar=False,**plot_params)
        # if E==1:
        #    ds.plot(**params, animated=True)
        artists_T.append([im])
        ax.set_title(f"N_ens:{E:3}  time: {datef(dt)}") 
    if shuffle:
        for _ in range(n_repetitions):
            random.shuffle(artists_T)
            artists.extend(artists_T)
        else:
            artists.extend(artists_T*n_repetitions)
            
    return artists
    
    
## Animation
# evolving timesteps 
# threshold temperature - freezing





def export_flutter(da,Ts,E,filename,
            projection, transform,
            plot_params=dict(),
            threshold=None,
            n_repetitions=2,shuffle=False
            ):
    # Generate flutter video given dataset, timesteps and ensembles
    
    plt.close()
    fig, ax = plt.subplots(subplot_kw=dict(projection=projection))
    ax.coastlines(resolution='50m')
    
    plot_params = plot_params.copy()
    plot_params['transform']=transform
    
    artists = animate_time(da,Ts,E, ax=ax,
                           threshold=threshold,plot_params=plot_params,
                           n_repetitions=n_repetitions,shuffle=shuffle)


    ani = ArtistAnimation(fig, artists, interval=1700//E, blit=True,
                                    repeat_delay=1000)

    ani.save(filename)
    
    # generates flutter video and saves it
    pass



