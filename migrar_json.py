import json
import sqlite3
from main import *

with open("isaac_save.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)
        
conn = sqlite3.connect("database/isaac.db")

cursor = conn.cursor()

personagens = listarPersonagens(dados)

for nome, desbloqueio in personagens:
    cursor.execute(
        "INSERT INTO personagem(nome, desbloqueado) VALUES(?, ?)",(nome, desbloqueio)
    )

    conn.commit()

print(personagens)

