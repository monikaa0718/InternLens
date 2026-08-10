import sqlite3
import pandas as pd

conn = sqlite3.connect('internlens.db')

df = pd.read_sql_query('SELECT * FROM internship_reviews', conn)

df.to_csv('internlens_export.csv', index=False)

print('Exported to internlens_export.csv')