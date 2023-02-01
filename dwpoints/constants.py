""" CONSTANTS
"""
#
# DEFAULT CONFIG
#
LON_COLUMN='lon'
LAT_COLUMN='lat'
SQUASH_KEYS=[]
NOISY=True

#
# PRINT STRINGS
#
AVAILABLE_REMOTES="AVAILABLE REMOTES:"
INITIAL_CONFIG="on"
NOT_ON="disabled"
OFF="off"


#
# PATHS
#
CONFIG_PATH='dwpts-config.json'
BAK_CONFIG_PATH='{}.bak'.format(CONFIG_PATH)


#
# STRING TEMPLATES
#



#
# JSON TEMPLATES
#
CONFIG_DICT={
    "lon": LON_COLUMN,
    "lat": LAT_COLUMN,
    "squash_keys": SQUASH_KEYS,
    "noisy": NOISY
}




