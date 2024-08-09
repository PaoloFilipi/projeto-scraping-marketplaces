import streamlit as st
import pandas as pd
import sqlite3

#conect to database SQLite
conn = sqlite3.connect('../data/quotes.db')

#Load table data mercadolivre_items in DataFrame pandas
df = pd.read_sql_query("select * from mercadolivre_items", conn)

#close database SQLite
conn.close()


st.title('Pesquisa de Mercado - Tênis Esportivo no Mercado Livre')
st.subheader('KPIs principais do sistema')

col1,col2,col3 = st.columns(3)

total_itens = df.shape[0]
col1.metric(label="Número Total de Itens", value = total_itens )

unique_brands = df['brand'].nunique()
col2.metric(label = "Número de Marcas Únicas", value = unique_brands)

average_new_price = df['new_price'].mean()
col3.metric(label ="Preço Médio Novo (R$)", value = f"{average_new_price:.2f}")

st.subheader('Marcas Mais Encontradas até a 10ª Página')
col1 ,col2 = st.columns([4,2])
top_10_page_brands = df['brand'].value_counts().sort_values(ascending=False)

col1.bar_chart(top_10_page_brands)
col2.write(top_10_page_brands)

st.subheader('Preço Médio por Marca')
col1, col2 = st.columns([4,2])
average_price_by_brand = df.groupby('brand')['new_price'].mean().sort_values(ascending=False)
col1.bar_chart(average_price_by_brand)
col2.write(average_price_by_brand)

#satisfação de marca
st.subheader('Satisfação por marca')
col1, col2 = st.columns([4, 2])
df_non_zero_reviews = df[df['reviews_rating_number'] > 0]
satisfaction_by_brand = df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)