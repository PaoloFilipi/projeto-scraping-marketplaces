import pandas as pd
import sqlite3
from  datetime import datetime


df = pd.read_json('../data/data.jsonl', lines=True)

# add column source
df['_source'] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"

#configure pandas to show all columns
pd.options.display.max_columns = None

#add column _data_coleta
df['_data_coleta'] = datetime.now()

#Transform data value null and define type
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

# remove columns parentheses  `reviews_amount`
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

# Transform prices to float and calculate total values
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

# Remove old price columns
df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'], inplace=True)

# Conect to database SQLite or Create new database
conn = sqlite3.connect('../data/quotes.db')

# Save DataFrame in database SQLite
df.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

# Close conection to database
conn.close()

print(df.head())

print(df)