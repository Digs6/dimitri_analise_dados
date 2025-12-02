import pandas as pd
import glob
import os
import re

# ====== PASTA DOS CSV DE NASCIDOS VIVOS ======
pasta = r"C:\Users\dimit\Documents\analise_dados\nascidos_vivos_sp_2008_2020\*.csv"
# =============================================

arquivos = glob.glob(pasta)
print("Arquivos encontrados:", len(arquivos))

if len(arquivos) == 0:
    raise SystemExit("❌ Nenhum arquivo encontrado.")

# Mapeamento de meses
meses_map = {
    "janeiro":1,"fevereiro":2,"marco":3,"março":3,
    "abril":4,"maio":5,"junho":6,"julho":7,
    "agosto":8,"setembro":9,"outubro":10,
    "novembro":11,"dezembro":12
}

linhas_final = []

for arquivo in sorted(arquivos):
    nome = os.path.basename(arquivo)
    print(f"\n📌 Processando: {nome}")

    # === descobrir o ano pelo nome ===
    ano = re.findall(r'20\d{2}', nome)
    ano = int(ano[0]) if ano else None

    # === ler arquivo pulando primeiras 4 linhas ===
    df = pd.read_csv(
        arquivo,
        sep=";",
        encoding="latin1",
        skiprows=4,
        names=["mes", "nascidos_vivos"]
    )

    # remover linhas “Total”
    df = df[~df["mes"].str.contains("Total", case=False, na=False)]

    # converter mes para número
    df["mes"] = df["mes"].str.strip().str.lower()
    df["mes"] = df["mes"].map(meses_map)

    # remover linhas sem mês numérico
    df = df.dropna(subset=["mes"])

    # converter valores
    df["nascidos_vivos"] = (
        df["nascidos_vivos"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    df["nascidos_vivos"] = pd.to_numeric(df["nascidos_vivos"], errors="coerce")

    # adicionar ano e município
    df["ano"] = ano
    df["municipio"] = "São Paulo"

    linhas_final.append(df)

# === unir tudo ===
df_nv = pd.concat(linhas_final, ignore_index=True)
df_nv = df_nv.sort_values(["ano", "mes"])

# === salvar arquivos finais ===
df_nv.to_csv("nascidos_vivos_mensal_sp_2008_2020.csv", index=False, encoding="utf-8-sig")

df_nv_anual = df_nv.groupby("ano", as_index=False)["nascidos_vivos"].sum()
df_nv_anual.to_csv("nascidos_vivos_anual_sp_2008_2020.csv", index=False, encoding="utf-8-sig")

print("\n✅ Arquivos criados:")
print(" - nascidos_vivos_mensal_sp_2008_2020.csv")
print(" - nascidos_vivos_anual_sp_2008_2020.csv")

print("\nExemplo:")
print(df_nv.head(15))
