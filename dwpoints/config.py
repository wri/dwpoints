import os.path
import yaml
import utils as utils
import constants as c
from copy import deepcopy
#
# DEFALUTS 
#
_DEFAULTS=deepcopy(c.CONFIG_DICT)


#
# LOAD CONFIG
#
if os.path.exists(c.DWPTS_CONFIG_PATH):
    _CONFIG=yaml.safe_load(open(c.DWPTS_CONFIG_PATH))
else:
    _CONFIG={}


def get(key):
    """ get value
    """
    return _CONFIG.get(key,_DEFAULTS.get(key))


def generate(
        year=c.YEAR,
        lon=c.LON_COLUMN,
        lat=c.LAT_COLUMN,
        squash_keys=c.SQUASH_KEYS,
        min_crop=c.MIN_CROP,
        min_cropish=c.MIN_CROPISH,
        noisy=c.NOISY,
        force=False):
    """ generate config file
    """
    config={
        'year': year,
        'lon': lon,
        'lat': lat,
        'squash_keys': squash_keys,
        'min_crop': min_crop,
        'min_cropish': min_cropish,
        'noisy': noisy
    }
    if not force and os.path.exists(c.SUBLR_CONFIG_PATH):
        utils.log(c.DWPTS_CONFIG_EXISTS,True,level="ERROR")
    else:
        with open(c.DWPTS_CONFIG_PATH,'w+') as file:
            file.write("# {}\n".format(c.SUBLR_CONFIG_COMMENT))
            file.write(yaml.safe_dump(config, default_flow_style=False))
        utils.log(c.SUBLR_CONFIG_CREATED,noisy)


