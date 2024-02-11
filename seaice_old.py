from netCDF4 import Dataset,num2date,date2num
import numpy as np
import numpy.ma as ma
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as mticker
import xarray as xr
import cartopy
from cartopy import crs as ccrs, feature as cfeature
import warnings
warnings.filterwarnings('ignore')
import glob
import struct
import datetime
import time
import sys
import os
import re

# def rescaled_cmap(levels, mapname='jet', cmap=cmap, enforcemidwhite=False):
#     num_color=levels.shape[0]
#     if not cmap:
#         cmap=cm.get_cmap(mapname)
#     colors=[]
#     for i in range(num_color):
#         color=cmap(1.*(i+1)/num_color)
#         colors.append(color) 
#         # print(i, color)
#     #new_colors=colors[1:-1]
#     new_colors=colors[0:-1]
#     # for c in new_colors:
#     #   print(c)
# #    print 'length of listed colors : ', len(new_colors)
#     if enforcemidwhite and len(new_colors)%2 == 1:
# #       print len(new_colors)/2, new_colors[len(new_colors)/2]  
#         new_colors[len(new_colors)/2] = (1.0, 1.0, 1.0, 1.0)
#     cmap2 = mpl.colors.ListedColormap(new_colors)
#     cmap2.set_under(colors[0])
#     cmap2.set_over(colors[-1])
#     cmap2.set_bad('0.75',1.0)
#     norm=mpl.colors.BoundaryNorm(levels, cmap2.N)
#     return cmap2


if POLE == 'N': #climatology for N Pole
  SEASON=['M03', 'M09']
  MONTH=['MAR', 'SEP']
  proj = ccrs.NorthPolarStereo()
else: #climatology for S pole
  SEASON=['M09', 'M02']
  MONTH=['SEP', 'FEB']
  proj = ccrs.SouthPolarStereo()

transform = crs=ccrs.PlateCarree()

fig, axes = plt.subplots(2, figsize=(10, 16), subplot_kw={'projection': proj})  
# fig = plt.figure(figsize=(10,16))

cmap = mpl.colormaps['Blues_r']
aice_levels = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,
                     0.8, 0.9, 0.95, 0.99])
# cmap = rescaled_cmap(aice_levels, cmap=cmap)

delta = 0.025
x = y = np.arange(-3.0, 3.01, delta)
X, Y = np.meshgrid(x, y)
Z1 = np.exp(-X**2 - Y**2)
Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
Z = (Z1 - Z2) * 2

    
i = 0
for sea,mon in zip(SEASON,MONTH):
    if (POLE=='N'):
        axes[i].set_extent([-180, 180, 29, 90], crs=ccrs.PlateCarree())
        xticks = np.arange(-180, 181, 30)
        yticks = np.arange(30, 90, 30)
        gl = axes[i].gridlines(draw_labels=True, dms=True,x_inline=False, y_inline=False, crs=ccrs.PlateCarree(), 
            linewidth=0.5, color='white', alpha=0.5)
        gl.ylocator = mticker.FixedLocator(yticks)
        gl.xlocator = mticker.FixedLocator(xticks)
        gl.xlabel_style = {'rotation':0}
        gl.ylabel_style = {'rotation':0}

    if  (POLE=='S'):
        ax[i].set_extent([-180, 180, -29, -90], crs=ccrs.PlateCarree())
        xticks = np.arange(-180, 181, 30)
        yticks = np.arange(-30, -90, -30)
        gl = axes[i].gridlines(draw_labels=True, x_inline=False, y_inline=False, crs=ccrs.PlateCarree(), 
            linewidth=0.5, color='white', alpha=0.5)
        gl.ylocator = mticker.FixedLocator(yticks)
        gl.xlocator = mticker.FixedLocator(xticks)
        gl.xlabel_style = {'rotation':0}
        gl.ylabel_style = {'rotation':0}
        
    
    CS = axes[i].contourf(X, Y, Z, aice_levels,cmap=cmap,extend='max')
    
    axes[i].add_feature(cfeature.OCEAN)
    # ax.add_feature(ice_shelves, facecolor='darkgrey')
    axes[i].add_feature(cfeature.LAND, facecolor='grey')
    axes[i].add_feature(cfeature.COASTLINE)

    title=mon 
    axes[i].set_title(title,fontsize=16)
    plt.draw()
    for ea in gl.left_label_artists:
        ea.set_visible(True)
    for ea in gl.right_label_artists:
        ea.set_visible(False)
    i += 1

