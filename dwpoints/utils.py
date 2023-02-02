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


#
# SCORING
#
def _equality_row(row,label_col,pred_cols):
    eq_dict={ pcol: int(row[label_col]==row[pcol]) for pcol in pred_cols }
    eq_dict['label']=row[label_col]
    return eq_dict
    
    
def get_acc_df(df,label_col,pred_cols):
    eq=pd.DataFrame(df.apply(
        _equality_row,
        axis=1,
        label_col=label_col,
        pred_cols=pred_cols).tolist())
    counts=eq.groupby(label_col).sum()
    counts['total']=[df[df.label==l].shape[0] for l in counts.index]
    accs=counts[pred_cols].divide(counts['total'],axis=0)
    accs.rename(columns={ c:f'{c}_acc' for c in pred_cols},inplace=True)
    counts.rename(columns={ c:f'{c}_count' for c in pred_cols},inplace=True)
    return accs.join(counts)



