import ee
import squash
from pprint import pprint
ee.Initialize()



# #
# # CONSTANTS
# #
# CLASSES=[
#     "water", 
#     "trees", 
#     "grass", 
#     "flooded_vegetation", 
#     "crops",
#     "shrub_and_scrub", 
#     "built", 
#     "bare", 
#     "snow_and_ice"
# ]
# YEAR=2022
# START_DATE=ee.Date.fromYMD(YEAR,1,1)
CRS='epsg:4326'
SCALE=10
MAX_PIX=9*4
# MIN_CROP=2
# MIN_CROPISH=11
# CROP_VALUE=4


# #
# # DATA
# #
# DW=ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1")
# DW=DW.filterDate(START_DATE,START_DATE.advance(1,'year'))


#
# METHODS
#
def print_info(**kwargs):
  pprint(ee.Dictionary(kwargs).getInfo())


# def probabilites_to_class(probs):
#   return ee.Image(probs).toArray().arrayArgmax().arrayGet([0]).rename(['label'])


# def month_lulc(month,rtype):
#   start=ee.Date.fromYMD(YEAR,ee.Number(month),1)
#   end=start.advance(1,'month')
#   dw=DW.filterDate(start,end)
#   if (rtype=='mean'):
#     probs=dw.select(CLASSES).mean()
#   elif (rtype=='median'):
#     probs=dw.select(CLASSES).median()
#   lulc=probabilites_to_class(probs)
#   return lulc 

# def monthly_mean_lulc(month):
#   return month_lulc(month,'mean')


# def monthly_median_lulc(month):
#   return month_lulc(month,'median')


# def is_crop(label):
#   label=ee.Image(label)
#   return label.eq(CROP_VALUE)


# def is_cropish(label):
#   label=ee.Image(label)
#   return is_crop(label).Or(label.eq(2).Or(label.eq(5).Or(label.eq(7))))


# def crop_rule(monthly_ic,label):
#   monthly_ic=ee.ImageCollection(monthly_ic)
#   crop_count=ee.Image(monthly_ic.map(is_crop).reduce(ee.Reducer.sum())).rename(['crop_count'])
#   cropish_count=ee.Image(monthly_ic.map(is_cropish).reduce(ee.Reducer.sum())).rename(['cropish_count'])
#   crop_im=crop_count.gte(MIN_CROP).And(cropish_count.gte(MIN_CROPISH)).multiply(CROP_VALUE).selfMask() 
#   return ee.ImageCollection([crop_im,label]).reduce(ee.Reducer.firstNonNull()).rename(['label'])


# #
# # MONTHLY ICS
# #
# dw_monthly_mean_labels=ee.ImageCollection(ee.List.sequence(1,12).map(monthly_mean_lulc))
# dw_monthly_median_labels=ee.ImageCollection(ee.List.sequence(1,12).map(monthly_median_lulc))


# #
# # ANNUAL SQUASH
# #
# dw_mode=DW.select('label').mode()
# dw_mean_label=probabilites_to_class(DW.select(CLASSES).mean())
# dw_median_label=probabilites_to_class(DW.select(CLASSES).median())
# dw_monthly_mean_label_mode=dw_monthly_mean_labels.mode()
# dw_monthly_median_label_mode=dw_monthly_median_labels.mode()
# dw_median_cr=crop_rule(dw_monthly_median_label_mode,dw_median_label)
# dw_mean_cr=crop_rule(dw_monthly_mean_label_mode,dw_mean_label)





#
# UI
#
def inspect(dw,lon,lat,is_label):
  pt=ee.Geometry.Point(lon,lat)
  sample_point=dw.reproject(crs=CRS,scale=SCALE).reduceRegion(
    reducer=ee.Reducer.firstNonNull(), 
    geometry=pt, 
    scale=SCALE, 
    crs=CRS, 
    maxPixels=MAX_PIX
  )
  if (is_label):
    return sample_point.getNumber('label')
  else:
    return sample_point.toArray(CLASSES).argmax().getNumber(0),sample_point.toArray(CLASSES)


squashes=squash.annual_dw(2022)


lon=-82.45585937500002
lat=34.87213971567944

lon=-82.915298
lat=34.816375

for k,v in squashes.items():
  print(k)
  print_info(lon=lon,lat=lat,inspect=inspect(v,lon,lat,True))






