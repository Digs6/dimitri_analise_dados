import statsmodels.api as sm
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

#dataset de gorjetas
df = sns.load_dataset("tips")
df.head()
df["time"].unique()
df["day"].unique
X = df["total_bill"]#variavel independente
y = df["tip"]#variavel dependente

#constante
x = sm.add_constant(X)
modelo = sm.OLS(y, X).fit()
print(modelo.summary())

#regressao linear multipla
X = df[["total_bill", "size"]]
y = df["tip"]#variavel dependente

#constante
x = sm.add_constant(X)
modelo = sm.OLS(y, X).fit()
print(modelo.summary())
modelo.params
modelo.pvalues
modelo.rsquared
modelo.rsquared_adj

#previsao de modelo
pred = modelo.predict()
comparacao = pd.DataFrame({
    "real": df["tip"],
    "calculada": pred
})
comparacao["residuos"] = comparacao["real"] - comparacao["calculada"]
sns.scatterplot(x=modelo.predict(), y=comparacao["residuos"])
plt.axhline(0, color='red', linestyle="--")