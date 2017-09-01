# Working-with-NCEP-NCAR-in-Python
Methods that assist with reading, mapping, ploting and analysing NetCDF4 files from NOAA (NCEP/NCAR reanalysis) into python. 
The example in this repository covers the use of (u- and v- component) wind speed (at 300hPa) from the NCEP/NCAR reanalysis (1) to help indentify any change in the mid-latitude jet stream from 1948-2017 in response to the amplification of arctic temperatures relative to elsewhere on the globe in recent decades (2, 3).  

## Required packages
iris  
pandas
numpy
math
matplotlib.pyplot
datetime
os
netCDF4

#### Mapping
mpl_toolkits.basemap

#### Windrose Diagrams
windrose
matplotlib.cm


## References:
1. Kalnay, E, Kanamitsu, M., Kistler, R., Collins, W., Deaven, D., Gandin, L., Iredell, M., Saha, S., White, G., Woollen, J., Zhu, Y., Leetmaa, A., Reynolds, R., Chelliah, M, Ebisuzaki, W., Higgins, W., Janowiak, J., Mo, K. C., Ropelewski, M. C., Wang, J., Jenne, R., Joseph, D. (1996) The NCEP/NCAR reanalysis project. Bull. American Meteorological Society, 77, 437–471.
2. Francis, J. A. and Vavrus, S. J. (2012) Evidence linking Arctic amplification to extreme weather in mid-latitudes. Geophysical Research Letters, 39, 1-6.
3. Francis, J. A. and Vavrus, S. J (2015) Evidence for a wavier jet stream in response to rapid Arctic warming. Environmental Research Letters, 10, 1-12.
