import sqlite3
import pandas as pd
import numpy as np
import datetime as dt

# Extracting csv contents and inserting into df variable
df = pd.read_csv('../../data/transactional-sample.csv', encoding='UTF-8', 
                 dtype={'transaction_id': str, 'merchant_id': str, 'user_id': str, 'device_id': str,
                        'card_number': str, 'transaction_amount': float, 'has_cbk': bool})

# Setting all columns to visible in pandas
pd.options.display.max_columns = None

# Creating 2 new columns from transaction_date(Date and Hour) 
df['transaction_time'] = pd.to_datetime(df['transaction_date']).dt.strftime('%H:%M:%S')
df['transaction_date'] = pd.to_datetime(df['transaction_date']).dt.strftime('%Y/%m/%d')

# Reordering columns
df_reordered = df.iloc[:, [0, 1, 2, 4, 8, 3, 5, 6, 7]]

# Connecting to SQLite database
conn = sqlite3.connect('../../data/cloudwalk_case.db')

# Saving dataframe into .db
df_reordered.to_sql('transactional_sample', conn, if_exists='replace', index=False)

# Closing connection to db
conn.close()