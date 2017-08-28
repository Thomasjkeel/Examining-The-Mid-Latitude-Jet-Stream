import iris

def subset_nc(filename, year):
    cubes = iris.load(filename)
    subset = cubes[1]
    print(cubes)
    wind_subset = subset.extract(
            iris.Constraint(latitude=lambda cell: 20 <= cell < 91, longitude=lambda cell: 180 <= cell < 341, \
                            Level=lambda cell: 300 <= cell < 301))
    iris.io.save(wind_subset,'vwnd.IGS.{0}.nc'.format(year))
    print(wind_subset.shape)
