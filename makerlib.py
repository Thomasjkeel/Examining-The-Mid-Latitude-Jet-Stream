import iris
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import iris.pandas as ip
import os
from datetime import datetime, timedelta, date
import pandas as pd
import math
from windrose import WindroseAxes
import matplotlib.cm as cm

# if not os.path.isdir('csv_dataframes'):
#         os.mkdir('csv_dataframes')

# if not os.path.isdir('pickle_jars'):
#         os.mkdir('pickle_jars')

def wind_direction_df(startdate, enddate, longitude, latitude, vwnd_file, uwnd_file,
                     csv_name=None, pickle_name=None, s=True, ret=False):
#     need to add something to remove level i.e. iris.Constraint
    vwnd_lst = []
    uwnd_lst = []
    date_lst = []
    card_dir = []
    wind_dir_to = []
    wind_dir_from = []
    lon = int(longitude)
    lat = int(latitude)

    iris.FUTURE.cell_datetime_objects = True

    try:
        v_filename = os.path.join(vwnd_file)
        v_cubes = iris.load(v_filename)
    except:
        raise KeyboardInterrupt, 'need path to v-wind netcdf4 file'

    vwind = v_cubes[0]

    try:
        u_filename = os.path.join(uwnd_file)
        u_cubes = iris.load(u_filename)
    except:
        raise KeyboardInterrupt, 'need path to v-wind netcdf4 file'

    uwind = u_cubes[0]


    time_c = vwind.coord('time')

    try:
        year, month, day = startdate.split('-')
        year, month, day = int(year), int(month), int(day)
        d0 = date(1948, 1, 1)
        d1 = date(year, month, day)
        delta = d1 - d0
        if delta.days < 0:
            raise KeyboardInterrupt, 'start date before start date of data'

        start_range = delta.days

        year, month, day = enddate.split('-')
        year, month, day = int(year), int(month), int(day)
        d1 = date(year, month, day)
        delta = d1 - d0
        if delta.days < 0 or delta.days <= start_range:
            raise KeyboardInterrupt, 'end date before start of data or start date'
        end_range = delta.days+1
    except:
        raise KeyboardInterrupt, 'needs to be string in format YYYY-MM-DD'


    for i in range(start_range, end_range):
        v_df = ip.as_data_frame(vwind[int('{0}'.format(i))], copy=True)
        vwnd_lst.append(v_df[lon][lat])

        u_df = ip.as_data_frame(uwind[int('{0}'.format(i))], copy=True)
        uwnd_lst.append(u_df[lon][lat])

        b = str(time_c.cell(int('{0}'.format(i))))[:10] # removes 00:00:00 from dates
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
        try:
            for char in csv_name:
                if char in '.csv':
                    csv_name = csv_name.replace(char,'')
            else:
                pass
            df.to_csv('{0}.csv'.format(csv_name))

        except:
            print('No csv_name given')

        try:
            for char in csv_name:
                if char in '.pkl':
                    csv_name = csv_name.replace(char,'')

            else:
                pass
            df.to_pickle('{0}.pkl'.format(pickle_name))
        except:
            print('No pickle_name given')

    if ret == True:
        return df

    else:
        print('done!')


def time_series_maker(vwnd_file, uwnd_file, startdate, enddate, longitude, latitude, variable, myWindow, running_mean=False):
    vwnd_lst = []
    uwnd_lst = []
    date_lst = []
    card_dir = []
    wind_dir_to = []
    wind_dir_from = []
    lon = int(longitude)
    lat = int(latitude)


    try:
        filename = os.path.join(vwnd_file)
    except:
        raise KeyboardInterrupt, 'need path to v-wind netcdf4 file'
    cubes = iris.load(filename)
    vwind = cubes[0]

    try:
        filename2 = os.path.join(uwnd_file)
    except:
        raise KeyboardInterrupt, 'need path to v-wind netcdf4 file'
    cubes2 = iris.load(filename2)
    uwind = cubes2[0]

    iris.FUTURE.cell_datetime_objects = True
    time_c = vwind.coord('time')

    try:
        year, month, day = startdate.split('-')
        year, month, day = int(year), int(month), int(day)
        d0 = date(1977, 1, 1)
        d1 = date(year, month, day)
        delta = d1 - d0
        if delta.days < 0:
            raise KeyboardInterrupt, 'start date before start of data'
#         elif delta.days >= 0:
        start_range = delta.days

        year, month, day = enddate.split('-')
        year, month, day = int(year), int(month), int(day)
        d0 = date(1977, 1, 1)
        d1 = date(year, month, day)
        delta = d1 - d0
        if delta.days < 0 or delta.days <= start_range:
            raise KeyboardInterrupt, 'end date before start of data or start date'
