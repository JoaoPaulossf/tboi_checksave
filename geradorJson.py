import json

arquivo = open("itens.txt", "r")
conteudo = arquivo.read()

dados = {"personagens": {}}

for linha in conteudo.strip().split("\n"):

    if not linha or " - " not in linha:
        continue
    
    nome, itens_texto = linha.split(" - ")
    nome = nome.lower()


    lista_itens = [item.strip() for item in itens_texto.split(",")]

    dados["personagens"][nome] = {
        "desbloqueado" : False,
        "itens": {},
        "marcas" : {
            "boss rush" : False,
            "mom's heart" : False,
            "satan" : False,
            "isaac" : False,
            "the lamb" : False,
            "???" : False,
            "ultra greed" : False,
            "ultra greedier" : False,
            "hush" : False,
            "delirium" : False,
            "mother" : False,
            "the beast" : False,
            "mega satan" : False
        },
        "all marks" : False,
    }

    for item in lista_itens:
        if not item or " | " not in item:
            continue
        nomeItem, requisito = item.split(" | ")
        dados["personagens"][nome]["itens"][nomeItem] = {
            "desbloqueado" : False,
            "requisito" : requisito.lower(),
        }

with open("isaac_save.json", "w", encoding="utf-8") as arquivo:
    json.dump(dados, arquivo, indent=4, ensure_ascii=False)

print("Arquivo criado!")