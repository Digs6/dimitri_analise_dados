import pandas as pd 
arquivo = "C:\\Users\\dimit\\Documents\\analise_dados\\titanic.csv"
df = pd.reaf_csv(arquivo)
df.shape
df.columms
df.info()
df.isna().sum()

filtro = df["Fare"].isna()
df.loc[filtro]

filtro = df ["Age"].isna()
df.loc[filtro]
media_idade = df["Age"].mean()
df["Age"] = df["Age"].fillna(media_idade)

filtro = df["Sex"]=="male"
df_homem = df.loc[filtro]
df_homem["Age"].mean()

filtro = df["Sex"]=="female"
df_mulher = df.loc[filtro]
df_mulher["Age"].mean()

df.groupby("Sex")["Age"].mean()

filtro = (df{"Sex"}=="male") & ()