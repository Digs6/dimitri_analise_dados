from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# --- Configurações ---
url = "https://www.dfimoveis.com.br/"
driver = webdriver.Chrome()
driver.get(url)
wait = WebDriverWait(driver, 15)

# --- Seleciona tipo de negócio: VENDA ---
botao_negocio = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@aria-labelledby='select2-negocios-container']")))
botao_negocio.click()
opcao_venda = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(translate(., 'venda', 'VENDA'), 'VENDA')]")))
opcao_venda.click()
print("✔ Tipo de negócio: VENDA")

# --- Seleciona tipo de imóvel: APARTAMENTO ---
botao_tipo = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@aria-labelledby='select2-tipos-container']")))
botao_tipo.click()
opcao_apto = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(translate(., 'apartamento', 'APARTAMENTO'), 'APARTAMENTO')]")))
opcao_apto.click()
print("✔ Tipo de imóvel: APARTAMENTO")

# --- Seleciona cidade: ÁGUAS CLARAS ---
botao_cidade = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@aria-labelledby='select2-cidades-container']")))
botao_cidade.click()
opcao_cidade = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(translate(., 'aguas claras', 'AGUAS CLARAS'), 'AGUAS CLARAS')]")))
opcao_cidade.click()
print("✔ Cidade: ÁGUAS CLARAS")

# --- Clica em Buscar ---
botao_buscar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Buscar Imóvel')]")))
botao_buscar.click()
print("🔎 Buscando imóveis...")
time.sleep(5)

# --- Coleta os resultados ---
imoveis = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.property-list__item")))

dados = []
for imovel in imoveis:
    try:
        titulo = imovel.find_element(By.CSS_SELECTOR, "h2.property-list__title").text
    except:
        titulo = None
    try:
        preco = imovel.find_element(By.CSS_SELECTOR, "span.price").text
    except:
        preco = None
    try:
        endereco = imovel.find_element(By.CSS_SELECTOR, "p.property-list__address").text
    except:
        endereco = None
    try:
        link = imovel.find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        link = None

    dados.append({
        "Título": titulo,
        "Preço": preco,
        "Endereço": endereco,
        "Link": link
    })

# --- Cria DataFrame ---
df = pd.DataFrame(dados)
print("✅ Dados coletados com sucesso!")
print(df.head())

# (opcional) salvar em CSV
df.to_csv("imoveis_aguas_claras.csv", index=False, encoding="utf-8-sig")

driver.quit()
