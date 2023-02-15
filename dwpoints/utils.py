import ee
from datetime import datetime
from pprint import pprint
import pandas as pd
import dwpoints.constants as c

EPS=1e-8
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
    total=pd.Series([df[df.label==l].shape[0] for l in counts.index])
    accs=counts[pred_cols].divide(total,axis=0)
    acc_row=pd.DataFrame([counts.sum(axis=0).divide(total.sum())])
    acc_row.index=['ALL']
    accs.rename(columns={ c:f'{c}_acc' for c in pred_cols},inplace=True)
    acc_row.rename(columns={ c:f'{c}_acc' for c in pred_cols},inplace=True)
    counts.rename(columns={ c:f'{c}_count' for c in pred_cols},inplace=True)
    stats=accs.join(counts)
    stats['total']=total
    stats=pd.concat([stats,acc_row]).fillna('--')
    return stats  


def get_cm_df(df,label_values,label_col,pred_col,dummy_prefix=c.DUMMY_PREFIX):
    dummies=pd.DataFrame(df[label_col]).join(pd.get_dummies(df[pred_col],prefix=dummy_prefix))
    required_cols=[f'{dummy_prefix}_{v}' for v in label_values]
    for col in required_cols:
        if col not in dummies:
            dummies[col]=0
    cm=dummies.groupby(label_col).sum()
    cm['total']=cm.sum(axis=1)
    col_total=cm.sum(axis=0)
    cm=pd.concat([cm,pd.DataFrame([col_total])]).astype(int)
    cm.index=[str(v) for v in label_values]+['total']
    return cm


def normalize_cm(cm_df,label_values,dummy_prefix=c.DUMMY_PREFIX):
    cols=[f'{dummy_prefix}_{v}' for v in label_values]
    rows=[f'{v}' for v in label_values]
    column_counts=cm_df.loc['total']
    column_counts=pd.DataFrame([column_counts])
    cm_df=cm_df.loc[rows,cols].divide(cm_df.loc['total',cols].add(EPS)).join(cm_df['total'])
    return pd.concat([cm_df,column_counts])



