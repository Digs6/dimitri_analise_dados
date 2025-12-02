import pandas as pd
import os
import statsmodels.api as sm
import matplotlib.pyplot as plt

# ================================
# 1. LER MORTALIDADE
# ================================
df_mort = pd.read_csv("mortalidade_infantil_sp_mensal_2008_2020.csv")

# ================================
# 2. LER NASCIDOS VIVOS
# ================================
df_nv = pd.read_csv("nascidos_vivos_sp_mensal_2008_2020.csv")

# ================================
# 3. LER COBERTURA ESF
# ================================
import pandas as pd
import statsmodels.api as sm

# ================================
# 1. LER OS ARQUIVOS PRONTOS
# ================================

mort = pd.read_csv("mortalidade_infantil_sp_mensal_2008_2020.csv")
nv   = pd.read_csv("nascidos_vivos_sp_mensal_2008_2020.csv")
esf  = pd.read_csv("cobertura_esf_sp_2008_2020.csv")   # se ainda não salvou, me avise

print("Mortalidade:", mort.head())
print("Nascidos:", nv.head())
print("ESF:", esf.head())


# ================================
# 2. CRIAR COLUNA DATA (YYYY-MM)
# ================================

mort["data"] = pd.to_datetime(dict(year=mort["ano"], month=mort["mes"], day=1))
nv["data"]   = pd.to_datetime(dict(year=nv["ano"], month=nv["mes"], day=1))

# ================================
# 3. JUNTAR MORTALIDADE + NASCIDOS
# ================================

df = pd.merge(mort, nv, on="data", how="inner")

# ================================
# 4. CRIAR TAXA DE MORTALIDADE INFANTIL
# ================================

df["taxa_mortalidade_infantil"] = (df["obitos_infantis"] / df["nascidos_vivos"]) * 1000

print("\n✅ Base mensal (mort + nasc):")
print(df.head())


# ================================
# 5. JUNTAR COM A ESF (ANUAL)
# ================================

df["ano"] = df["data"].dt.year
df = pd.merge(df, esf, on="ano", how="left")

print("\n✅ Base completa (com ESF):")
print(df.head())


# ================================
# 6. LIMPAR DADOS FINAIS
# ================================

df_final = df[[
    "data",
    "ano",
    "mes",
    "obitos_infantis",
    "nascidos_vivos",
    "taxa_mortalidade_infantil",
    "cobertura_esf"
]].dropna()

print("\n✅ Base final para regressão:")
print(df_final.head())
print("\nNúmero de observações:", df_final.shape[0])


# ================================
# 7. REGRESSÃO LINEAR (OLS)
# ================================

Y = df_final["taxa_mortalidade_infantil"]
X = df_final[["cobertura_esf"]]

X = sm.add_constant(X)

modelo = sm.OLS(Y, X).fit()

print("\n✅ RESULTADO DA REGRESSÃO:")
print(modelo.summary())
