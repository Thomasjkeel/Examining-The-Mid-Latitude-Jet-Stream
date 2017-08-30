def time_series_maker(vwnd_file, uwnd_file, startdate, enddate, lon, lat, variable, myWindow=24, running_mean=False):
    try:
        df = wind_direction_df(vwnd_file=vwnd_file, uwnd_file=uwnd_file, startdate=startdate, enddate=enddate,
         level=level, lat=lat, lon=lon, s=False, ret=True)
    except:
        raise KeyboardInterrupt, 'df maker failed'

    if running_mean == True:
        try:
            fig = df[variable].plot()
            mw = df[variable].rolling(window=myWindow,center=True).mean()
            mw.plot(style='-r', label = "{0}hr Moving Window".format(myWindow))
            return fig
        except:
            raise KeyboardInterrupt, 'enter valid variable'

    else:
        try:
            fig = df[variable].plot()
            return fig
        except:
            raise KeyboardInterrupt, 'enter valid variable'

    
