import iris
import numpy as np
import pandas as pd
import math
from subset import subset_nc


def wind_direction_df(startdate, enddate, lon, lat, level, vwnd_file, uwnd_file, level2=None, 
                     csv_name=None, pickle_name=None, s=True, ret=False):

    vwnd_lst = []
    uwnd_lst = []
    date_lst = []
    card_dir = []
    wind_dir_to = []
    wind_dir_from = []
    lon = int(lon)
    lat = int(lat)

    iris.FUTURE.cell_datetime_objects = False

    try:
        vwind = subset_nc(filename=vwnd_file, startdate=startdate, enddate=enddate,
         level=level,level2=level2, lat_min=lat, lat_max=lat, lon_min=lon, lon_max=lon)
    except:
        raise KeyboardInterrupt, 'need path to v-wind netcdf4 file OR try setting iris.FUTURE.cell_datetime_objects to False'

    try:
        uwind = subset_nc(filename=uwnd_file,startdate=startdate, enddate=enddate,
         level=level, level2=level2, lat_min=lat, lat_max=lat, lon_min=lon, lon_max=lon)
    except:
        raise KeyboardInterrupt, 'need path to u-wind netcdf4 file'


    time_c = vwind.coord('time')

    for i in range(len(vwind.coord('time').points)):
        iris.FUTURE.cell_datetime_objects = True
        v_df = vwind.data[i]
        vwnd_lst.append(v_df)

        u_df = uwind.data[i]
        uwnd_lst.append(u_df)

        b = str(time_c.cell(i))[:10] # removes 00:00:00 from dates
        date_lst.append(b)

    vws = pd.DataFrame(vwnd_lst,columns=['mean v-wind (m/s)'])
    uws = pd.DataFrame(uwnd_lst,columns=['mean u-wind (m/s)'])
    dates = pd.DataFrame(date_lst,columns=['date'])

    df = vws.join(uws)
    df = df.join(dates)

    for i in range(0, len(df)):
        u_ms = df['mean u-wind (m/s)'][i]
        v_ms = df['mean v-wind (m/s)'][i]
        wind_abs = np.sqrt(u_ms**2 + v_ms**2)
        wind_dir_trig_to = math.atan2(u_ms/wind_abs, v_ms/wind_abs)
        wind_dir_trig_to_degrees = wind_dir_trig_to * 180/math.pi
        wind_dir_trig_from_degrees = wind_dir_trig_to_degrees + 180
        wind_dir_cardinal = 90 - wind_dir_trig_from_degrees
        wind_dir_from.append(wind_dir_trig_from_degrees)
        wind_dir_to.append(wind_dir_trig_to_degrees)

    wd_f = pd.DataFrame(wind_dir_from, columns=['wind direction from (deg)'])
    wd_t = pd.DataFrame(wind_dir_to, columns=['wind direction to (deg)'])

    df = df.join(wd_f)
    df = df.join(wd_t)

    for i in range(0, len(df)):
        if df['wind direction from (deg)'][i] >= 348.75 or df['wind direction from (deg)'][i] < 11.25:
            direction = 'N'
            card_dir.append(direction)
        elif df['wind direction from (deg)'][i] >= 11.25 and df['wind direction from (deg)'][i] < 33.75:
            direction = 'NNE'
            card_dir.append(direction)
        elif df['wind direction from (deg)'][i] >= 33.75 and df['wind direction from (deg)'][i] < 56.25:
            direction = 'NE'
            card_dir.append(direction)
        elif df['wind direction from (deg)'][i] >= 56.25 and df['wind direction from (deg)'][i] < 78.75:
            direction = 'ENE'
            card_dir.append(direction)
        elif df['wind direction from (deg)'][i] >= 78.75 and df['wind direction from (deg)'][i] < 101.25:
            direction = 'E'
            card_dir.append(direction)
        elif df['wind direction from (deg)'][i] >= 101.25 and df['wind direction from (deg)'][i] < 123.75:
            direction = 'ESE'
            card_dir.append(direction)
        elif df['wind direction from (deg)'][i] >= 123.75 and df['wind direction from (deg)'][i] < 146.25:
            direction = 'SE'
            card_dir.append(direction)
        elif df['wind direction from (deg)'][i] >= 146.25 and df['wind direction from (deg)'][i] < 168.75:
            direction = 'SSE'
            card_dir.append(direction)
        elif df['wind direction from (deg)'][i] >= 168.75 and df['wind direction from (deg)'][i] < 191.25:
            direction = 'S'
            card_dir.append(direction)
        elif df['wind direction from (deg)'][i] >= 191.25 and df['wind direction from (deg)'][i] < 213.75:
            direction = 'SSW'
            card_dir.append(direction)
        elif df['wind direction from (deg)'][i] >= 213.75 and df['wind direction from (deg)'][i] < 236.25:
            direction = 'SW'
            card_dir.append(direction)
        elif df['wind direction from (deg)'][i] >= 236.25 and df['wind direction from (deg)'][i] < 258.75:
            direction = 'WSW'
            card_dir.append(direction)
        elif df['wind direction from (deg)'][i] >= 258.75 and df['wind direction from (deg)'][i] < 281.25:
            direction = 'W'
            card_dir.append(direction)
        elif df['wind direction from (deg)'][i] >= 281.25 and df['wind direction from (deg)'][i] < 303.75:
            direction = 'WNW'
            card_dir.append(direction)
        elif df['wind direction from (deg)'][i] >= 303.75 and df['wind direction from (deg)'][i] < 326.25:
            direction = 'NW'
            card_dir.append(direction)
        elif df['wind direction from (deg)'][i] >= 326.25 and df['wind direction from (deg)'][i] < 348.75:
            direction = 'NNW'
            card_dir.append(direction)

    c_d= pd.DataFrame(card_dir, columns=['cardinal direction'])
    df = df.join(c_d)
    df['wind speed in direction'] = np.sqrt(df['mean u-wind (m/s)']**2 + df['mean v-wind (m/s)']**2)


    df.index = df["date"]
    del df['date']

    firstDate = df.index[0]
    lastDate = df.index[len(df['mean u-wind (m/s)'])-1]
    df = df.reindex(index=pd.date_range(start = firstDate, end = lastDate), fill_value = None)

    if s == True:
        if csv_name != None:
            for char in csv_name:
                if char in '.csv':
                    csv_name = csv_name.replace(char,'')
                else:
                    pass
            df.to_csv('{0}.csv'.format(csv_name))

        else:
            print('No csv_name given')

        if pickle_name != None:
            for char in pickle_name:
                if char in '.pkl':
                    pickle_name = pickle_name.replace(char,'')
                else:
                    pass
            df.to_pickle('{0}.pkl'.format(pickle_name))
        else:
            print('No pickle_name given')

    if ret == True:
        return df

    else:
        print('done!')
