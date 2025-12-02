import pandas as pd
import os
import re
from datetime import datetime

# ----------------------------
# 1) Lista de paths (copiados do seu Windows)
# ----------------------------
paths = [
r"C:\Users\dimit\Downloads\cobertura-ab-03-11-2025 (13).xlsx",
r"C:\Users\dimit\Downloads\cobertura-ab-03-11-2025 (12).xlsx",
r"C:\Users\dimit\Downloads\cobertura-ab-03-11-2025 (11).xlsx",
r"C:\Users\dimit\Downloads\cobertura-ab-03-11-2025 (10).xlsx",
r"C:\Users\dimit\Downloads\cobertura-ab-03-11-2025 (9).xlsx",
r"C:\Users\dimit\Downloads\cobertura-ab-03-11-2025 (8).xlsx",
r"C:\Users\dimit\Downloads\cobertura-ab-03-11-2025 (7).xlsx",
r"C:\Users\dimit\Downloads\cobertura-ab-03-11-2025 (6).xlsx",
r"C:\Users\dimit\Downloads\cobertura-ab-03-11-2025 (5).xlsx",
r"C:\Users\dimit\Downloads\cobertura-ab-03-11-2025 (4).xlsx",
r"C:\Users\dimit\Downloads\cobertura-ab-03-11-2025 (3).xlsx",
r"C:\Users\dimit\Downloads\cobertura-ab-03-11-2025 (2).xlsx",
r"C:\Users\dimit\Downloads\cobertura-ab-03-11-2025 (1).xlsx",
r"C:\Users\dimit\Downloads\cobertura-ab-03-11-2025.xlsx"
]

# ----------------------------
# 2) Funções utilitárias
# ----------------------------
month_name_pt = {
    'jan':1,'fev':2,'mar':3,'abr':4,'mai':5,'jun':6,'jul':7,'ago':8,'set':9,'out':10,'nov':11,'dez':12
}

def detect_columns(df):
    """Detect common relevant columns: municipality code, municipality name, coverage abs, coverage pct, period."""
    cols = [c.strip() for c in df.columns]
    cov_abs = None
    cov_pct = None
    cod_mun = None
    nome_mun = None
    period_col = None
    uf_col = None

    for c in cols:
        lc = c.lower()
        if "n° cobertura esf" in lc or "nº cobertura esf" in lc or ("cobertura" in lc and "esf" in lc and any(x in lc for x in ["nº","n°","numero","quant","pop","população","populacao"])):
            cov_abs = c
        if "cobertura esf" in lc and ("%".lower() in lc or "porcent" in lc or "percent" in lc or "percentagem" in lc or re.search(r'\b\d+\,\d+\b', lc) is None):
            # note: lenient detection; prefer explicit pct if present
            if "n°" not in lc and "nº" not in lc and not cov_abs:
                cov_pct = c
            else:
                # keep both possibilities
                if not cov_pct:
                    cov_pct = c
        if any(x in lc for x in ["codigo", "cod ibge", "cod_mun", "cod_municip", "codigo_ibge", "codmun"]):
            cod_mun = c
        if any(x in lc for x in ["municipio", "município", "nome do município", "nome do municipio"]):
            nome_mun = c
        if any(x in lc for x in ["periodo", "referencia", "referência", "mês", "mes", "ano"]):
            period_col = c
        if any(x in lc for x in ["uf", "estado", "unidade federativa"]):
            uf_col = c

    # fallback heuristics
    if not nome_mun:
        for c in cols:
            if "mun" in c.lower():
                nome_mun = c
                break
    if not cov_abs:
        for c in cols:
            if "pop" in c.lower() and "cad" in c.lower():
                cov_abs = c
                break
    if not cov_pct:
        for c in cols:
            if "cobertura" in c.lower() and "esf" in c.lower():
                # avoid choosing a column that contains "n°"
                if "n°" not in c.lower() and "nº" not in c.lower():
                    cov_pct = c
                    break

    return cod_mun, nome_mun, cov_abs, cov_pct, period_col, uf_col

def melt_month_columns(df):
    """
    Detect month columns in wide format (ex.: 'jun/2010', 'jul/2010', 'jun-2010', '2010-06', 'jun/10') and melt to long.
    Returns DataFrame with columns: municipality cols, 'date' and 'value' (string).
    """
    pattern = re.compile(r'(?i)\b(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)[^\d]*\d{2,4}\b|(\d{1,2}[/-]\d{4})|(\d{4}[/-]\d{2})')
    month_cols = [c for c in df.columns if pattern.search(c)]
    if not month_cols:
        return None
    id_cols = [c for c in df.columns if c not in month_cols]
    df_long = df.melt(id_vars=id_cols, value_vars=month_cols, var_name='periodo_col', value_name='valor_mes')
    return df_long

