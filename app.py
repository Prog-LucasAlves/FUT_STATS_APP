import streamlit as st
import pandas as pd
from main import createHomeHTFT

########################
# Configuração da Página
########################
st.set_page_config(page_title="FUTSTATS", page_icon="⚽", layout="wide")


########################
# Carregar os dados
########################
@st.cache_data(ttl=300)
def load_data():
    data = pd.read_csv("silver/Dados_Betfair_Exchange_HT00.csv", sep=";")
    return data


########################
# Título da página
########################
st.title("⚽ FutStats HT - FT")

########################
# Abas da página
########################
st.markdown(
    """
<style>
    div[data-baseweb="select"] > div {
        width: 200px !important;  /* Ajuste a largura conforme necessário */
    }
</style>
""",
    unsafe_allow_html=True,
)

tab1, tab2 = st.tabs(["Mandante | HT - FT", "Visitante | HT - FT"])

with tab1:
    home = st.selectbox(
        "Selecione o time mandante:",
        load_data()["Home"].sort_values().unique(),
    )
    # Exibeir os dados baseado no home createHomeHTFT
    st.dataframe(
        createHomeHTFT()[createHomeHTFT()["Home"] == home],
        hide_index=True,
        column_config={
            "Home": st.column_config.TextColumn("Time Mandante", width="medium"),
            "D/D": st.column_config.NumberColumn("Derrota/Derrota"),
        },
    )

with tab2:
    away = st.selectbox(
        "Selecione o time visitante:",
        load_data()["Away"].sort_values().unique(),
    )
