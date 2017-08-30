from datetime import date
import os
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import numpy as np

def map_maker(data, date_needed, llat=20, llon=180, ulat=90, ulon=320., vmin=-60, vmax=60, colorbar=True):
    try:
        year, month, day = date_needed.split('-')
        year, month, day = int(year), int(month), int(day)
        d0 = date(1948, 1, 1)
        d1 = date(year, month, day)
        delta = d1 - d0
        if delta.days < 0:
            raise KeyboardInterrupt, 'date before start of data'
        day = delta.days
    except:
        raise KeyboardInterrupt, 'needs to be YYYY-MM-DD'

    if data == 'v-wind':
        filename = os.path.join('working_data/vwind.IGS.77to17.nc')
        fh = Dataset(filename)
        vwind = fh.variables['vwnd'][day]
        tmax_units = fh.variables['vwnd'].units

    elif data == 'u-wind':
        filename = os.path.join('working_data/uwind.IGS.77to17.nc')
        fh = Dataset(filename)
        vwind = fh.variables['uwnd'][day] # day from 01-01-1977
        tmax_units = fh.variables['uwnd'].units

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
