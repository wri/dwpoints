import ee
import squash
import config
import constants as c
import utils as utils
import pandas as pd
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
  print(df.to_dict('records'),'>>>')
  df.loc[:,DW_COLS]=df.apply(inpsect_row,axis=1,result_type='expand')
  df_dict_list=df.to_dict('records')
  print(df_dict_list,'<<<',type(df_dict_list))
  df_dict_list=ee.List(df_dict_list).getInfo()
  print(df_dict_list,'<<<',type(df_dict_list))  
  df=pd.DataFrame(df_dict_list)
  print(df.to_dict('records'),'>>>')



inspect_points('TEMP.csv')

# squashes=squash.annual_dw(2022)



# lon=-82.45585937500002
# lat=34.87213971567944

# lon=-82.915298
# lat=34.816375

# for k,v in squashes.items():
#   utils.log_info(msg=k,noisy=True,lon=lon,lat=lat,inspect=inspect(v,lon,lat,True))






