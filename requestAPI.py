import requests
from bs4 import BeautifulSoup

import json

url = "https://bindingofisaacrebirth.wiki.gg/api.php"
params = {
    "action": "parse",
    "page": "Completion_Marks",
    "format": "json",
    "prop": "text"
}
headers = {
    "User-Agent": "IsaacSaveTrackerProject/1.0 (linkmagnofxd@gmail.com)"
}

response = requests.get(url, params=params, headers=headers).json()
html_limpo = response["parse"]["text"]["*"]
soup = BeautifulSoup(html_limpo, "html.parser")

tabelas = soup.find_all("table", class_="wikitable")

dados_extraidos = []

for idx, tabela in enumerate(tabelas):
    linhas = tabela.find_all("tr")

    cabecalhos = [th.get_text(strip=True) for th in linhas[0].find_all("th")]

    registros_tabela = []

    for linha in linhas[1:]:  # Ignora o cabeçalho
        colunas = [td.get_text(strip=True) for td in linha.find_all(["td", "th"])]
        if colunas:
            registros_tabela.append(colunas)

    dados_extraidos.append({
        "tabela": idx,
        "colunas": cabecalhos,
        "amostra_linhas": registros_tabela[:3],
        "total_linhas": len(registros_tabela)
    })

with open("inspecao_wiki.json", "w", encoding="utf-8") as f:
    json.dump(dados_extraidos, f, indent=4, ensure_ascii=False)

print("Arquivo 'inspecao_wiki.json' criado com sucesso!")