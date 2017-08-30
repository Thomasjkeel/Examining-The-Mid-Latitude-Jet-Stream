from datetime import date
import os
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import numpy as np
from subset import subset_nc


def map_maker(data, date_needed, level, llat=20, llon=180, ulat=90, ulon=320, vmin=-60, vmax=60, colorbar=True):
    subset = subset_nc(filename=data, startdate=date_needed, enddate=date_needed, level=300, lat_min=llat, lon_min=llon,
     lat_max=ulat, lon_max=ulon)
    iris.io.save(subset,'delete_this.nc')
    fh = Dataset('delete_this.nc')
    os.remove('delete_this.nc')
    try:
        vwind = fh.variables['vwnd']
        tmax_units = fh.variables['vwnd'].units
    except:
        vwind = fh.variables['vwnd']
        tmax_units = fh.variables['vwnd'].units


    lons = fh.variables['lon'][:]
    lats = fh.variables['lat'][:]
    lon_0 = lons.mean()
    lat_0 = lats.mean()

    m=Basemap(projection='cyl', llcrnrlon=llon, \
      urcrnrlon=ulon, llcrnrlat=llat,urcrnrlat=ulat, \
        resolution='c')
    lon, lat = np.meshgrid(lons, lats)
    xi, yi = m(lon, lat)
    cs = m.pcolor(xi,yi,np.squeeze(vwind), cmap='RdBu_r', vmin=vmin, vmax=vmax) # change vmax

    # Add Grid Lines
    m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=8)
    m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=8)
    m.drawcoastlines()
    if colorbar == True:
        cbar = m.colorbar(cs, location='bottom', pad="10%")
        cbar.set_label(tmax_units)

    return m
