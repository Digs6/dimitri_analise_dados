import pandas as pd
import glob
import os
import re

pasta = r"C:\Users\dimit\Documents\analise_dados\mortalidade_infantil_sp_2008_2020\*.csv"

arquivos = sorted(glob.glob(pasta))
print("Arquivos encontrados:", arquivos)

linhas_finais = []

for arq in arquivos:
    nome = os.path.basename(arq)
    print("\nLendo:", nome)

    # 1. Ler arquivo inteiro como texto
    with open(arq, "r", encoding="latin1", errors="replace") as f:
        linhas = f.readlines()

    # 2. Encontrar a linha com os valores (contém 'SAO PAULO' e ;)
    linha_valores = None

    for l in linhas:
        if "SAO PAULO" in l and ";" in l:
            linha_valores = l
            break

    if linha_valores is None:
        print("❌ Não encontrei linha de dados em", nome)
        continue  # <-- AGORA está dentro do for corretamente

    # 3. Separar por ';'
    partes = linha_valores.replace('"', "").strip().split(";")

    # formato esperado: municipio + 12 meses + total = 14 colunas
    if len(partes) < 14:
        print("⚠ Formato inesperado em", nome, "->", partes)
        continue

    municipio = partes[0]
    valores = partes[1:13]  # 12 meses

    valores_limpos = []
    for v in valores:
        v = v.replace(".", "").replace(",", "")
        try:
            valores_limpos.append(int(v))
        except:
            valores_limpos.append(None)

    # 4. Extrair ano do nome do arquivo
    numeros = re.findall(r"20\d{2}", nome)
    if len(numeros) == 0:
        print("⚠ Não achei ano no nome do arquivo:", nome)
        continue

    ano = int(numeros[0])

    # 5. Criar linhas mensais
    for mes, morte in enumerate(valores_limpos, start=1):
        linhas_finais.append({
            "ano": ano,
            "mes": mes,
            "obitos_infantis": morte
        })

# 6. Criar dataframe final
df_mort = pd.DataFrame(linhas_finais)
df_mort = df_mort.sort_values(["ano", "mes"]).reset_index(drop=True)

# 7. Salvar
df_mort.to_csv("mortalidade_sp_mensal_2008_2020.csv", index=False, encoding="utf-8-sig")

print("\n✅ ARQUIVO FINAL CRIADO: mortalidade_sp_mensal_2008_2020.csv")
print(df_mort.head(24))
