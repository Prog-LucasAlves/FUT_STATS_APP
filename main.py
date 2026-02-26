import pandas as pd
import os


def getData():
    """Download arquivos CSVs"""

    # Criar Pasta Bronze
    PATH = "bronze"
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    url = "https://raw.githubusercontent.com/futpythontrader/Bases_de_Dados/refs/heads/main/Base_de_Dados_BetfairExchange.csv"
    df = pd.read_csv(url)
    df.to_csv(f"{PATH}/Dados_Betfair_Exchange.csv", index=False, sep=";")


def joinData():
    """Juntar arquivos CSVs por liga"""

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
                "Odd_H_Back",
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

    print(htfthome)


if __name__ == "__main__":
    getData()
    joinData()
    createHomeHTFT()
