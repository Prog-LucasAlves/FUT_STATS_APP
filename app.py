import streamlit as st
import pandas as pd 

########################
# Configuração da Página
########################
st.set_page_config(
    page_title="FUTSTATS",
    page_icon="⚽",
    layout="wide"
)

########################
# Carregar os dados
########################
df = pd.read_csv('silver/Dados_Betfair_Exchange_HT00.csv')

########################
# Título da página
########################
st.title("⚽ FUTSTATS APP HT - FT")


st.table()
