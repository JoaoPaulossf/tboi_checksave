import sqlite3

conn = sqlite3.connect("database/isaac.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE personagem(
    id INTEGER PRIMARY KEY,
    nome TEXT,
    desbloqueado INTEGER               
)
""")

cursor.execute("""
CREATE TABLE boss(
    id INTEGER PRIMARY KEY,
    nome TEXT
)
""")

cursor.execute("""
CREATE TABLE item(
    id INTEGER PRIMARY KEY,
    nome TEXT,
    qualidade INTEGER
)               
""")

cursor.execute("""
CREATE TABLE unlock(
    id INTEGER PRIMARY KEY, 
    personagem_id INTEGER,
    item_id INTEGER,
    boss_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE progresso(
    id INTEGER PRIMARY KEY,
    personagem_id INTEGER,
    boss_id INTEGER,
    concluido INTEGER
)
""")

conn.commit()

conn.close()