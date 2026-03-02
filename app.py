import streamlit as st
import pandas as pd
from main import createHomeHTFT, createHomeHTGoals
import os

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


@st.cache_data(ttl=300)
def load_data_total():
    data = pd.read_csv("bronze/Dados_Betfair_Exchange.csv", sep=";")
    return data


@st.cache_data(ttl=300)
def load_data_today():
    # Ler e unir varios arquivos csv da pasta gameday
    data = pd.concat(
        [pd.read_csv(f"gameday/{file}", sep=";") for file in os.listdir("gameday")],
    )
    return data


@st.cache_data(ttl=300)
def load_createHomeHTFT():
    data = createHomeHTFT()
    return data


@st.cache_data(ttl=300)
def load_createHomeHTGoals():
    data = createHomeHTGoals()
    return data


########################
# Título da página
########################
st.title("⚽ FutStats HT - FT")

ultima_data = load_data_total().iloc[-1]["Date"]
st.markdown(f"**📅 Última atualização: {ultima_data}**")

########################
# CSS
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

st.markdown(
    """
<style>
    div[data-testid="stDateInput"] > div {
        width: 200px !important;  /* Ajuste a largura conforme necessário */
    }
</style>
""",
    unsafe_allow_html=True,
)

########################
# Abas da página
########################
tab1, tab2, tab3, tab4 = st.tabs(
    ["Dados Gerais", "Mandante | HT - FT", "Visitante | HT - FT", "Jogos do Dia"],
)

with tab1:
    minDateDG = load_data_total()["Date"].min()
    maxDateDG = load_data_total()["Date"].max()

    selectDataDG = st.date_input(
        "Selecione a data:",
        value=minDateDG,
        min_value=minDateDG,
        max_value=maxDateDG,
        format="DD/MM/YYYY",
    )

    dateDG = selectDataDG.strftime("%Y-%m-%d")

    st.dataframe(
        load_data_total()[load_data_total()["Date"] == dateDG],
        hide_index=True,
        width="stretch",
    )

