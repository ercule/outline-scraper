# python3 -m pip install pandas
# to run: python3 concat.py

import pandas as pd
from pathlib import Path

source_files = sorted(Path('/Users/jd/Desktop/FireHydrantCSV').glob('*.csv'))

dataframes = []
for file in source_files:
    df = pd.read_csv(file) # additional arguments up to your needs
    df['source'] = file.name
    dataframes.append(df)

df_all = pd.concat(dataframes)
df_all.to_csv("merged.csv")