import ee
import re
from pathlib import Path
import pandas as pd
from pprint import pprint
import dwpoints.squash as squash
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
SQUASH_KEYS=config.get('squash_keys')
NOISY=config.get('noisy')



#
# INTERNAL
#
def _inpsect_row(row,lon,lat,cols):
    """ _inpsect_row
    Returns row-<dict> containing label values for each col in cols
    """
    return { col: inspect(squashes[col],row[lon],row[lat]) for col in cols }


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
def inspect(labels,lon,lat):
    """ inspect labels-squash at point lon,lat

    Args:
        - labels<ee.Image>: a single band "labels" ee.image
        - lon<float>: longitude value 
        - lat<float>: latitude value 

    returns <int> labels-label value at point lon,lat 
    """
    pt=ee.Geometry.Point(lon,lat)
    sample_point=labels.rename(['label']).reproject(crs=c.CRS,scale=c.SCALE).reduceRegion(
        reducer=ee.Reducer.firstNonNull(), 
        geometry=pt, 
        scale=c.SCALE, 
        crs=c.CRS, 
        maxPixels=c.MAX_PIX
    )
    return sample_point.getNumber('label')



def inspect_points(src,dest,year,lon,lat,min_crop,min_cropish,noisy,squash):
    df=pd.read_csv(path)
    print(df.head().to_dict('records'),'>>>')
    df.loc[:,DW_COLS]=df.apply(_inpsect_row,axis=1,result_type='expand')
    df_dict_list=df.to_dict('records')
    print(len(df_dict_list),df_dict_list[:3],'<<<',type(df_dict_list))
    df_dict_list=ee.List(df_dict_list).getInfo()
    print(len(df_dict_list),df_dict_list[:3],'<<<',type(df_dict_list))
    df=pd.DataFrame(df_dict_list)
    print(df.head().to_dict('records'),'>>>')



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
    print("RUN",squash)
    if squash:
        squash=squash.split(',')
    else:
        squash=config.get('squash_keys')
    if not dest:
        dest=_prefix_path(prefix,src)
    print(lon,lat,dest,squash)
    print('--'*50)
    df=pd.read_csv(path)
    print('SIZE',df.shape[0])
    # inspect_points(src,dest,year,lon,lat,min_crop,min_cropish,noisy,squash)




