import os.path
import yaml
import dwpoints.utils as utils
import dwpoints.constants as c
from copy import deepcopy
#
# DEFALUTS 
#
_DEFAULTS=deepcopy(c.CONFIG_DICT)


#
# LOAD CONFIG
#
if os.path.exists(c.DWPOINTS_CONFIG_PATH):
    _CONFIG=yaml.safe_load(open(c.DWPOINTS_CONFIG_PATH))
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
        min_crop=c.MIN_CROP,
        min_cropish=c.MIN_CROPISH,
        noisy=c.NOISY,
        squash=None,
        force=False):
    """ generate config file
    """
    if squash:
        squash=squash.split(',')
    else:
        squash=c.SQUASH_KEYS
    config={
        'year': year,
        'lon': lon,
        'lat': lat,
        'squash_keys': squash,
        'min_crop': min_crop,
        'min_cropish': min_cropish,
        'noisy': noisy
    }
    if not force and os.path.exists(c.DWPOINTS_CONFIG_PATH):
        utils.log(c.DWPOINTS_CONFIG_EXISTS,True,level="ERROR")
    else:
        with open(c.DWPOINTS_CONFIG_PATH,'w+') as file:
            file.write("# {}\n".format(c.DWPOINTS_CONFIG_COMMENT))
            file.write(yaml.safe_dump(config, default_flow_style=False))
        utils.log(c.DWPOINTS_CONFIG_CREATED,noisy)


