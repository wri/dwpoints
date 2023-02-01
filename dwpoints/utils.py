import ee
from pprint import pprint
#
# HELPERS
#
def log(msg,noisy,level='INFO',**kwargs):
    if noisy:
        print(f"[{level}] DW_POINTS: {msg}")
        if kwargs:
            pprint(kwargs)


def log_info(msg,noisy,level='INFO',**kwargs):
    log(msg,noisy,level=level,**ee.Dictionary(kwargs).getInfo())


def print_info(**kwargs):
  pprint(ee.Dictionary(kwargs).getInfo())