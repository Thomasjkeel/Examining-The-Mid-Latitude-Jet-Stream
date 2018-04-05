# {
#     "url"   : "https://api.ecmwf.int/v1",
#     "key"   : "XXXXXXXXXXXXXXXXXXXXXXXXX", # unique API key
#     "email" : "XXXXXXXXXXXXXXXXXXXXXXXXX" # email address
# }
# Note: above text should be stored in usr/.ecmwfapirc

#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer
server = ECMWFDataServer()
server.retrieve({
                "dataset": "interim",
#                "date": "1979-01-01/to/2017-10-31", # Time period YYYY-MM-DD
                "date": "1979-12-21/to/2017-10-31", # Retreve data for the study period (21st 1979)
                "expver": "1",
                "levtype": "pl",   # sfc = surface; pl = pressure levels
                "levelist": "150/175/200/225/250/300/350/400/450/500", # all the pressure_levels needed (10 levels between (150-500 hPa))
                "param": "v", # Retrieves v-component Note: For Parameters.. See the ECMWF parameter database, at http://apps.ecmwf.int/codes/grib/param-db
                "stream": "oper",
                "type": "an",
                "time": "00:00:00", # time-step 00:00
                "step": "0",
                "area": "80/-180/20/-20",    # North America study region
                "grid": "1.0/1.0",  # 1.0 longitude by 1.0 latitude
                "format": "netcdf",    # Convert the output file from the default GRIB format to NetCDF format. Requires "grid" to be set to a regular lat/lon grid.
                "target": "data/IGSData_vwind.nc",    # The output file name. Set this to whatever you like.
                })
