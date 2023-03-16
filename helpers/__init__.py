import pandas as pd
import re
import numpy as np

def _extract_lesion_column(lesion):
    site, type_l, subtype, code = 'None', 'None', 'None', 'None'
    if lesion != 0:
        types = re.findall('^([1-9]|11|00)([1-4])([0-2])([1-9]|10|0)',str(lesion))
        if types:
            site, type_l, subtype, code = types[0]
    return pd.Series({'lesion_site': site, 'lesion_type': type_l, 'lesion_subtype': subtype, 'lesion_code': code}, dtype='category')

def get_data():
  df = pd.read_csv('./cow.csv')
  df.loc[:, ['lesion_site', 'lesion_type', 'lesion_subtype', 'lesion_code']] = df.lesion.apply(_extract_lesion_column).astype('category')
  df.drop(columns=['lesion', 'hospital_number'], inplace=True)
  categorical_columns = []
  for col in df:
      if str(df[col].dtype) != 'category' and df[col].unique().size < 10:
          df[col].fillna('[NAN]', inplace=True)
          categorical_columns.append(col)
          df[col] = df[col].astype('category')

  X = dict()
  Y = None
  for col in df:
      if col == 'outcome Class':
          Y = df[col].cat.codes.values
      elif str(df[col].dtype) != 'category':
          X[col] = {'data': df[col].fillna(df[col].mean()).values, 'type': 'category'}
      else:
          X[col] = {'data': df[col].cat.codes.values, 'type': 'number'}
  return X, Y