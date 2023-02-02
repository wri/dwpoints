import ee
from pprint import pprint
import dwpoints.constants as c


#
# print/log
#
def log(msg,noisy=c.NOISY,level='INFO',**kwargs):
    print()
    if noisy:
        print(f"[{level}] DW_POINTS: {msg}")
        if kwargs:
            print('-'*100)
            pprint(kwargs)
    print()


def log_info(msg,noisy=c.NOISY,level='INFO',**kwargs):
    log(msg,noisy,level=level,**ee.Dictionary(kwargs).getInfo())


def print_info(**kwargs):
  pprint(ee.Dictionary(kwargs).getInfo())