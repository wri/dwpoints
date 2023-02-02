""" dwpoints.squash

Public Method: `annual_dw` returns a dictionary of different dynamic world annual-squashes 

Edit this file to add new squash layers.  

"""
import ee
import dwpoints.constants as c
ee.Initialize()


#
# DATA
#
DW=ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1")


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


def is_cropish(label):
  label=ee.Image(label)
  return is_crop(label).Or(label.eq(2).Or(label.eq(5).Or(label.eq(7))))


def crop_rule(monthly_ic,label):
  monthly_ic=ee.ImageCollection(monthly_ic)
  crop_count=ee.Image(monthly_ic.map(is_crop).reduce(ee.Reducer.sum())).rename(['crop_count'])
  cropish_count=ee.Image(monthly_ic.map(is_cropish).reduce(ee.Reducer.sum())).rename(['cropish_count'])
  crop_im=crop_count.gte(c.MIN_CROP).And(cropish_count.gte(c.MIN_CROPISH)).multiply(c.CROP_VALUE).selfMask().rename(['label'])
  print('WARNING:TODO: DONT USE CONFIG FOR MIN_CROP/ISH')
  return ee.Image(label).where(crop_im,crop_im)


#
# PUBLIC
#
def annual_dw(year):
    start_date=ee.Date.fromYMD(year,1,1)
    # MONTHLY ICS
    dw_monthly_mean_labels=ee.ImageCollection(ee.List.sequence(1,12).map(lambda m: monthly_mean_lulc(year,m)))
    dw_monthly_median_labels=ee.ImageCollection(ee.List.sequence(1,12).map(lambda m: monthly_median_lulc(year,m)))
    # ANNUAL SQUASHES
    dw=DW.filterDate(start_date,start_date.advance(1,'year'))
    dw_mode=dw.select('label').mode()
    dw_mean_label=probabilites_to_class(dw.select(c.CLASSES).mean())
    dw_median_label=probabilites_to_class(dw.select(c.CLASSES).median())
    dw_monthly_mean_label_mode=dw_monthly_mean_labels.mode()
    dw_monthly_median_label_mode=dw_monthly_median_labels.mode()
    dw_median_cr=crop_rule(dw_monthly_median_label_mode,dw_median_label)
    dw_mean_cr=crop_rule(dw_monthly_mean_label_mode,dw_mean_label)
    return {
        'dw_mode': dw_mode,
        'dw_mean_label': dw_mean_label,
        'dw_median_label': dw_median_label,
        'dw_monthly_mean_label_mode': dw_monthly_mean_label_mode,
        'dw_monthly_median_label_mode': dw_monthly_median_label_mode,
        'dw_median_cr': dw_median_cr,
        'dw_mean_cr': dw_mean_cr }
