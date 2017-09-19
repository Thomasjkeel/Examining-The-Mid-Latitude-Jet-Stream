import iris
import datetime
from dateutil.relativedelta import relativedelta

iris.FUTURE.netcdf_promote = True
iris.FUTURE.cell_datetime_objects=False


def time_value(date, cube):
    """function that takes a string of date (YYYY-MM-DD) and returns it in correct format, derived from the data"""
    try:
        time_units = cube.coord('time').units
    except:
        raise KeyboardInterrupt, 'cube has no coord time'
    try:
        year, month, day = date.split('-')
        year, month, day = int(year), int(month), int(day)
        val = time_units.date2num(datetime.datetime(year, month, day))
    except:
        raise KeyboardInterrupt, 'format of date needs to be: \"YYYY-MM-DD\"'

    return val



def subset_nc(filename, startdate, enddate, level=300, lat_min=20, lat_max=90, lon_min=180, lon_max=340):

    """A function to subnet the netCDF4 file (.nc) which can be adjusted to extract
     only the bits you need when making your dataframe"""

    try:
        cubes = iris.load(filename)
        if len(cubes) == 1:
            subset = cubes[0]
        else:
            subset = cubes[1]
    except:
        raise KeyboardInterrupt, 'need path to v-wind netcdf4 file'

    try:
        year, month, day = startdate.split('-')
        year, month, day = int(year), int(month), int(day)
        time_units = subset.coord('time').units
        s_val = time_units.date2num(datetime.datetime(year, month, day))
    except:
        raise KeyboardInterrupt, 'startdate needs to be in format: YYYY-MM-DD'

    try:
        year, month, day = enddate.split('-')
        year, month, day = int(year), int(month), int(day)+1 # add one it includes the last day
        e_val = time_units.date2num(datetime.datetime(year, month, day))
    except:
        raise KeyboardInterrupt, 'enddate needs to be in format: YYYY-MM-DD'

    try:
        subset = subset.extract(
                                        iris.Constraint(latitude=lambda cell: lat_min <= cell < lat_max+1,
                                        longitude=lambda cell: lon_min <= cell < lon_max+1,
                                        Level=lambda cell: level <= cell < level+1,
                                                    time=lambda cell: int(s_val) <= cell < int(e_val)))
    except:
        raise KeyboardInterrupt, 'variables out of range of the data\'s dimensions OR try setting iris.FUTURE.cell_datetime_objects to False'

    return subset
