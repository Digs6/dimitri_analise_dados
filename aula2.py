import pandas as pd
df = pd.read_csv("C:/Users/dimit/Documents/analise_dados/imoveis_brasil.csv")
df.shape
df.columns
df.head(5)
df.tail(5)
df.sample(5)
df.info()

#exercicio verificar imoveis
df["Tipo_Imovel"].unique()
filtro = df["Valor_Imovel"] > 1000000
df_1M = df.loc[filtro]
df2 = df[["Cidade", "Bairro","Valor_Imovel"]]
df.sort_values(["Valor_Imovel"],ascending=True)
df["Valor_Imovel"].mean()
df["Tipo_Imovel"].unique()
filtro = df["Cidade"] == "Curitiba"
df.loc[filtro, ["Valor_Imovel"]].mean()
valor_medio_geral = df["Valor_Imovel"].mean()
filtro = df["Valor_Imovel"] > valor_medio_geral
df_maior = df.loc[filtro]
len(df_maior)
filtro = df["Valor_Imovel"] < valor_medio_geral
df_menor = df.loc[filtro]
len(df_menor)