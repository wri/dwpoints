import ee
import pandas as pd
from pprint import pprint
import dwpoints.squash as squash
import dwpoints.config as config
import dwpoints.constants as c
import dwpoints.utils as utils
ee.Initialize()


#
# UI
#
def inspect(dw,lon,lat):
  """ inspect dw-squash at point lon,lat

  Args:
    - dw<ee.Image>: a single band dynamicworld-squash label image
    - lon<float>: longitude value 
    - lat<float>: latitude value 

  returns <int> dw-label value at point lon,lat 
  """
  pt=ee.Geometry.Point(lon,lat)
  sample_point=dw.rename(['label']).reproject(crs=c.CRS,scale=c.SCALE).reduceRegion(
    reducer=ee.Reducer.firstNonNull(), 
    geometry=pt, 
    scale=c.SCALE, 
    crs=c.CRS, 
    maxPixels=c.MAX_PIX
  )
  return sample_point.getNumber('label')

squashes=squash.annual_dw(2022)
DW_COLS=config.get("squash_keys")

def get_dw(col):
  return squashes[col]


def inpsect_row(row):
  values={ dwc: inspect(get_dw(dwc),row['lon'],row['lat']) for dwc in DW_COLS }
  print('-------------',values)
  return values
  # print('---')
  # return ee.Dictionary(values).getInfo()

def inspect_points(path):
  df=pd.read_csv(path)
  print('SIZE',df.shape[0])
  print(df.head().to_dict('records'),'>>>')
  df.loc[:,DW_COLS]=df.apply(inpsect_row,axis=1,result_type='expand')
  df_dict_list=df.to_dict('records')
  print(len(df_dict_list),df_dict_list[:3],'<<<',type(df_dict_list))
  df_dict_list=ee.List(df_dict_list).getInfo()
  print(len(df_dict_list),df_dict_list[:3],'<<<',type(df_dict_list))
  df=pd.DataFrame(df_dict_list)
  print(df.head().to_dict('records'),'>>>')



def run(*args,**kwargs):
  print("RUN",args)
  pprint(kwargs)
  print('--'*50)
  inspect_points('TEMP.csv')
  # inspect_points('https://storage.googleapis.com/dynamic-world-public/dw-exports/point_data/dev_dw_sample_pts-100.csv')





