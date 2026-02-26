import streamlit as st
import pandas as pd

########################
# Configuração da Página
########################
st.set_page_config(page_title="FUTSTATS", page_icon="⚽", layout="wide")


########################
# Carregar os dados
########################
@st.cache_data(ttl=300)
def load_data():
    data = pd.read_csv("silver/Dados_Betfair_Exchange_HT00.csv")
    return data


########################
# Título da página
########################
st.title("⚽ FutStats HT - FT")

########################
# Abas da página
########################
tab1, tab2 = st.tabs(["Mandante | HT - FT", "Visitante | HT - FT"])

with tab1:
    home = st.selectbox("Selecione o time mandante:", load_data()["Home"].unique())

with tab2:
    away = st.selectbox("Selecione o time visitante:", load_data()["Away"].unique())
