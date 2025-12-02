import pandas as pd
import glob
import os
import re

pasta = r"C:\Users\dimit\Documents\analise_dados\mortalidade_infantil_sp_2008_2020"
arquivos = sorted(glob.glob(pasta + "/*.csv"))

linhas_finais = []

for arq in arquivos:

    nome = os.path.basename(arq)
    print("\n📄 Lendo:", nome)

    # Extrai ano do nome
    ano = int(re.findall(r"20\d{2}", nome)[0])

    # Lê todas as linhas do arquivo
    with open(arq, "r", encoding="latin1", errors="replace") as f:
        linhas = [l.strip() for l in f.readlines()]

    # Procura linha que contém os dados (linha com município)
    linha_valores = None
    for l in linhas:
        # A linha CERTEIRA sempre começa com "355030 SAO PAULO"
        if l.startswith('"355030 SAO PAULO"') or l.startswith("355030 SAO PAULO"):
            linha_valores = l
            break

    if linha_valores is None:
        print("❌ Não encontrei linha de valores!")
        print("Arquivo:", nome)
        continue

    # Limpa e separa valores
    partes = linha_valores.replace('"', "").split(";")

    # partes[0] = nome, as demais são os meses
    valores_meses = partes[1:13]   # janeiro → dezembro

    # Garante que são números
    valores_meses = [int(v.replace(".", "").replace(",", "")) for v in valores_meses]

    # Mapa mês
    mapa_mes = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
        5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
        9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
    }

    # Salva no formato final
    for i, valor in enumerate(valores_meses, start=1):
        linhas_finais.append({
            "ano": ano,
            "mes": i,
            "obitos_infantis": valor
        })

# Criar DataFrame final
df_mort = pd.DataFrame(linhas_finais)
df_mort = df_mort.sort_values(["ano", "mes"]).reset_index(drop=True)

# Exportar
df_mort.to_csv("mortalidade_infantil_sp_mensal_2008_2020.csv", index=False, encoding="utf-8-sig")

print("\n✅ Arquivo final salvo: mortalidade_infantil_sp_mensal_2008_2020.csv")
print(df_mort.head(20))
