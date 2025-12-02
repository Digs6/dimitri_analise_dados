import os

pasta_nv = r"C:\Users\dimit\Documents\analise_dados\nascidos_vivos_sp_2008_2020"
print(sorted(os.listdir(pasta_nv)))

arquivo = r"C:\Users\dimit\Documents\analise_dados\nascidos_vivos_sp_2008_2020\nascidos_vivos_sp_2008.csv"

with open(arquivo, "r", encoding="latin1", errors="replace") as f:
    for i in range(30):
        line = f.readline()
        if not line:
            break
        print(f"{i+1:02d} | {line.rstrip()}")
