import json
import sqlite3
from main import *

with open("isaac_save.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)
        
conn = sqlite3.connect("database/isaac.db")

cursor = conn.cursor()

personagens = listarPersonagens(dados)

boss = exibirProgresso("Isaac", dados)

for nome, desbloqueio in personagens:
    #preenchimento da tabela personagem
    cursor.execute(
        "INSERT INTO personagem(nome, desbloqueado) VALUES(?, ?)",(nome, desbloqueio)
    )
    conn.commit()

    idPersonagem  = cursor.execute(
        "SELECT id FROM personagem WHERE nome = ?",(nome)
    )
    
    #listagem de itens do personagem "nome"
    itens, situacao, requisito = listarItens(nome,dados)
    for item in itens:
        cursor.execute(
            "INSERT INTO item(nome) VALUES(?)",(item)
        )
        conn.commit()

        idItem  = cursor.execute(
            "SELECT id FROM personagem WHERE nome = ?",(nome)
        )


for marca in boss:
    cursor.execute(
        "INSERT INTO boss (nome) VALUES(?)",(marca)
    )

    conn.commit()
