
dic = {
    "Nome":"Laerte",
    "Idade":19,
    "email":"dimitrigollovitz@gmail.com"
}

dic["email"]
dic["Nome"]
dic["Idade"]

import pandas as pd
pd.DataFrame({dic})

import requests as rq
cep = "70844070"
url = f"https://viacep.com.br/ws/{cep}/json/"
response = rq.get(url)
response.json()

url = f"http://www.ipeadata.gov.br/api/odata4/Metadados"
response = rq.get(url)
Metadados = response.json()
Metadados = Metadados["value"]
df = pd.DataFrame(Metadados)

SERCODIGO = "ADH_PESHOTOT_BRA"
url = f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{SERCODIGO}')"
response = rq.get(url)
response.json()

SERCODIGO = "HOMIC"
url = f"http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='{SERCODIGO}')"
response = rq.get(url)
dados = response.json()
dados = dados ["value"]
df = pd.DataFrame(dados)
df.shape
df.columns
df.info()
df["VALDATA"] = pd.to_datetime(df["VALDATA"], errors="coerce")
df["VALDATA"] = df["VALDATA"].dt.year
df["VALDATA"].unique()
filtro = df["NIVNOME"]=="Brasil"
df_brasil = df.loc[filtro]
df_brasil[["VALDATA","VALVALOR"]].plot()

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# Plot
ax = df_brasil[["VALDATA", "VALVALOR"]].plot(x="VALDATA", y="VALVALOR", legend=False)
# Formatação do eixo X
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))  # ou '%Y-%m-%d' conforme sua preferência
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()