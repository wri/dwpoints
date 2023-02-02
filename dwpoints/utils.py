import ee
from datetime import datetime
from pprint import pprint
import dwpoints.constants as c


#
# print/log
#
def log(msg,noisy=c.NOISY,level='INFO',**kwargs):
    if noisy:
        print(f"[{level}] DW_POINTS: {msg}")
        if kwargs:
            print('-'*100)
            pprint(kwargs)


def log_info(msg,noisy=c.NOISY,level='INFO',**kwargs):
    log(msg,noisy,level=level,**ee.Dictionary(kwargs).getInfo())


def print_info(**kwargs):
  pprint(ee.Dictionary(kwargs).getInfo())


#
# TIMER
#
class Timer(object):
    TIME_FORMAT='[%Y.%m.%d] %H:%M:%S'
    def __init__(self,fmt=TIME_FORMAT):
        self.fmt=fmt
    def start(self):
        self.start=datetime.now()
        return self.start.strftime(self.fmt)
    def time(self):
        return datetime.now().strftime(self.fmt)
    def state(self):
        return str(datetime.now()-self.start)
    def stop(self):
        self.end=datetime.now()
        return self.end.strftime(self.fmt)
    def delta(self):
        return str(self.end-self.start)