def parse_period_to_year_month(s):
    """Try to parse a variety of period strings into (year, month). Returns (year,int month) or (None,None)."""
    if pd.isna(s):
        return None, None
    s = str(s).strip()
    # common formats: 'jun/2010', 'jun-2010', '06/2010', '2010-06', '2010/06', 'jun/10'
    # try numeric first
    try:
        dt = pd.to_datetime(s, dayfirst=True, errors='coerce')
        if pd.notna(dt):
            return dt.year, dt.month
    except:
        pass
    # textual month month/year e.g., 'jun/2010' or 'jun-2010'
    m = re.search(r'(?i)(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)[^\d]*(\d{2,4})', s)
    if m:
        mon_txt = m.group(1).lower()[:3]
        yr = m.group(2)
        yr = int(yr) if len(yr) == 4 else (2000 + int(yr))
        mon = month_name_pt.get(mon_txt[:3], None)
        return yr, mon
    m2 = re.search(r'(\d{1,2})[/-](\d{4})', s)
    if m2:
        mon = int(m2.group(1))
        yr = int(m2.group(2))
        return yr, mon
    m3 = re.search(r'(\d{4})[/-](\d{1,2})', s)
    if m3:
        yr = int(m3.group(1)); mon = int(m3.group(2))
        return yr, mon
    # fallback: find any 4-digit year and try to guess month from text
    y = re.search(r'(20\d{2})', s)
    if y:
        yr = int(y.group(1))
        # try month name
        for k,v in month_name_pt.items():
            if k in s.lower():
                return yr, v
        return yr, None
    return None, None

# ----------------------------
# 3) Processar cada arquivo
# ----------------------------
rows = []
for path in paths:
    if not os.path.exists(path):
        print("Arquivo não encontrado:", path)
        continue
    print("Processando:", path)
    try:
        xls = pd.ExcelFile(path)
        sheet = xls.sheet_names[0]
        df = pd.read_excel(path, sheet_name=sheet, dtype=str)
    except Exception as e:
        print("Erro ao ler:", path, e)
        continue

    # Strip column names
    df.columns = [c.strip() for c in df.columns]

    cod_mun, nome_mun, cov_abs_col, cov_pct_col, period_col, uf_col = detect_columns(df)

    # if wide monthly format (columns like jun/2010), melt
    melted = melt_month_columns(df)
    if melted is not None:
        # find period column is 'periodo_col' and value is 'valor_mes'
        df_long = melted
        # try to identify value column type: is it absolute or pct? we will attempt to map by column name
        # We'll keep both valor_mes (string) and we will try to coerce numeric.
        # Identify municipality columns (id_vars from melt)
        id_cols = [c for c in df_long.columns if c not in ['periodo_col','valor_mes']]
        # we expect id_cols to include municipality name/code
        for idx, r in df_long.iterrows():
            # build dict for ease
            d = {c: r[c] for c in id_cols}
            period_str = r['periodo_col']
            yr, mon = parse_period_to_year_month(period_str)
            val = r['valor_mes']
            d.update({
                'periodo_raw': period_str,
                'valor_mes': val,
                'year': yr,
                'month': mon,
                'source_file': os.path.basename(path)
            })
            rows.append(d)
    else:
        # long format or already monthly rows
        # If there's a period column, use it; otherwise try detect month info in any column
        if period_col:
            # each row corresponds to a period (probably monthly)
            for idx, r in df.iterrows():
                d = r.to_dict()
                period_val = r.get(period_col, None)
                yr, mon = parse_period_to_year_month(period_val)
                d.update({
                    'periodo_raw': period_val,
                    'year': yr,
                    'month': mon,
                    'source_file': os.path.basename(path)
                })
                rows.append(d)
        else:
            # no explicit period: maybe the file is already aggregated per cycle (single row per municipality)
            # Assign cycle based on filename order possibility: try to extract a year from file content or filename
            # Try to find any year inside the sheet text (very heuristic)
            text_blob = " ".join(df.fillna("").astype(str).values.flatten()[:100].tolist())
            y_search = re.search(r'(20\d{2})', text_blob)
            year_guess = int(y_search.group(1)) if y_search else None
            # assume month = June (start of cycle)
            for idx, r in df.iterrows():
                d = r.to_dict()
                d.update({
                    'periodo_raw': None,
                    'year': year_guess,
                    'month': 6,
                    'source_file': os.path.basename(path)
                })
                rows.append(d)

# ----------------------------
# 4) Montar DataFrame unificado e limpar
# ----------------------------
if not rows:
    raise SystemExit("Nenhum registro extraído. Verifique os arquivos e colunas.")

un = pd.DataFrame(rows)

# Normalize possible municipality column names into 'municipio' and 'cod_municipio'
# Try to pick the best candidate for municipality name and code from columns
possible_mun_cols = [c for c in un.columns if any(x in c.lower() for x in ["municipio","município","nome do município","nome_municipio","nome"])]
possible_cod_cols = [c for c in un.columns if any(x in c.lower() for x in ["cod","codigo","codigo_ibge","ibge"])]

