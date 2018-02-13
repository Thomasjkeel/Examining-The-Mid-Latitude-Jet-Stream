import makerlib

def time_series_maker(vwnd_file, uwnd_file, startdate, enddate, level, level2, lon, lat, variable, print_vars=False, myWindow=24, running_mean=False):
    try:
        df = makerlib.wind_direction_df(vwnd_file=vwnd_file, uwnd_file=uwnd_file, startdate=startdate, enddate=enddate,
                                        level=level,level2=level2, lat=lat, lon=lon, s=False, ret=True)

    except:
        raise KeyboardInterrupt, 'dataframe maker has failed'

    if print_vars == True:
        print('valid variables: ', list(df.columns.values))
        return

    if running_mean == True:
        try:
            fig = df[variable].plot()
            mw = df[variable].rolling(window=myWindow,center=True).mean()
            mw.plot(style='-r', label = "{0}hr Moving Window".format(myWindow))
            return fig
        except:
            raise KeyboardInterrupt, 'enter valid variable from list: {0})'.format(list(df.columns.values))

    else:
        try:
            fig = df[variable].plot()
            return fig
        except:
            raise KeyboardInterrupt, 'enter valid variable from list: {0})'.format(list(df.columns.values))
