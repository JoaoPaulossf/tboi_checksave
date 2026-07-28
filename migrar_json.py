import json
import sqlite3
from main import *

with open("isaac_save.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)
        
conn = sqlite3.connect("database/isaac.db")

cursor = conn.cursor()

personagens = listarPersonagens(dados)

marcas,estados = exibirProgresso("isaac", dados)

print(marcas)

for marca in marcas:
    cursor.execute(
        "INSERT INTO boss (nome) VALUES(?)",(marca,)
    )
    cursor.execute("SELECT nome FROM boss")
    print(cursor.fetchall())

for nome, desbloqueio in personagens:
    #preenchimento da tabela personagem
    cursor.execute(
        "INSERT INTO personagem(nome, desbloqueado) VALUES(?, ?)",(nome, desbloqueio)
    )
    idPersonagem  = cursor.lastrowid
    
    #listagem de itens do personagem "nome"
    itens, situacao, requisito = listarItens(nome,dados)
    i = 0
    for item in itens:
        cursor.execute(
            "INSERT INTO item(nome) VALUES(?)",(item,)
        )
        idItem = cursor.lastrowid

        requisitos = [r.strip() for r in requisito[i].split("+")]
        for boss in requisitos:
            cursor.execute(
                "SELECT id FROM boss WHERE nome = ?",
                (boss,)
            )
            resultado = cursor.fetchone()

            if resultado is None:
                raise ValueError(f'Boss "{requisito[i]}" não encontrado.')

            idRequisito = resultado[0]

            cursor.execute(
                "INSERT INTO unlock(personagem_id, item_id, boss_id) VALUES(?, ?, ?)",(idPersonagem,idItem,idRequisito)
            )
            
        marcas, situacao = exibirProgresso(nome,dados)

        j = 0
        for marca in marcas:
            cursor.execute(
                "SELECT id FROM boss WHERE nome = ?",
                (boss,)
            )
            resultado = cursor.fetchone()
            
            if resultado is None:
                raise ValueError(f'Boss "{requisito[i]}" não encontrado.')

            idRequisito = resultado[0]


        i += 1
        
        cursor.execute(
            "INSERT INTO progresso(personagem_id, boss_id, concluido) VALUES(?, ?, ?)",(idPersonagem,idRequisito,situacao[i])
        )

conn.commit()

conn.close()

