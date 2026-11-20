import requests
from bs4 import BeautifulSoup
import sqlite3
import json
import re

URL_API = "https://bindingofisaacrebirth.wiki.gg/api.php"
headers = {
    "User-Agent": "IsaacDBBuilder/1.0 (linkmagnofxd@gmail.com)"
}

def limparTexto(texto):
    # Remove sujeiras de formatação HTML
    texto = texto.replace("\u200d", "").replace("\xa0", " ")
    return re.sub(r"\s+", " ", texto).strip()

def buscarQualidadesItem():
    params = {
        "action": "parse",
        "page": "Items",
        "format": "json",
        "prop": "text"
    }

    response = requests.get(URL_API, params=params, headers=headers).json()
    html_limpo = response["parse"]["text"]["*"]
    soup = BeautifulSoup(html_limpo, "html.parser")

    qualidades = {}

    for tabela in soup.find_all("table", class_="wikitable"):
        linhas = tabela.find_all("tr")
        for linha in linhas[1:]:  # Ignora o cabeçalho
            colunas = linha.find_all(["td", "th"])
            if len(colunas) >= 5:
                nome = limparTexto(colunas[0].get_text()).lower()
                qual_texto = limparTexto(colunas[-1].get_text())
                if qual_texto.isdigit():
                    qualidades[nome] = int(qual_texto)
    return qualidades

print(buscarQualidadesItem())