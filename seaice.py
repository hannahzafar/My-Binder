import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy
from cartopy import crs as ccrs, feature as cfeature


POLE = 'N'

transform = crs=ccrs.PlateCarree()
if POLE == 'N': #climatology for N Pole
  SEASON=['M03', 'M09']
  MONTH=['MAR', 'SEP']
  proj = ccrs.NorthPolarStereo()
  
else: #climatology for S pole
  SEASON=['M09', 'M02']
  MONTH=['SEP', 'FEB']
  proj = ccrs.SouthPolarStereo()


fig, axes = plt.subplots(2,3, figsize=(16, 10), subplot_kw={'projection': proj})


for i, ax in enumerate(fig.axes):
  gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, y_inline=False,
          xlocs=range(-180,181,30), ylocs=range(-180,181,30), rotate_labels=False,
          linewidth=0.5, color='white', alpha=0.5)
  gl.right_labels=False
  gl.left_labels=True
  for ea in gl.left_label_artists:
    ea.set_visible(True)
  if (POLE=='N'):
    ax.set_extent([-180, 180, 45.5, 90], crs=ccrs.PlateCarree())
    # ax.add_feature(cfeature.LAND, facecolor='lightgrey')
  else:
    ax.set_extent([-180, 180, -45.5, -90], crs=ccrs.PlateCarree())
    # ax.add_feature(cfeature.LAND, facecolor='lightgrey',edgecolor='k')
plt.show()
