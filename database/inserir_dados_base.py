from conexao import conectar

with conectar() as conn:
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO personagem (nome, desbloqueado) VALUES
        ('Isaac', 1),
        ('Magdalene', 0)
        ON CONFLICT (nome) DO NOTHING
    """)

    conn.commit()
