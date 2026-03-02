import pandas as pd
import os
import datetime


def getDataDay():
    """Download jogos do dia"""

    # Criar Pasta Bronze
    PATH = "gameday"
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    # Pegar coma data de hoje, amanha e dpois
    date_hoje = datetime.date.today()
    date_amanha = date_hoje + datetime.timedelta(days=1)
    date_depois = date_hoje + datetime.timedelta(days=2)

    date_list = [date_hoje, date_amanha, date_depois]

    for i in date_list:
        url = f"https://github.com/futpythontrader/Jogos_do_Dia/raw/main/Betfair/Jogos_do_Dia_Betfair_Back_Lay_{i}.csv"
        df = pd.read_csv(url)
        # Eliminar as colunas que começam com IDM
        df = df.loc[:, ~df.columns.str.startswith("IDM")]
        # Elimnrar as ultimas 10 colunas
        df = df.iloc[:, :-45]

        df.to_csv(f"{PATH}/Jogos_do_Dia_Betfair_{i}.csv", index=False, sep=";")


def getData():
    """Download dados jogos(odds) betfair"""

    # Criar Pasta Bronze
    PATH = "bronze"
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    url = "https://raw.githubusercontent.com/futpythontrader/Bases_de_Dados/refs/heads/main/Base_de_Dados_BetfairExchange.csv"
    df = pd.read_csv(url)
    df.to_csv(f"{PATH}/Dados_Betfair_Exchange.csv", index=False, sep=";")


def joinData():
    """Transformação dos jogos(odds) betfair"""

    # Criar Pasta Prata
    PATH = "silver"
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    # Pegar dados da pasta bronze e separar por liga
    for file in os.listdir("bronze"):
        df = pd.read_csv(f"bronze/{file}", sep=";")

        # Lista das colunas
        list = df.columns.tolist()

        # Salvar a lista em csv
        pd.DataFrame(list).to_csv(f"{PATH}/Colunas.csv", index=False, sep=";")

        ####### 0 x 0 HT #######
        HT00 = df[
            [
                "Date",
                "Home",
                "Away",
                "Goals_H_HT",
                "Goals_A_HT",
                "Goals_H_FT",
                "Goals_A_FT",
            ]
        ]
        HT00["HT00"] = HT00.apply(
            lambda row: 1 if row["Goals_H_HT"] == 0 and row["Goals_A_HT"] == 0 else 0,
            axis=1,
        )

        HT00.to_csv(f"{PATH}/Dados_Betfair_Exchange_HT00.csv", index=False, sep=";")
        ####### 0 x 0 HT #######


def createDataframeHTFT():
    """Criar dataframe com informações de gols e resultado no HT e FT"""

    # Pegar dados da pasta bronze e separar por liga
    for file in os.listdir("bronze"):
        df = pd.read_csv(f"bronze/{file}", sep=";")

    def result(h, a):
        if h > a:
            return "V"
        elif h < a:
            return "D"
        else:
            return "E"

    df["Result_HT"] = df.apply(
        lambda row: result(row["Goals_H_HT"], row["Goals_A_HT"]),
        axis=1,
    )
    df["Result_FT"] = df.apply(
        lambda row: result(row["Goals_H_FT"], row["Goals_A_FT"]),
        axis=1,
    )

    # ) Coluna com o resultado do HT e FT combinados
    df["HT_FT"] = df["Result_HT"] + "/" + df["Result_FT"]

    return df


