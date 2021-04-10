import pandas as pd
import numpy as np
import sqlite3

DB_SAVE_NAME = 'public_data/names.db'
CENSUS_BASE = 308745538 # 2010 population
FB_RECORD_COUNT = 32315270 # SELECT COUNT(1) FROM TABLE

census = pd.read_csv('data/Names_2010Census.csv')
census = census[['name', 'count']]
census['freq'] = census['count'] / CENSUS_BASE
census.set_index('name', inplace=True)

sql = """
    select UPPER(lname) AS name, count(1) as count 
    from usa 
    group by UPPER(lname)
    having count(1) >= 10
    order by count desc"""

conn = sqlite3.connect('data/fbleak.db')
fbleak = pd.read_sql_query(sql, conn)
fbleak['freq'] = fbleak['count'] / FB_RECORD_COUNT
fbleak.set_index('name', inplace=True)
conn.close()

# generate percentile data
joined = fbleak.join(census, lsuffix='_fb', rsuffix='_c', how='inner')
overall_ratios = joined['freq_fb']/joined['freq_c']
percentiles = overall_ratios.quantile(np.linspace(0, 1, 100+1), 'lower')
percentiles.name = 'ratio'
percentiles.index.name = 'percentile'
percentiles = percentiles.reset_index()
percentiles.set_index('ratio',inplace=True)

# write out data
conn = sqlite3.connect(DB_SAVE_NAME)
census.to_sql('census',conn,if_exists='replace',index=True, index_label='name')
fbleak.to_sql('fbleak',conn,if_exists='replace',index=True, index_label='name')
percentiles.to_sql('percentiles',conn, if_exists='replace', index=True, index_label='ratio')
conn.close()