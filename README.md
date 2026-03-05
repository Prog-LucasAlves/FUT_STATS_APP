# FUT_STATS_APP

Aplicação de análise estatística de futebol (HT/FT) com foco em dados da Betfair Exchange, construída com Streamlit.

## Visão geral

O projeto faz três coisas principais:

- baixa dados históricos e jogos do dia a partir de fontes públicas;
- transforma os dados em camadas (`bronze`, `silver`, `gameday`);
- exibe estatísticas e tabelas interativas em uma interface Streamlit.

As análises são focadas em:

- transições de resultado entre HT e FT (`D/D`, `E/V`, `V/E`, etc.);
- probabilidades e odds implícitas por time mandante e visitante;
- cenários de jogos que chegam em `0x0` no HT e seus desfechos no FT.

## Stack

- Python 3.13+
- Streamlit
- Pandas
- Gerenciamento de dependências com `uv`

## Estrutura do projeto

```text
FUT_STATS_APP/
|- app.py
|- main.py
|- bronze/
|  |- Dados_Betfair_Exchange.csv
|- silver/
|  |- Dados_Betfair_Exchange_HT00.csv
|  |- Colunas.csv
|- gameday/
|  |- Jogos_do_Dia_Betfair_YYYY-MM-DD.csv
|- action/
|  |- T_HT00.xlsx
|- pyproject.toml
|- uv.lock
```

## Pipeline de dados

As funções de pipeline estão em `main.py`:

- `getDataDay()`:
  - baixa jogos do dia e do dia seguinte;
  - salva arquivos em `gameday/`.
- `getData()`:
  - baixa a base histórica da Betfair Exchange;
  - salva em `bronze/Dados_Betfair_Exchange.csv`.
- `joinData()`:
  - gera arquivos derivados em `silver/`;
  - cria `Dados_Betfair_Exchange_HT00.csv` com colunas relevantes de HT/FT.

As funções `create*` em `main.py` geram dataframes estatísticos usados na interface.

## Interface (Streamlit)

A aplicação (`app.py`) possui abas para:

- Dados Gerais
- Mandante | HT - FT
- Visitante | HT - FT
- Jogos do Dia

A interface lê principalmente:

- `silver/Dados_Betfair_Exchange_HT00.csv`
- `bronze/Dados_Betfair_Exchange.csv`
- arquivos em `gameday/`

## Como executar

## 1) Instalar dependências

Com `uv`:

```bash
uv sync
```

Sem `uv` (alternativa):

```bash
pip install streamlit pandas
```

## 2) Atualizar dados

```bash
python main.py
```

Esse comando baixa/atualiza os arquivos de entrada e de transformação local.

## 3) Rodar a aplicação

```bash
streamlit run app.py
```

Depois, abra a URL local informada pelo Streamlit (normalmente `http://localhost:8501`).

## Fontes de dados

- Jogos do dia:
  - `https://github.com/futpythontrader/Jogos_do_Dia`
- Base histórica Betfair Exchange:
  - `https://github.com/futpythontrader/Bases_de_Dados`

## Observações

- O projeto depende de acesso à internet para atualização das bases.
- Os arquivos CSV usam `;` como separador.
- Como a base cresce com o tempo, resultados e métricas mudam conforme a data de atualização.

## Licença

Este projeto está sob licença MIT. Consulte `LICENSE` para mais detalhes.
