import requests
import pandas as pd
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4OTcxMzUzLCJpYXQiOjE3NTYzNzkzNTMsImp0aSI6ImJlYjRlYWZhNjkzMjRmNjFiM2I4MTBmYzE3NGY5NGJiIiwidXNlcl9pZCI6IjgzIn0.ArrFg8_7SCDM3CbauaLcQZX5fkpZkYhiuy3rt2l9xHg"
headers = {'Authorization': 'JWT {}'.format(token)}

#petrobras
params = {
'ticker': 'PETR4',
'ano_tri': '20252T',
}

response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
response.status_code
response = response.json()
dados = response["dados"][0]
balanco = dados["balanco"]
df = pd.DataFrame(balanco)

filtro = (
        (df["conta"] == "3.11") & 
        (df["descricao"].str.contains("^lucro", case=False)) &
        (df["data_ini"]=="2025-01-01")
        )
lucro_liquido = df.loc[filtro, ["valor"]].iloc[0]

filtro = (
        (df["conta"] == "2.03") & 
        (df["descricao"].str.contains("^patrimônio", case=False)) 
        )
pl = df.loc[filtro, ["valor"]].iloc[0]
roe = lucro_liquido / pl
roe

#vale
params = {
'ticker': 'VALE3',
'ano_tri': '20252T',
}

response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
response.status_code
response = response.json()
dados = response["dados"][0]
balanco = dados["balanco"]
df = pd.DataFrame(balanco)

filtro = (
        (df["conta"] == "3.11") & 
        (df["descricao"].str.contains("^lucro", case=False)) &
        (df["data_ini"]=="2025-01-01")
        )
lucro_liquido = df.loc[filtro, ["valor"]].iloc[0]

filtro = (
        (df["conta"] == "2.03") & 
        (df["descricao"].str.contains("^patrimônio", case=False)) 
        )
pl = df.loc[filtro, ["valor"]].iloc[0]
roe = lucro_liquido / pl
roe

#banco do brasil
for ticker in ["PETR4", "VALE3", "BBAS3"]:
    params = {
    'ticker': ticker,
    'ano_tri': '20252T',
    }
    response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
    response.status_code
    response = response.json()
    dados = response["dados"][0]
    balanco = dados["balanco"]
    df = pd.DataFrame(balanco)

    filtro = (
            (df["conta"] == "3.11") & 
            (df["descricao"].str.contains("^lucro", case=False)) &
            (df["data_ini"]=="2025-01-01")
            )
    lucro_liquido = df.loc[filtro, ["valor"]].iloc[0]

    filtro = (
            (df["conta"].str.contains("2.0.", case=False)) & 
            (df["descricao"].str.contains("^patrim", case=False)) 
            )
    pl = df.loc[filtro, ["valor"]].iloc[0]
    roe = lucro_liquido / pl
    print(roe)
#todas
import requests
import pandas as pd

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU4OTcxMzUzLCJpYXQiOjE3NTYzNzkzNTMsImp0aSI6ImJlYjRlYWZhNjkzMjRmNjFiM2I4MTBmYzE3NGY5NGJiIiwidXNlcl9pZCI6IjgzIn0.ArrFg8_7SCDM3CbauaLcQZX5fkpZkYhiuy3rt2l9xHg"
headers = {'Authorization': 'JWT {}'.format(token)}
params = {
'data_base': '2025-09-01'
}
response = requests.get('https://laboratoriodefinancas.com/api/v1/planilhao',params=params, headers=headers)
response = response.json()
dados = response["dados"]
df = pd.DataFrame(dados)
filtro = df["setor"]=="construção"
tickers = df.loc[filtro, "ticker"].values
lista_resultado=[]
for ticker in tickers:
    params = {
    'ticker': ticker,
    'ano_tri': '20252T',
    }
    response = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
    response.status_code
    response = response.json()
    dados = response["dados"][0]
    balanco = dados["balanco"]
    df = pd.DataFrame(balanco)

    filtro = (
            (df["conta"] == "3.11") & 
            (df["descricao"].str.contains("^lucro", case=False)) &
            (df["data_ini"]=="2025-01-01")
            )
    lucro_liquido = df.loc[filtro, ["valor"]].iloc[0]

    filtro = (
            (df["conta"].str.contains("2.0.", case=False)) & 
            (df["descricao"].str.contains("^patrim", case=False)) 
            )
    pl = df.loc[filtro, ["valor"]].iloc[0]
    roe = lucro_liquido / pl
    roe = roe.iloc[0]
    resultados = {
                "ticker":ticker,
                "roe": roe
        }
    lista_resultado.append(resultados)
    print(ticker, roe)
df_final = pd.DataFrame(lista_resultado)
df_final.sort_values(["roe"])
