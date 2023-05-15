""" dwpoints.labels

Public Method: `annual_dw` returns a dictionary of different dynamic world annual-labels 

Edit this file to add new labels layers.  

"""
import ee
import dwpoints.constants as c
ee.Initialize()


#
# DATA
#
DW=ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1")
NO_SNOW_IM=ee.Dictionary({
  'water': 1,
  'trees': 1,
  'grass': 1,
  'flooded_vegetation': 1,
  'crops': 1,
  'shrub_and_scrub': 1,
  'built': 1,
  'bare': 1,
  'snow_and_ice': 0
}).toImage(c.CLASSES)

#
# METHODS
#
def probabilites_to_class(probs):
  return ee.Image(probs).toArray().arrayArgmax().arrayGet([0]).rename(['label'])


def month_lulc(year,month,rtype):
  start=ee.Date.fromYMD(year,ee.Number(month),1)
  end=start.advance(1,'month')
  dw=DW.filterDate(start,end)
  if (rtype=='mean'):
    probs=dw.select(c.CLASSES).mean()
  elif (rtype=='median'):
    probs=dw.select(c.CLASSES).median()
  lulc=probabilites_to_class(probs)
  return lulc 


def monthly_mean_lulc(year,month):
  return month_lulc(year,month,'mean')


def monthly_median_lulc(year,month):
  return month_lulc(year,month,'median')


def is_crop(label):
  label=ee.Image(label)
  return label.eq(c.CROP_VALUE)


def is_snow(label):
  label=ee.Image(label)
  return label.eq(c.SNOW_VALUE)

def is_builtup(label):
  label=ee.Image(label)
  return label.eq(c.BUILTUP_VALUE)


def is_cropish(label):
  label=ee.Image(label)
  return is_crop(label).Or(label.eq(2).Or(label.eq(5).Or(label.eq(7))))


def crop_rule(monthly_ic,label,min_crop,min_cropish):
  monthly_ic=ee.ImageCollection(monthly_ic)
  crop_count=ee.Image(monthly_ic.map(is_crop).reduce(ee.Reducer.sum())).rename(['crop_count'])
  cropish_count=ee.Image(monthly_ic.map(is_cropish).reduce(ee.Reducer.sum())).rename(['cropish_count'])
  crop_pixels=crop_count.gte(min_crop).And(cropish_count.gte(min_cropish)).multiply(c.CROP_VALUE).selfMask().rename(['label'])
  return ee.Image(label).where(crop_pixels,crop_pixels)


def snow_rule(monthly_ic,probs,min_snow):
  monthly_ic=ee.ImageCollection(monthly_ic)
  label=probabilites_to_class(ee.Image(probs).multiply(NO_SNOW_IM))
  snow_count=ee.Image(monthly_ic.map(is_snow).reduce(ee.Reducer.sum())).rename(['snow_count'])
  snow_pixels=snow_count.gt(min_snow).multiply(c.SNOW_VALUE)
  return ee.Image(label).where(snow_pixels,snow_pixels)


def bu_rule(monthly_ic,label,nb_builtup):
  monthly_ic=ee.ImageCollection(monthly_ic)
  bu_count=ee.Image(monthly_ic.map(is_builtup).reduce(ee.Reducer.sum())).rename(['bu_count'])
  bu_pixels=bu_count.gte(nb_builtup).multiply(c.BUILTUP_VALUE)
  return ee.Image(label).where(bu_pixels,bu_pixels)


#
# PUBLIC
#
def aggregate_dw(year=None,month=None,day=c.DAY,duration=c.DURATION,duration_type=c.DURATION_TYPE,start_date=None):
    if start_date:
        start_date=ee.Date(start_date)
    else:
        start_date=ee.Date.fromYMD(year,month,day)
    end_date=start_date.advance(duration,duration_type)
    dw=DW.filterDate(start_date,end_date).select(c.CLASSES)
    dw_mean_label=probabilites_to_class(dw.mean())
    dw_median_label=probabilites_to_class(dw.median())
    return {
        'dw_mean_label': dw_mean_label,
        'dw_median_label': dw_median_label }


def annual_dw(year,min_crop=c.MIN_CROP,min_cropish=c.MIN_CROPISH,min_snow=c.MIN_SNOW,nb_builtup=c.NB_BUILTUP):
    start_date=ee.Date.fromYMD(year,1,1)
    # MONTHLY ICS
    dw_monthly_mean_labels=ee.ImageCollection(ee.List.sequence(1,12).map(lambda m: monthly_mean_lulc(year,m)))
    dw_monthly_median_labels=ee.ImageCollection(ee.List.sequence(1,12).map(lambda m: monthly_median_lulc(year,m)))
    # ANNUAL SQUASHES
    dw=DW.filterDate(start_date,start_date.advance(1,'year'))
    dw_mean=dw.select(c.CLASSES).mean()
    dw_median=dw.select(c.CLASSES).median()
    dw_mode=dw.select('label').mode()
    dw_mean_label=probabilites_to_class(dw_mean)
    dw_median_label=probabilites_to_class(dw_median)
    dw_monthly_mean_label_mode=dw_monthly_mean_labels.mode()
    dw_monthly_median_label_mode=dw_monthly_median_labels.mode()
    dw_median_cr=crop_rule(dw_monthly_median_labels,dw_median_label,min_crop,min_cropish)
    dw_mean_cr=crop_rule(dw_monthly_mean_labels,dw_mean_label,min_crop,min_cropish)
    # example of snow/br/cr_rule
    dw_median_sr=snow_rule(dw_monthly_median_labels,dw_median,min_snow)
    dw_median_sr_cr=crop_rule(dw_monthly_median_labels,dw_median_sr,min_crop,min_cropish)
    dw_median_sr_cr_br=bu_rule(dw_monthly_median_labels,dw_median_sr_cr,nb_builtup)
    return {
        'dw_mode': dw_mode,
        'dw_mean_label': dw_mean_label,
        'dw_median_label': dw_median_label,
        'dw_monthly_mean_label_mode': dw_monthly_mean_label_mode,
        'dw_monthly_median_label_mode': dw_monthly_median_label_mode,
        'dw_median_cr': dw_median_cr,
        'dw_mean_cr': dw_mean_cr,
        'dw_median_sr': dw_median_sr,
        'dw_median_sr_cr': dw_median_sr_cr,
        'dw_median_sr_cr_br': dw_median_sr_cr_br
      }
