# R script to calculate the area of each of the ten study regions

require(raster)

# Makes grid of cells for study area
r = raster()
a <- area(r)
lat <- yFromRow(r, 10:70)

# Areas needed
Alaska = sum(a[150:162, 180:254])
Arctic_seas = sum(a[163:169, 180:249])
Atl = sum(a[110:139,300:339])
CAM = sum(a[110:118,242:269])
CNA = sum(a[119:139,255:274])
ENA = sum(a[115:139,275:299])
N_pac = sum(a[130:149, 180:229])
S_pac = sum(a[110:129,180:229])
WestCanGre = sum(a[140:169,255:339])
WNA = sum(a[119:149,230:254])

# Gets slice of longitudinal cells in kilometres
# from 80 N to 20 N
area <- a[10:70,1]
write.csv(area, file = 'path/to/Desktop/area.csv')