with tab2:
    st.subheader("⚽ Informações do HT")

    home = st.selectbox(
        "Selecione o time mandante:",
        load_data()["Home"].sort_values().unique(),
    )
    # Exibir os dados baseado no home - time selecionado
    datamandantehtft = load_createHomeHTFT()[load_createHomeHTFT()["Home"] == home]

    # Exibr os dados baseado no home - - time selecionado
    datamandantegoalsht = load_createHomeHTGoals()[
        load_createHomeHTGoals()["Home"] == home
    ]

    # Organizar as colunas
    datamandantehtft = datamandantehtft[
        [
            "Home",
            "Games",
            "HT_Losse_Games",
            "D/D",
            "P_D_D",
            "Odd_back_D/D",
            "Odd_lay_D/D",
            "D/E",
            "P_D_E",
            "Odd_back_D/E",
            "Odd_lay_D/E",
            "D/V",
            "P_D_V",
            "Odd_back_D/V",
            "Odd_lay_D/V",
            "HT_Draw_Games",
            "E/D",
            "P_E_D",
            "Odd_back_E/D",
            "Odd_lay_E/D",
            "E/E",
            "P_E_E",
            "Odd_back_E/E",
            "Odd_lay_E/E",
            "E/V",
            "P_E_V",
            "Odd_back_E/V",
            "Odd_lay_E/V",
            "Odd_Lay_Draw",
            "HT_Win_Games",
            "V/D",
            "P_V_D",
            "Odd_back_V/D",
            "Odd_lay_V/D",
            "V/E",
            "P_V_E",
            "Odd_back_V/E",
            "Odd_lay_V/E",
            "V/V",
            "P_V_V",
            "Odd_back_V/V",
            "Odd_lay_V/V",
        ]
    ]

    # Dataframe Derrota
    dataderrotahtmandante = datamandantehtft[
        [
            "Home",
            "HT_Losse_Games",
            "D/D",
            "P_D_D",
            "Odd_back_D/D",
            "Odd_lay_D/D",
            "D/E",
            "P_D_E",
            "Odd_back_D/E",
            "Odd_lay_D/E",
            "D/V",
            "P_D_V",
            "Odd_back_D/V",
            "Odd_lay_D/V",
        ]
    ]

    # Dataframe Empate
    dataempatehtmandante = datamandantehtft[
        [
            "Home",
            "HT_Draw_Games",
            "E/D",
            "P_E_D",
            "Odd_back_E/D",
            "Odd_lay_E/D",
            "E/E",
            "P_E_E",
            "Odd_back_E/E",
            "Odd_lay_E/E",
            "E/V",
            "P_E_V",
            "Odd_back_E/V",
            "Odd_lay_E/V",
            "Odd_Lay_Draw",
        ]
    ]

    # Dataframe Vitória
    datavitoriahtmandante = datamandantehtft[
        [
            "Home",
            "HT_Win_Games",
            "V/D",
            "P_V_D",
            "Odd_back_V/D",
            "Odd_lay_V/D",
            "V/E",
            "P_V_E",
            "Odd_back_V/E",
            "Odd_lay_V/E",
            "V/V",
            "P_V_V",
            "Odd_back_V/V",
            "Odd_lay_V/V",
        ]
    ]

    # Dataframe Informações Gerais
    datainfo = datamandantehtft[
        ["Home", "Games", "HT_Losse_Games", "HT_Draw_Games", "HT_Win_Games"]
    ]

    st.dataframe(
        datainfo,
        hide_index=True,
        width="content",
        column_config={
            "Home": st.column_config.TextColumn("Time Mandante", width="medium"),
            "Games": st.column_config.NumberColumn("Jogos"),
            "HT_Losse_Games": st.column_config.NumberColumn("Qtd. Derrotas HT"),
            "HT_Draw_Games": st.column_config.NumberColumn("Qtd. Empates HT"),
            "HT_Win_Games": st.column_config.NumberColumn("Qtd. Vitórias HT"),
        },
    )

    st.dataframe(
        datamandantegoalsht,
        hide_index=True,
        width="content",
        column_config={
            "Home": st.column_config.TextColumn("Time Mandante", width="medium"),
            "total_jogos": st.column_config.NumberColumn("Jogos"),
            "total_gols_home": st.column_config.NumberColumn("Gols Marcados HT"),
            "total_gols_away": st.column_config.NumberColumn("Gols Sofridos HT"),
            "acima_05": st.column_config.NumberColumn("Jogos Acima 0.5 Gols HT"),
            "perc_acima_05": st.column_config.NumberColumn(
                "Prob. Acima 0.5 Gols HT",
                format="%.2f%%",
            ),
            "Odd_perc_acima_05": st.column_config.NumberColumn(
                "Odd Prob. Acima 0.5 Gols HT",
                format="%.2f",
            ),
            "acima_15": st.column_config.NumberColumn("Jogos Acima 1.5 Gols HT"),
            "perc_acima_15": st.column_config.NumberColumn(
                "Prob. Acima 1.5 Gols HT",
                format="%.2f%%",
            ),
            "Odd_perc_acima_15": st.column_config.NumberColumn(
                "Odd Prob. Acima 1.5 Gols HT",
                format="%.2f",
            ),
        },
    )

    st.dataframe(
        dataderrotahtmandante,
        hide_index=True,
        width="content",
        column_config={
            "Home": st.column_config.TextColumn("Time Mandante", width="medium"),
            "HT_Losse_Games": st.column_config.NumberColumn("Qtd. Derrotas HT"),
            # Derrota -> Derrota
            "D/D": st.column_config.NumberColumn("D/D"),
            "P_D_D": st.column_config.NumberColumn("P(D/D)", format="%.2f%%"),
            "Odd_back_D/D": st.column_config.NumberColumn(
                "Odd Back D/D",
                format="%.2f",
            ),
            "Odd_lay_D/D": st.column_config.NumberColumn("Odd Lay D/D", format="%.2f"),
            # Derrota -> Empate
            "D/E": st.column_config.NumberColumn("D/E"),
            "P_D_E": st.column_config.NumberColumn("P(D/E)", format="%.2f%%"),
            "Odd_back_D/E": st.column_config.NumberColumn(
                "Odd Back D/E",
                format="%.2f",
            ),
            "Odd_lay_D/E": st.column_config.NumberColumn("Odd Lay D/E", format="%.2f"),
            # Derrota -> Vitória
            "D/V": st.column_config.NumberColumn("D/V"),
            "P_D_V": st.column_config.NumberColumn("P(D/V)", format="%.2f%%"),
            "Odd_back_D/V": st.column_config.NumberColumn(
                "Odd Back D/V",
                format="%.2f",
            ),
            "Odd_lay_D/V": st.column_config.NumberColumn("Odd Lay D/V", format="%.2f"),
        },
    )

    st.dataframe(
        dataempatehtmandante,
        hide_index=True,
        width="content",
        column_config={
            "Home": st.column_config.TextColumn("Time Mandante", width="medium"),
            "HT_Draw_Games": st.column_config.NumberColumn("Qtd. Empates HT"),
            # Empate -> Derrota
            "E/D": st.column_config.NumberColumn("E/D"),
            "P_E_D": st.column_config.NumberColumn("P(E/D)", format="%.2f%%"),
            "Odd_back_E/D": st.column_config.NumberColumn(
                "Odd Back E/D",
                format="%.2f",
            ),
            "Odd_lay_E/D": st.column_config.NumberColumn("Odd Lay E/D", format="%.2f"),
            # Empate -> Empate
            "E/E": st.column_config.NumberColumn("E/E"),
            "P_E_E": st.column_config.NumberColumn("P(E/E)", format="%.2f%%"),
            "Odd_back_E/E": st.column_config.NumberColumn(
                "Odd Back E/E",
                format="%.2f",
            ),
            "Odd_lay_E/E": st.column_config.NumberColumn("Odd Lay E/E", format="%.2f"),
            # Empate -> Vitória
            "E/V": st.column_config.NumberColumn("E/V"),
            "P_E_V": st.column_config.NumberColumn("P(E/V)", format="%.2f%%"),
            "Odd_back_E/V": st.column_config.NumberColumn(
                "Odd Back E/V",
                format="%.2f",
            ),
            "Odd_lay_E/V": st.column_config.NumberColumn("Odd Lay E/V", format="%.2f"),
            # Lay Draw
            "Odd_Lay_Draw": st.column_config.NumberColumn(
                "Odd Lay Draw",
                format="%.2f",
            ),
        },
    )

    st.dataframe(
        datavitoriahtmandante,
        hide_index=True,
        width="content",
        column_config={
            "Home": st.column_config.TextColumn("Time Mandante", width="medium"),
            "HT_Win_Games": st.column_config.NumberColumn("Qtd. Vitórias HT"),
            # Vitória -> Derrota
            "V/D": st.column_config.NumberColumn("V/D"),
            "P_V_D": st.column_config.NumberColumn("P(V/D)", format="%.2f%%"),
            "Odd_back_V/D": st.column_config.NumberColumn(
                "Odd Back V/D",
                format="%.2f",
            ),
            "Odd_lay_V/D": st.column_config.NumberColumn("Odd Lay V/D", format="%.2f"),
            # Vitória -> Empate
            "V/E": st.column_config.NumberColumn("V/E"),
            "P_V_E": st.column_config.NumberColumn("P(V/E)", format="%.2f%%"),
            "Odd_back_V/E": st.column_config.NumberColumn(
                "Odd Back V/E",
                format="%.2f",
            ),
            "Odd_lay_V/E": st.column_config.NumberColumn("Odd Lay V/E", format="%.2f"),
            # Vitória -> Vitória
            "V/V": st.column_config.NumberColumn("V/V"),
            "P_V_V": st.column_config.NumberColumn("P(V/V)", format="%.2f%%"),
            "Odd_back_V/V": st.column_config.NumberColumn(
                "Odd Back V/V",
                format="%.2f",
            ),
            "Odd_lay_V/V": st.column_config.NumberColumn("Odd Lay V/V", format="%.2f"),
        },
    )


with tab3:
    away = st.selectbox(
        "Selecione o time visitante:",
        load_data()["Away"].sort_values().unique(),
    )

with tab4:
    # Selecionar data
    dateJD = st.selectbox(
        "Selecione a data:",
        load_data_today()["Date"].sort_values().unique(),
    )
    st.dataframe(
        load_data_today()[load_data_today()["Date"] == dateJD],
        hide_index=True,
        width="stretch",
    )
