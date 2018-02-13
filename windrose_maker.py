from makerlib import wind_direction_df
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import numpy as np
import matplotlib.cm as cm

def windrose_maker(vwnd_file, uwnd_file, startdate, enddate, level, lon, lat, level2=None, title=None, filename=None, yticks=None, to_return=True): # save=False
    try:
        df = wind_direction_df(vwnd_file=vwnd_file, uwnd_file=uwnd_file, startdate=startdate, enddate=enddate,
         level=level, level2=level2, lat=lat, lon=lon, s=False, ret=True)

    except:
        raise KeyboardInterrupt, 'dataframe maker has failed'

    df.name = title
    df.filename = filename
    plt.rcParams['axes.titlepad'] = 20
    ax = WindroseAxes.from_ax()
    ax.contourf(df['wind direction from (deg)'], df['wind speed in direction'], bins=np.arange(0, 90, 10), cmap=cm.hot)
    ax.set_legend()
    ax.legend(loc=6, bbox_to_anchor=(1.0,0.2), title = 'm/s')
    if title != None:
        ax.set_title(df.name, size = 16)

    if yticks != None:
        ax.set_yticks(np.array(yticks));# six labels on original
        # ax.set_yticklabels(['200 (n)', '400 (n)', '600 (n)', '800 (n)', '1000 (n)'])

    # if save == True:
    #     plt.savefig(os.path.join('figures','{0}_windrose.png'.format(df.filename)), bbox_inches='tight')
    #     plt.close()
    if to_return == True:
        return ax

    else:
        print('done!, not returned')
