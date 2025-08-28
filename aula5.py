import pandas as pd 
file = "C:\\Users\\dimit\\Documents\\analise_dados\\cadastro_alunos.xlsx"
df = pd.read_excel(file)
filtro = df["nome_aluno"].str.contains("ana", case=False)
df.loc[filtro]

import request as rq
url = f"http://www.ipeadata.gov.br/api/odata4/Metadados"
response = request.get(url)
Metadados = response.json()
Metadados = Metadados["value"]
df = pd.DataFrame(Metadados)
filtro = df["SERNOME"].str.contains("educação", case=False)
df.loc[filtro,{"SERNOME"}].values

import requests
import json

uri = 'https://api.football-data.org/v4/matches'
headers = { 'X-Auth-Token': 'UR_TOKEN' }

response = requests.get(uri, headers=headers)
for match in response.json()['matches']:
  print match