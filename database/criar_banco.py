import sqlite3

conn = sqlite3.connect("database/isaac.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE personagem(
    id_personagem INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    desbloqueado INTEGER NOT NULL            
)
""")

cursor.execute("""
CREATE TABLE boss(
    id_boss INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE progresso(
    id_progresso INTEGER PRIMARY KEY AUTOINCREMENT,
    id_personagem INTEGER,
    id_boss INTEGER,
    concluido INTEGER NOT NULL,
    UNIQUE(id_personagem, id_boss),
    FOREIGN KEY(id_personagem) REFERENCES personagem(id_personagem),
    FOREIGN KEY(id_boss) REFERENCES boss(id_boss)
)
""")

cursor.execute("""
CREATE TABLE item(
    id_item INTEGER PRIMARY KEY AUTOINCREMENT,
    id_progresso INTEGER,
    nome TEXT,
    qualidade INTEGER,
    item_bom INTEGER,
    UNIQUE(id_progresso, nome),
    FOREIGN KEY(id_progresso) REFERENCES progresso(id_progresso)
)               
""")

conn.commit()

conn.close()