#         elif delta.days >= 0:
        end_range = delta.days+1
    except:
        raise KeyboardInterrupt, 'needs to be string in format YYYY-MM-DD'


    for i in range(start_range, end_range):
        df = ip.as_data_frame(vwind[int('{0}'.format(i))], copy=True)
        vwnd_lst.append(df[lon][lat])

        df2 = ip.as_data_frame(uwind[int('{0}'.format(i))], copy=True)
        uwnd_lst.append(df2[lon][lat])

        b = str(time_c.cell(int('{0}'.format(i))))[:10]
        date_lst.append(b)

    vws = pd.DataFrame(vwnd_lst,columns=['mean v-wind (m/s)'])
    uws = pd.DataFrame(uwnd_lst,columns=['mean u-wind (m/s)'])
    dates = pd.DataFrame(date_lst,columns=['date'])

    df = vws.join(uws)
    df = df.join(dates)

    # make list of valid options i.e. wdf, winddirfrom, wdt, winddirto
    if variable == 'wind direction from' or 'wind direction to':
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

        wd1 = pd.DataFrame(wind_dir_from, columns=['wind direction from (deg)'])
        wd2 = pd.DataFrame(wind_dir_to, columns=['wind direction to (deg)'])

        df = df.join(wd1)
        df = df.join(wd2)

    if variable == 'wind speed in direction':
        df['wind speed in direction'] = np.sqrt(df['mean u-wind (m/s)']**2 + df['mean v-wind (m/s)']**2)


    df.index = df["date"]
    del df['date']

    firstDate = df.index[0]
    lastDate = df.index[len(df['mean u-wind (m/s)'])-1]
    df = df.reindex(index=pd.date_range(start = firstDate, end = lastDate), fill_value = None)

    if variable == 'v-wind':
        if running_mean == True:
            fig = df[startdate : enddate]['mean v-wind (m/s)'].plot()
            mw = df[startdate : enddate]['mean v-wind (m/s)'].rolling(window=myWindow,center=True).mean()
            mw.plot(style='-r', label = "{0}hr Moving Window".format(myWindow))
            return fig
        else:
            fig = df[startdate : enddate]['mean v-wind (m/s)'].plot()
            return fig

    elif variable == 'u-wind':
        if running_mean == True:
            fig = df[startdate : enddate]['mean u-wind (m/s)'].plot()
            mw = df[startdate : enddate]['mean u-wind (m/s)'].rolling(window=myWindow,center=True).mean()
            mw.plot(style='-r', label = "{0}hr Moving Window".format(myWindow))
            return fig

        else:
            fig = df[startdate : enddate]['mean u-wind (m/s)'].plot()
            return fig

    elif variable == 'wind direction from':
        if running_mean == True:
            fig = df[startdate : enddate]['wind direction from (deg)'].plot()
            mw = df[startdate : enddate]['wind direction from (deg)'].rolling(window=myWindow,center=True).mean()
            mw.plot(style='-r', label = "{0}hr Moving Window".format(myWindow))
            return fig

        else:
            fig = df[startdate : enddate]['wind direction from (deg)'].plot()
            return fig

    elif variable == 'wind direction to':
        if running_mean == True:
            fig = df[startdate : enddate]['wind direction to (deg)'].plot()
            mw = df[startdate : enddate]['wind direction to (deg)'].rolling(window=myWindow,center=True).mean()
            mw.plot(style='-r', label = "{0}hr Moving Window".format(myWindow))
            return fig

        else:
            fig = df[startdate : enddate]['wind direction to (deg)'].plot()
            return fig

    elif variable == 'wind speed in direction':
        if running_mean == True:
            fig = df[startdate : enddate]['wind speed in direction'].plot()
            mw = df[startdate : enddate]['wind speed in direction'].rolling(window=myWindow,center=True).mean()
            mw.plot(style='-r', label = "{0}hr Moving Window".format(myWindow))
            return fig

        else:
            fig = df[startdate : enddate]['wind speed in direction'].plot()
            return fig

    else:
        raise KeyboardInterrupt, 'enter valid variable'


def windrose_maker(startdate, enddate, longitude, latitude, title, filename=None, yticks=None, save=False, to_return=True):
    df = dataframe_maker(startdate, enddate, longitude, latitude, s=False, ret=True)

    df.name = title
    df.filename = filename
    plt.rcParams['axes.titlepad'] = 20
    ax = WindroseAxes.from_ax()
    ax.contourf(df['wind direction from (deg)'], df['wind speed in direction'], bins=np.arange(0, 90, 10), cmap=cm.hot)
    ax.set_legend()
    ax.legend(loc=6, bbox_to_anchor=(1.0,0.2), title = 'm/s')
    ax.set_title(df.name, size = 16)
    if yticks == None:
        pass
    else:
        ax.set_yticks(np.array(yticks));# six labels on original
        # ax.set_yticklabels(['200 (n)', '400 (n)', '600 (n)', '800 (n)', '1000 (n)'])
    if save == True:
        plt.savefig(os.path.join('figures','{0}_windrose.png'.format(df.filename)), bbox_inches='tight')
        plt.close()
    if to_return == True:
        return ax
