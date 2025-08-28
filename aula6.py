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