cbar = fig.colorbar(CS,ax=axes.ravel().tolist())
cbar.set_ticks(list(aice_levels))

-------------------------------------------------------------------------------------------------------------------------------
 
from netCDF4 import Dataset,num2date,date2num
import numpy as np
import numpy.ma as ma
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as mticker
import xarray as xr
import cartopy
# print(cartopy.__version__)
from cartopy import crs as ccrs, feature as cfeature
import warnings
warnings.filterwarnings('ignore')
import glob
import struct
import datetime
import time
import sys
import os
import re

POLE = 'N'
if POLE == 'N': #climatology for N Pole
  SEASON=['M03', 'M09']
  MONTH=['MAR', 'SEP']
  proj = ccrs.NorthPolarStereo()
else: #climatology for S pole
  SEASON=['M09', 'M02']
  MONTH=['SEP', 'FEB']
  proj = ccrs.SouthPolarStereo()

transform = crs=ccrs.PlateCarree()

ice_shelves = cfeature.NaturalEarthFeature(
        category='physical',
        name='antarctic_ice_shelves_polys',
        scale='10m')

# ice_shelves_lines = cfeature.NaturalEarthFeature(
#         category='physical',
#         name='antarctic_ice_shelves_lines',
#         scale='10m')

land = cfeature.NaturalEarthFeature(
        category='physical',
        name='land',
        scale='10m')

fig, axes = plt.subplots(2, figsize=(10, 16), subplot_kw={'projection': proj})  
# fig = plt.figure(figsize=(10,16))

cmap = mpl.colormaps['Blues_r']
aice_levels = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7,
                     0.8, 0.9, 0.95, 0.99])
# cmap = rescaled_cmap(aice_levels, cmap=cmap)

delta = 0.025
x = y = np.arange(-3.0, 3.01, delta)
X, Y = np.meshgrid(x, y)
Z1 = np.exp(-X**2 - Y**2)
Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
Z = (Z1 - Z2) * 2

i = 0
for sea,mon in zip(SEASON,MONTH):
    if (POLE=='N'):
        axes[i].set_extent([-180, 180, 45.5, 90], crs=ccrs.PlateCarree())
        gl = axes[i].gridlines(crs=ccrs.PlateCarree(), draw_labels=True, y_inline=False,
                  xlocs=range(-180,181,30), ylocs=range(-180,181,30), rotate_labels=False,
                  linewidth=0.5, color='white', alpha=0.5)
        
        plt.draw()
        for ea in gl.left_label_artists:
            ea.set_visible(True)
        for ea in gl.right_label_artists:
            ea.set_visible(False)
        
        axes[i].add_feature(cfeature.LAND, facecolor='lightgrey',edgecolor='k')
        

    if  (POLE=='S'):
        axes[i].set_extent([-180, 180, -45.5, -90], crs=ccrs.PlateCarree())
        gl = axes[i].gridlines(crs=ccrs.PlateCarree(), draw_labels=True, y_inline=False,
                  xlocs=range(-180,181,30), ylocs=range(-180,181,30), rotate_labels=False,
                  linewidth=0.5, color='white', alpha=0.5)
        
        plt.draw()
        for ea in gl.left_label_artists:
            ea.set_visible(True)
        for ea in gl.right_label_artists:
            ea.set_visible(False)
        
        axes[i].add_feature(cfeature.LAND, facecolor='lightgrey')
        axes[i].add_feature(land,facecolor='lightgrey')
        axes[i].add_feature(ice_shelves, facecolor='lightgrey')
        axes[i].add_feature(cfeature.COASTLINE)
        
    # axes[i].add_feature(cfeature.OCEAN)
    CS = axes[i].contourf(X, Y, Z, aice_levels,cmap=cmap,extend='max')

    title=mon 
    axes[i].set_title(title,fontsize=16)
    i += 1

cbar = fig.colorbar(CS,ax=axes.ravel().tolist())
cbar.set_ticks(list(aice_levels))
