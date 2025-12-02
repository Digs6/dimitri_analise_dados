import pandas as pd
import glob
import os
import re

pasta = r"C:\Users\dimit\Documents\analise_dados\nascidos_vivos_sp_2008_2020\*.csv"

arquivos = sorted(glob.glob(pasta))
print("Arquivos encontrados:", arquivos)

linhas_finais = []

for arq in arquivos:
    nome = os.path.basename(arq)
    print("\nLendo:", nome)

    # 1. Ler arquivo inteiro como texto
    with open(arq, "r", encoding="latin1", errors="replace") as f:
        linhas = f.readlines()

    # 2. Encontrar a linha com valores (ex: "Janeiro";14155)
    linha_janeiro = None

    for l in linhas:
        if "Janeiro" in l and ";" in l:
            linha_janeiro = l
            break

    if linha_janeiro is None:
        print("❌ Não encontrei linha com Janeiro em", nome)
        continue

    # 3. Achar todas as linhas de meses
    meses_linhas = []
    for l in linhas:
        if ";" in l and any(m in l for m in
            ["Janeiro","Fevereiro","Marco","Abril","Maio","Junho",
             "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]):
            meses_linhas.append(l)

    # se encontrou menos de 12 meses, formato errado
    if len(meses_linhas) < 12:
        print("⚠ Formato inesperado em", nome)
        continue

    # 4. Extrair ano do arquivo (ex: 2008)
    numeros = re.findall(r"20\d{2}", nome)
    if len(numeros) == 0:
        print("⚠ Não achei o ano no nome do arquivo:", nome)
        continue

    ano = int(numeros[0])

    # 5. Dicionário para transformar nomes → número do mês
    mapa_mes = {
        "Janeiro":1, "Fevereiro":2, "Marco":3, "Abril":4, "Maio":5, "Junho":6,
        "Julho":7, "Agosto":8, "Setembro":9, "Outubro":10, "Novembro":11, "Dezembro":12
    }

    # 6. Ler mês a mês
    for linha in meses_linhas:
        partes = linha.replace('"',"").strip().split(";")
        mes_nome = partes[0]
        nascidos = partes[1]

        if mes_nome == "Total":
            continue

        mes_num = mapa_mes[mes_nome]

        # converter valor
        nascidos = int(nascidos.replace(".","").replace(",",""))

        linhas_finais.append({
            "ano": ano,
            "mes": mes_num,
            "nascidos_vivos": nascidos
        })

# 7. Criar DataFrame final
df_nv = pd.DataFrame(linhas_finais)
df_nv = df_nv.sort_values(["ano","mes"]).reset_index(drop=True)

# 8. Salvar
df_nv.to_csv("nascidos_vivos_sp_mensal_2008_2020.csv", index=False, encoding="utf-8-sig")

print("\n✅ ARQUIVO FINAL CRIADO: nascidos_vivos_sp_mensal_2008_2020.csv")
print(df_nv.head(24))