def createHomeHTFT():
    """Criar dataframe com informações de gols e resultado no HT e FT apenas para jogos de casa"""

    df = createDataframeHTFT()

    htfthome = (
        df.groupby("Home")["HT_FT"].value_counts().unstack(fill_value=0).reset_index()
    )

    htfthome["Games"] = htfthome.select_dtypes(include="number").sum(axis=1)

    cols_ht_derrota = ["D/V", "D/E", "D/D"]
    cols_ht_empate = ["E/V", "E/E", "E/D"]
    cols_ht_vitoria = ["V/V", "V/E", "V/D"]

    htfthome["HT_Losse_Games"] = htfthome[cols_ht_derrota].sum(axis=1)
    htfthome["HT_Draw_Games"] = htfthome[cols_ht_empate].sum(axis=1)
    htfthome["HT_Win_Games"] = htfthome[cols_ht_vitoria].sum(axis=1)

    # round(1 / (team_stats["perc_acima_05"] / 100), 2)

    htfthome["P_D_D"] = round((htfthome["D/D"] / htfthome["HT_Losse_Games"]) * 100, 2)
    htfthome["Odd_back_D/D"] = round(1 / (htfthome["P_D_D"] / 100), 2)
    htfthome["Odd_lay_D/D"] = round(1 / (1 - (htfthome["P_D_D"] / 100)), 2)

    htfthome["P_D_E"] = round((htfthome["D/E"] / htfthome["HT_Losse_Games"]) * 100, 2)
    htfthome["Odd_back_D/E"] = round(1 / (htfthome["P_D_E"] / 100), 2)
    htfthome["Odd_lay_D/E"] = round(1 / (1 - (htfthome["P_D_E"] / 100)), 2)

    htfthome["P_D_V"] = round((htfthome["D/V"] / htfthome["HT_Losse_Games"]) * 100, 2)
    htfthome["Odd_back_D/V"] = round(1 / (htfthome["P_D_V"] / 100), 2)
    htfthome["Odd_lay_D/V"] = round(1 / (1 - (htfthome["P_D_V"] / 100)), 2)

    htfthome["P_E_D"] = round((htfthome["E/D"] / htfthome["HT_Draw_Games"]) * 100, 2)
    htfthome["Odd_back_E/D"] = round(1 / (htfthome["P_E_D"] / 100), 2)
    htfthome["Odd_lay_E/D"] = round(1 / (1 - (htfthome["P_E_D"] / 100)), 2)

    htfthome["P_E_E"] = round((htfthome["E/E"] / htfthome["HT_Draw_Games"]) * 100, 2)
    htfthome["Odd_back_E/E"] = round(1 / (htfthome["P_E_E"] / 100), 2)
    htfthome["Odd_lay_E/E"] = round(1 / (1 - (htfthome["P_E_E"])) / 100, 2)

    htfthome["P_E_V"] = round((htfthome["E/V"] / htfthome["HT_Draw_Games"]) * 100, 2)
    htfthome["Odd_back_E/V"] = round(1 / (htfthome["P_E_V"] / 100), 2)
    htfthome["Odd_lay_E/V"] = round(1 / (1 - (htfthome["P_E_V"])) / 100, 2)

    dataprob = htfthome["Odd_lay"] = htfthome["P_E_V"] + htfthome["P_E_D"]
    htfthome["Odd_Lay_Draw"] = round(1 / (1 - (dataprob / 100)), 2)  #

    htfthome["P_V_D"] = round((htfthome["V/D"] / htfthome["HT_Win_Games"]) * 100, 2)
    htfthome["Odd_back_V/D"] = round(1 / (htfthome["P_V_D"] / 100), 2)
    htfthome["Odd_lay_V/D"] = round(1 / (1 - (htfthome["P_V_D"])) / 100, 2)

    htfthome["P_V_E"] = round((htfthome["V/E"] / htfthome["HT_Win_Games"]) * 100, 2)
    htfthome["Odd_back_V/E"] = round(1 / (htfthome["P_V_E"] / 100), 2)
    htfthome["Odd_lay_V/E"] = round(1 / (1 - (htfthome["P_V_E"])) / 100, 2)

    htfthome["P_V_V"] = round((htfthome["V/V"] / htfthome["HT_Win_Games"]) * 100, 2)
    htfthome["Odd_back_V/V"] = round(1 / (htfthome["P_V_V"] / 100), 2)
    htfthome["Odd_lay_V/V"] = round(1 / (1 - (htfthome["P_V_V"])) / 100, 2)

    return htfthome


def createHomeHTGoals():

    hthomegoals = createDataframeHTFT()

    hthomegoals = hthomegoals[["Home", "Goals_H_HT", "Goals_A_HT"]]

    hthomegoals["Goals_total"] = hthomegoals["Goals_H_HT"] + hthomegoals["Goals_A_HT"]

    team_stats = (
        hthomegoals.groupby("Home")
        .agg(
            total_jogos=("Goals_H_HT", "count"),
            total_gols_home=("Goals_H_HT", "sum"),
            total_gols_away=("Goals_A_HT", "sum"),
            acima_05=("Goals_total", lambda x: (x > 0.5).sum()),
            acima_15=("Goals_total", lambda x: (x > 1.5).sum()),
        )
        .reset_index()
    )

    team_stats["perc_acima_05"] = (
        team_stats["acima_05"] / team_stats["total_jogos"]
    ) * 100
    team_stats["Odd_perc_acima_05"] = round(1 / (team_stats["perc_acima_05"] / 100), 2)

    team_stats["perc_acima_15"] = (
        team_stats["acima_15"] / team_stats["total_jogos"]
    ) * 100
    team_stats["Odd_perc_acima_15"] = round(1 / (team_stats["perc_acima_15"] / 100), 2)

    team_stats = team_stats[
        [
            "Home",
            "total_jogos",
            "total_gols_home",
            "total_gols_away",
            "acima_05",
            "perc_acima_05",
            "Odd_perc_acima_05",
            "acima_15",
            "perc_acima_15",
            "Odd_perc_acima_15",
        ]
    ]

    return team_stats


if __name__ == "__main__":
    getDataDay()
    getData()
    joinData()
    createHomeHTFT()
    createHomeHTGoals()
