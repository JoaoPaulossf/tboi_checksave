from conexao import conectar

with conectar() as conn:
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO personagem (nome, desbloqueado) VALUES
        ('Isaac', 1),
        ('Magdalene', 0)
    """)

    cursor.execute("""
            INSERT OR IGNORE INTO boss (nome) VALUES
            ('Satan'),
            ('Blue Baby')
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO progresso (id_personagem,id_boss,concluido) VALUES
        (1,1,1),
        (1,2,0)
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO item (id_progresso,nome,qualidade,item_bom) VALUES
        (1, 'Judas', 0 , 1),
        (2, 'D6', 4, 1)
    """)
    
    conn.commit()
