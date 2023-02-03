import ee
import re
from pathlib import Path
import pandas as pd
from pprint import pprint
import dwpoints.labels as labels
import dwpoints.config as config
import dwpoints.constants as c
import dwpoints.utils as utils
ee.Initialize()
#
# CONFIG CONSTANTS
#
YEAR=config.get('year')
LON_COLUMN=config.get('lon')
LAT_COLUMN=config.get('lat')
MIN_CROP=config.get('min_crop')
MIN_CROPISH=config.get('min_cropish')
DEST_PREFIX=config.get('prefix')
ACCURACY_DEST_PREFIX=config.get('acc_prefix')
CONFUSION_DEST_PREFIX=config.get('cm_prefix')
SQUASH_KEYS=config.get('squash_keys')
NOISY=config.get('noisy')
NORMALIZE_CM=config.get('normalize')



#
# INTERNAL
#
def _inpsect_row(row,lon,lat,cols,labels_dict):
    """ _inpsect_row
    Returns row-<dict> containing label values for each col in cols
    """
    return { col: inspect(labels_dict[col],row[lon],row[lat]) for col in cols }


def _prefix_path(prefix,path):
    if re.search('^(http|https|gs)://',path):
        path=Path(path).name
    path=Path(path)
    newpath=f'{prefix}.{path.name}'
    parent=str(path.parent)
    if parent not in [None,False,'.','..','/','~/']:
        newpath=f'{parent}/{newpath}'
    return newpath


#
# PUBLIC
#
def inspect(label,lon,lat):
    """ inspect label at point lon,lat

    Args:
        - label<ee.Image>: a single band "label" ee.image
        - lon<float>: longitude value 
        - lat<float>: latitude value 

    returns <int> label value at point lon,lat 
    """
    pt=ee.Geometry.Point(lon,lat)
    sample_point=label.rename(['label']).reproject(crs=c.CRS,scale=c.SCALE).reduceRegion(
        reducer=ee.Reducer.firstNonNull(), 
        geometry=pt, 
        scale=c.SCALE, 
        crs=c.CRS, 
        maxPixels=c.MAX_PIX
    )
    return sample_point.getNumber('label')


def run(        
        src,
        dest=None,
        year=YEAR,
        lon=LON_COLUMN,
        lat=LAT_COLUMN,
        min_crop=MIN_CROP,
        min_cropish=MIN_CROPISH,
        prefix=DEST_PREFIX,
        noisy=NOISY,
        squash=SQUASH_KEYS):
    """ generate labels values for pts and labels in csv

    Args:
        - src<str>: path or url to source csv
        - dest<str|None>: destination (if None uses `{prefix}.{src}`)
        - year<int>: year to produce annual labels
        - lon<str>: longitude column name 
        - lat<str>: latitude column name 
        - min_crop<int>: minimum number of crop months for crop-rule
        - min_cropish<int>: minimum number of crop-ish months for crop-rule
        - prefix<str>: destination prefix (only used if dest not provided)
        - noisy<bool>: print log statements
        - squash<list<str>>: list of columns to use as squash keys

    Action: 
        label values are saved to csv
    """
    labels_dict=labels.annual_dw(year,min_crop,min_cropish)
    if squash:
        squash=squash.split(',')
    else:
        squash=config.get('squash_keys')
    if not dest:
        dest=_prefix_path(prefix,src)
    df=pd.read_csv(src)
    utils.log('generating dynamic world point values',
        year=year,
        min_crop=min_crop,
        min_cropish=min_cropish,
        src=src,
        dest=dest,
        nb_points=df.shape[0],
        squash_columns=squash)
    timer=utils.Timer()
    utils.log(f'[{timer.start()}] ...inspecting rows')
    df.loc[:,squash]=df.apply(
        _inpsect_row,
        axis=1,
        result_type='expand',
        lon=lon,lat=lat,cols=squash,labels_dict=labels_dict)
    utils.log(f'[{timer.time()}] ...earthengine request ({timer.state()})')
    out=df.to_dict('records')
    df_dict_list=ee.List(df.to_dict('records'))
    df=pd.DataFrame(df_dict_list.getInfo())
    df.to_csv(dest,index=False)
    utils.log(f'[{timer.stop()}] complete ({timer.delta()})')



def accuracy(        
        src,
        label,
        prefix=ACCURACY_DEST_PREFIX,
        noisy=NOISY,
        squash=SQUASH_KEYS):
    """ generate accuracy results in csv

    Args:
        - src<str>: path or url to source csv
        - label<str>: column name for label
        - dest<str|None>: destination (if None uses `{prefix}.{src}`)
        - prefix<str>: destination prefix (only used if dest not provided)
        - noisy<bool>: print log statements
        - squash<list<str>>: list of columns to use as squash keys

    Action: 
        accuracy results are saved to a csv
    """
    if squash:
        squash=squash.split(',')
    else:
        squash=config.get('squash_keys')
    dest=_prefix_path(prefix,src)
    df=pd.read_csv(src)
    utils.log('generating aggrement assement',
        src=src,
        dest=dest,
        nb_points=df.shape[0],
        squash_columns=squash)
    timer=utils.Timer()
    utils.log(f'[{timer.start()}] ...')
    df=utils.get_acc_df(df,label,squash)
    df.reset_index(names=['label']).to_csv(dest,index=False)
    utils.log(f'[{timer.stop()}] complete ({timer.delta()})')




def confusion(        
        src,
        label,
        prefix=CONFUSION_DEST_PREFIX,
        noisy=NOISY,
        squash=SQUASH_KEYS,
        normalize=NORMALIZE_CM):
    """ generate confusion-matrix results in csvs

    Args:
        - src<str>: path or url to source csv
        - label<str>: column name for label
        - dest<str|None>: destination (if None uses `{prefix}.{src}`)
        - prefix<str>: destination prefix (only used if dest not provided)
        - noisy<bool>: print log statements
        - squash<list<str>>: list of columns to use as squash keys

    Action: 
        confusion matrices are saved to individual csv's for each
        column in squash
    """
    if squash:
        squash=squash.split(',')
    else:
        squash=config.get('squash_keys')
    df=pd.read_csv(src)
    dest=_prefix_path(f'{prefix}.<squash>',src)
    utils.log('generating confusion matrices',
        src=src,
        dest=dest,
        nb_points=df.shape[0],
        squash_columns=squash)
    timer=utils.Timer()
    utils.log(f'[{timer.start()}] ...')
    for pcol in squash:
        cmdf=utils.get_cm_df(
            df,
            c.LABEL_VALUES,
            label,
            pcol)
        if normalize:
            cmdf=utils.normalize_cm(cmdf,c.LABEL_VALUES)
            dest=_prefix_path(f'{prefix}-norm.{pcol}',src)
            print(dest)
        else:
            dest=_prefix_path(f'{prefix}.{pcol}',src)
        print('-',dest)
        cmdf.reset_index(names=['label']).to_csv(dest,index=False)
        utils.log(f'[{timer.time()}] {pcol} ({timer.state()})') 
    utils.log(f'[{timer.stop()}] complete ({timer.delta()})')








