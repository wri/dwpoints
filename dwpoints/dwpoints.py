import ee
import squash
import constants as c
import utils as utils
ee.Initialize()


#
# UI
#
def inspect(dw,lon,lat,is_label):
  pt=ee.Geometry.Point(lon,lat)
  sample_point=dw.reproject(crs=c.CRS,scale=c.SCALE).reduceRegion(
    reducer=ee.Reducer.firstNonNull(), 
    geometry=pt, 
    scale=c.SCALE, 
    crs=c.CRS, 
    maxPixels=c.MAX_PIX
  )
  if (is_label):
    return sample_point.getNumber('label')
  else:
    return sample_point.toArray(c.CLASSES).argmax().getNumber(0),sample_point.toArray(c.CLASSES)


squashes=squash.annual_dw(2022)


lon=-82.45585937500002
lat=34.87213971567944

lon=-82.915298
lat=34.816375

for k,v in squashes.items():
  utils.log_info(msg=k,noisy=True,lon=lon,lat=lat,inspect=inspect(v,lon,lat,True))






