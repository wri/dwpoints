""" CONSTANTS
"""
#
# DEFAULT CONFIG
#
LON_COLUMN='lon'
LAT_COLUMN='lat'
SQUASH_KEYS=[
    'dw_mode',
    'dw_median_label',
    'dw_monthly_median_label_mode',
    'dw_median_cr'
]
NOISY=True
MIN_CROP=2
MIN_CROPISH=11
YEAR=2022

#
# PRINT STRINGS
#


#
# PATHS
#
DWPTS_CONFIG_PATH='dwpts-config.json'
BAK_CONFIG_PATH='{}.bak'.format(DWPTS_CONFIG_PATH)


#
# STRING TEMPLATES
#



#
# JSON TEMPLATES
#
CONFIG_DICT={
    "year": YEAR,
    "lon": LON_COLUMN,
    "lat": LAT_COLUMN,
    "squash_keys": SQUASH_KEYS,
    "min_crop": MIN_CROP,
    "min_cropish": MIN_CROPISH,
    "noisy": NOISY
}


#
# NOT CONFIGURABLE
#
DWPTS_CONFIG_EXISTS='DWPTS: config file exists. use `force=True` to overite'
CRS='epsg:4326'
SCALE=10
MAX_PIX=9*4
CROP_VALUE=4
CLASSES=[
    "water", 
    "trees", 
    "grass", 
    "flooded_vegetation", 
    "crops",
    "shrub_and_scrub", 
    "built", 
    "bare", 
    "snow_and_ice"
]
