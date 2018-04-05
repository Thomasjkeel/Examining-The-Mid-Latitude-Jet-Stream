import pandas as pd
from makerlib import wind_direction_df

def westerly_count(vwnd_file, uwnd_file, startdate, enddate, level, level2, lon, lat):
    """Counts of days where wind is flowing westerly (W, WSW, WNW) which suggests that
    the mid-latitude jet-stream is not propogating vertically over this cell.
    """
    df = wind_direction_df(vwnd_file=vwnd_file, uwnd_file=uwnd_file,
                           startdate=startdate, enddate=enddate,
                           level=level, level2=level2 lon=lon, lat=lat, s=False, ret=True)

    dfW = df.loc[((df['cardinal direction'].str.startswith('W') == True))]
    dicts = {}
    jja_dicts = {}
    djf_dicts = {}
    keys = range((int(enddate[:4]))-(int(startdate[:4])))
    start_year = int(startdate[:4])

    for i in keys:
        # All
        a = '{0}-01-01'.format(start_year)
        b = '{0}-01-01'.format(start_year+1)
        values = len(dfW[a:b])
        dicts[start_year] = values
        # Summer
        c = '{0}-06-01'.format(start_year)
        d = '{0}-08-31'.format(start_year)
        jja_values = len(dfW[c:d])
        jja_dicts[start_year] = jja_values
        # Winter
        e = '{0}-12-01'.format(start_year)
        f = '{0}-02-28'.format(start_year+1) # problem that need solving: leap years and 29th February
        djf_values = len(dfW[e:f])
        djf_dicts[start_year] = djf_values

        start_year += 1

    df_year_counts = pd.DataFrame.from_dict(dicts, orient='index') # for indexing and time series\
    df_year_counts.columns = ['year_count']
    df_summer_counts = pd.DataFrame.from_dict(jja_dicts, orient='index') # for indexing and time series\
    df_summer_counts.columns = ['JJA_count']

    df_winter_counts = pd.DataFrame.from_dict(djf_dicts, orient='index') # for indexing and time series\
    df_winter_counts.columns = ['DJF_count']

    count_df = df_year_counts.join(df_summer_counts)
    count_df = count_df.join(df_winter_counts)

    return count_df