# create municipio column if possible
if possible_mun_cols:
    un['municipio'] = un[possible_mun_cols[0]].astype(str)
elif possible_cod_cols:
    un['municipio'] = un[possible_cod_cols[0]].astype(str)
else:
    # fallback to first non-system column
    other_cols = [c for c in un.columns if c not in ['periodo_raw','year','month','valor_mes','source_file']]
    if other_cols:
        un['municipio'] = un[other_cols[0]].astype(str)
    else:
        raise SystemExit("Não foi possível identificar coluna de município automaticamente.")

# bring coverage absolute and pct into normalized numeric columns if they exist
# Search in original columns for common names
cov_abs_candidates = [c for c in un.columns if "cobertura" in c.lower() and "esf" in c.lower() and any(x in c.lower() for x in ["n","nº","n°","numero","quant","pop","população","populacao"])]
cov_pct_candidates = [c for c in un.columns if "cobertura" in c.lower() and "esf" in c.lower() and not any(x in c.lower() for x in ["n","nº","n°","numero","quant","pop","população","populacao"])]

# map if exist
if cov_abs_candidates:
    un['cobertura_abs_raw'] = un[cov_abs_candidates[0]]
elif 'valor_mes' in un.columns:
    un['cobertura_abs_raw'] = un['valor_mes']
else:
    un['cobertura_abs_raw'] = None

if cov_pct_candidates:
    un['cobertura_pct_raw'] = un[cov_pct_candidates[0]]
else:
    # try to see if valor_mes looks like percent (contains % or comma)
    un['cobertura_pct_raw'] = un['valor_mes']

# coerce numeric (replace commas, dots, percent sign)
def to_number(x):
    if pd.isna(x): return None
    s = str(x).strip()
    s = s.replace('.', '').replace('%', '').replace(' ', '')
    s = s.replace(',', '.')
    s = re.sub(r'[^\d\.-]', '', s)
    try:
        return float(s)
    except:
        return None

un['cobertura_abs'] = un['cobertura_abs_raw'].apply(to_number)
un['cobertura_pct'] = un['cobertura_pct_raw'].apply(to_number)

# compute cycle year according to rule A: June YYYY -> May YYYY+1 assigned to YYYY
# For each row with year,month:
def cycle_year_from_row(y, m):
    if pd.isna(y) or y is None:
        return None
    if m is None:
        return y
    try:
        m = int(m)
    except:
        return y
    if 6 <= m <= 12:
        return int(y)
    else:
        # months 1..5 belong to previous year's cycle
        return int(y) - 1

un['cycle_year'] = un.apply(lambda r: cycle_year_from_row(r.get('year'), r.get('month')), axis=1)

# Drop rows without cycle_year or without municipio
un = un[un['cycle_year'].notna()]
un = un[un['municipio'].notna()]

# ----------------------------
# 5) Agregar por municipio x cycle_year (média dos meses dentro do ciclo)
# ----------------------------
grouped = un.groupby(['municipio','cycle_year']).agg(
    cobertura_abs_mean = ('cobertura_abs','mean'),
    cobertura_abs_median = ('cobertura_abs','median'),
    cobertura_pct_mean = ('cobertura_pct','mean'),
    registros = ('cobertura_abs','count')
).reset_index()

# Some municipalities might have NaN coverage if read failed; keep them but mark
grouped['cobertura_abs_mean'] = grouped['cobertura_abs_mean'].round(2)
grouped['cobertura_pct_mean'] = grouped['cobertura_pct_mean'].round(2)

# ----------------------------
# 6) Determinar ano de adesão = primeiro cycle_year com cobertura_abs_mean > 0
# ----------------------------
adesao = grouped[grouped['cobertura_abs_mean'].notna()].copy()
adesao = adesao[adesao['cobertura_abs_mean'] > 0]
first = adesao.sort_values(['municipio','cycle_year']).groupby('municipio').first().reset_index()
first = first[['municipio','cycle_year']].rename(columns={'cycle_year':'ano_adesao',})
# municipalities without any positive coverage will be NaN (never adopted in sample)

# ----------------------------
# 7) Salvar outputs
# ----------------------------
out_panel = os.path.join(os.getcwd(), 'painel_esf_sergipe.csv')
out_adesao = os.path.join(os.getcwd(), 'adesao_esf_sergipe.csv')

grouped.to_csv(out_panel, index=False, encoding='utf-8-sig')
first.to_csv(out_adesao, index=False, encoding='utf-8-sig')

print("Painel salvo em:", out_panel)
print("Adesão salvo em:", out_adesao)
print("Linhas painel:", grouped.shape[0], "Municípios com adesão encontrada:", first.shape[0])
