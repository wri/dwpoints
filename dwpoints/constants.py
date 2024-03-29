""" CONSTANTS
"""
#
# DEFAULT CONFIG
#
LON_COLUMN='lon'
LAT_COLUMN='lat'
SQUASH_KEYS=[
    # requesting too many squash-keys leads to error: "Request payload size exceeds the limit: 10485760 bytes"
    'dw_median_label',
    'dw_median_cr',
    'dw_median_sr_cr_br'
]
AGGREGATE_SQUASH_KEYS=[
    'dw_mean_label',
    'dw_median_label'
]
NOISY=True
MIN_CROP=2
MIN_CROPISH=11
MIN_SNOW=10
NB_BUILTUP=6
YEAR=2022
DEST_PREFIX='dwpoints'
ACCURACY_DEST_PREFIX='acc'
CONFUSION_DEST_PREFIX='cm'
NORMALIZE_CM=False
MONTH=1
DAY=1
DURATION=1
DURATION_TYPE='month'
#
# PATHS
#
DWPOINTS_CONFIG_PATH='dwpoints-config.yaml'
BAK_CONFIG_PATH='{}.bak'.format(DWPOINTS_CONFIG_PATH)

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
    "min_snow": MIN_SNOW,
    "nb_builtup": NB_BUILTUP,
    "noisy": NOISY,
    "prefix": DEST_PREFIX,
    "normalize": NORMALIZE_CM,
    "acc_prefix": ACCURACY_DEST_PREFIX,
    "cm_prefix": CONFUSION_DEST_PREFIX,
    "month": MONTH,
    "day": DAY,
    "duration": DURATION,
    "duration_type": DURATION_TYPE,
    "aggregate_squash_keys": AGGREGATE_SQUASH_KEYS
}


#
# NOT CONFIGURABLE
#
LABEL_VALUES=range(9)
DUMMY_PREFIX='DW'
CRS='epsg:4326'
SCALE=10
MAX_PIX=9*4
CROP_VALUE=4
BUILTUP_VALUE=6
SNOW_VALUE=8
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


#
# COMMENT STRINGS
#
DWPOINTS_CONFIG_COMMENT="dwpoints: config"
DWPOINTS_CONFIG_EXISTS="dwpoints-config.yaml exists.  use force=True to overwrite."
DWPOINTS_CONFIG_CREATED="dwpoints-config.yaml created. edit file to change configuration"

