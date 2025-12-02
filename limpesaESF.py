import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np


# 1. Ler os três arquivos já prontos
df_mort = pd.read_csv("mortalidade_infantil_sp_mensal_2008_2020.csv")
df_nv   = pd.read_csv("nascidos_vivos_sp_mensal_2008_2020.csv")
df_esf  = pd.read_csv("cobertura_esf_sp_mensal_2008_2020.csv")

# 2. Juntar tudo
df = df_mort.merge(df_nv, on=["ano","mes"])
df = df.merge(df_esf, on=["ano","mes"])

print("✅ Dados combinados:")
print(df.head())

# 3. Criar taxa de mortalidade infantil (por 1.000 nascidos vivos)
df["taxa_mortalidade"] = (df["obitos_infantis"] / df["nascidos_vivos"]) * 1000

print("\n✅ Taxa criada")
print(df[["ano","mes","taxa_mortalidade","cobertura_esf"]].head())

# 4. REGRESSÃO
# y = taxa de mortalidade
# x = cobertura ESF

X = df[["cobertura_esf"]]
X = sm.add_constant(X)

y = df["taxa_mortalidade"]

modelo = sm.OLS(y, X).fit()

# 5. RESULTADO
print("\n✅ RESULTADO DA REGRESSÃO")
print(modelo.summary())

import pandas as pd

# Ler os arquivos já gerados
mort = pd.read_csv("mortalidade_infantil_sp_mensal_2008_2020.csv")
nasc = pd.read_csv("nascidos_vivos_sp_mensal_2008_2020.csv")
esf  = pd.read_csv("cobertura_esf_sp_mensal_2008_2020.csv")

# Conferir colunas
print(mort.columns)
print(nasc.columns)
print(esf.columns)

# Juntar mortalidade com nascidos
df_final = pd.merge(mort, nasc, on=["ano","mes"], how="inner")

# Juntar com cobertura da ESF
df_final = pd.merge(df_final, esf, on=["ano","mes"], how="inner")

# Criar taxa de mortalidade por mil nascidos vivos
df_final["taxa_mortalidade"] = (df_final["obitos_infantis"] / df_final["nascidos_vivos"]) * 1000

# Conferir se deu certo
print(df_final.head(12))
print("\nFormato final:")
print(df_final.info())

import matplotlib.pyplot as plt
import numpy as np

# X e Y
x = df_final["cobertura_esf"]
y = df_final["taxa_mortalidade"]

# Estimar a linha de regressão
coef = np.polyfit(x, y, 1)
linha = np.poly1d(coef)

# Criar gráfico
plt.figure()
plt.scatter(x, y)
plt.plot(x, linha(x))
plt.xlabel("Cobertura da ESF (%)")
plt.ylabel("Taxa de mortalidade infantil (por mil NV)")
plt.title("Relação entre Cobertura da ESF e Mortalidade Infantil – São Paulo (2008–2020)")
plt.show()

df_final["data"] = pd.to_datetime(dict(year=df_final.ano, month=df_final.mes, day=1))

plt.figure()
plt.plot(df_final["data"], df_final["taxa_mortalidade"])
plt.xlabel("Ano")
plt.ylabel("Taxa de mortalidade infantil")
plt.title("Evolução da mortalidade infantil em São Paulo (2008–2020)")
plt.show()

plt.figure()
plt.plot(df_final["data"], df_final["cobertura_esf"])
plt.xlabel("Ano")
plt.ylabel("Cobertura da ESF (%)")
plt.title("Evolução da cobertura da ESF em São Paulo (2008–2020)")
plt.show()

# normalizar entre 0 e 1 (só para o gráfico)
df_final["mort_norm"] = (df_final["taxa_mortalidade"] - df_final["taxa_mortalidade"].min()) / (df_final["taxa_mortalidade"].max() - df_final["taxa_mortalidade"].min())
df_final["esf_norm"] = (df_final["cobertura_esf"] - df_final["cobertura_esf"].min()) / (df_final["cobertura_esf"].max() - df_final["cobertura_esf"].min())

import matplotlib.pyplot as plt

serie_anual = df_final.groupby("ano")["taxa_mortalidade"].mean()
plt.figure()
plt.plot(serie_anual.index, serie_anual.values)
plt.xlabel("Ano")
plt.ylabel("Taxa de mortalidade infantil (por mil NV)")
plt.title("Evolução da mortalidade infantil - São Paulo (2008–2020)")
plt.show()

esf_anual = df_final.groupby("ano")["cobertura_esf"].mean()
plt.figure()
plt.bar(esf_anual.index, esf_anual.values)
plt.xlabel("Ano")
plt.ylabel("Cobertura ESF (%)")
plt.title("Cobertura da Estratégia Saúde da Família - São Paulo (2008–2020)")
plt.show()

x = df_final["cobertura_esf"]
y = df_final["taxa_mortalidade"]
coef = np.polyfit(x, y, 1)
linha = np.poly1d(coef)
plt.figure()
plt.scatter(x, y)
plt.plot(x, linha(x))
plt.xlabel("Cobertura ESF (%)")
plt.ylabel("Taxa de mortalidade infantil (por mil NV)")
plt.title("Relação entre ESF e Mortalidade Infantil - São Paulo")
plt.show()

mort_anual = df_final.groupby("ano")["taxa_mortalidade"].mean()
plt.figure()
plt.bar(mort_anual.index, mort_anual.values)
plt.xlabel("Ano")
plt.ylabel("Taxa de mortalidade infantil (por mil NV)")
plt.title("Mortalidade infantil por ano - São Paulo (2008–2020)")
plt.show()
