import random

from database.conexao import conectar

def personagemExiste(personagem): #verifica se o personagem existe, caso exista, retorna o id
    
    with conectar() as conn:        
        cursor = conn.cursor()

        cursor.execute(
        "SELECT * FROM personagem WHERE nome = ?",(personagem,)
        )
    
        resultado = cursor.fetchone()

        if resultado is None:
            return False

        return resultado[0]


def personagemEhDesbloqueado(id): #verifica se o personagem é desbloqueado atraves do id do personagem
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT desbloqueado FROM personagem WHERE id = ?",
            (id,)
        )

        situacao = cursor.fetchone()[0]

        if situacao == 0:
            return False
        
        return True

def desbloquearPersonagem(id): # desbloqueia um personagem
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE personagem SET desbloqueado = 1 WHERE id = ?",
            (id,)
        )

        conn.commit()    

def bloquearPersonagem(id): # bloqueia um personagem
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE personagem SET desbloqueado = 0 WHERE id = ?",
            (id,)
        )

        conn.commit()

# Função testada !
def listarItens(idNome): # lista todos os itens de um personagem
    output = []
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT item_id, boss_id FROM unlock WHERE personagem_id = ?",
            (idNome,)
        )

        id = cursor.fetchall()

        for tuplas in id:
            cursor.execute(
                "SELECT nome FROM item WHERE id = ?",
                (tuplas[0],)
            )

            nome_item = cursor.fetchone()[0]

            cursor.execute(
                "SELECT nome FROM boss WHERE id = ?",
                (tuplas[1],)
            )

            nome_boss = cursor.fetchone()[0]

            tupla = (nome_item,nome_boss)

            output.append(tupla)

        return output # retorna uma lista de tuplas no formato [(nome_item, nome_boss)]
        
# função testada ! 
def listarPersonagens():# apenas lista o nome de todos os personagens
    saida = []
    with conectar() as conn:
            cursor = conn.cursor()
    
            cursor.execute(
                "SELECT nome FROM personagem"
            )

            saida = cursor.fetchall()

    return saida

# função testada !
def verificarAllMarks(idNome): # verifica se o personagem tem todos os boss concluidos
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT concluido FROM progresso WHERE personagem_id = ?",
            (idNome,)
        )

        progressos = cursor.fetchone()

        for progresso in progressos:
            if not progresso:
                return False

        print(f"Você tem todas as marcas!")

#ainda tem que ser testada!   
def atualizarMarca(idNome, idMarca): # desbloqueia uma marca de um determinado boss em um determinado personagem
    
    with conectar() as conn:
            cursor = conn.cursor()
    
            cursor.execute(
                "UPDATE progresso SET concluido = 1 WHERE personagem_id = ? and boss_id = ?",
                (idNome,idMarca,)
            )

            conn.commit()
    

# função validada !!
def exibirProgresso(idNome): # Pega os dados do progresso de determinado personagem e exibe eles no terminal
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT boss_id,concluido FROM progresso WHERE personagem_id = ?",
            (idNome,)
        )

        saida = cursor.fetchall()

        for status in saida:
            idBoss = status[0]
            
            cursor.execute(
                "SELECT nome FROM boss WHERE id = ?",
                (idBoss,)
            )

            nome_boss = cursor.fetchone()[0]

            if(status[1]):
                situacao = "desbloqueado"
            else:
                situacao = "bloqueado"

            print(f"Boss:{nome_boss} | situação:{situacao}")
    
    
# função validada!!
def gerarRun():# gera uma run aleatória de acordo com os personagens desbloqueados

    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT nome FROM personagem WHERE desbloqueado = 1"
        )

        personagens_desbloqueados = cursor.fetchall()

        personagem_sorteado = random.choice(personagens_desbloqueados)[0]

        objetivosPrimarios = ["The lamb", "Blue baby(???)", "Mega Satan", "Mother", "The beast" , "Greed"]
        objetivosSecundarios = ["Delirium", "Boss Rush", "Hush"]
        primarioSorteado = random.choice(objetivosPrimarios)
        secundarioSorteado = random.choice(objetivosSecundarios)

        print(f"\nPersonagem:{personagem_sorteado.capitalize()}\nObjetivo: {primarioSorteado}\nTentar chegar no {secundarioSorteado}\n")

def main():
    lista = listarItens(1)
    for tupla in lista:
        print(f"{tupla[0]} : {tupla[1]}")
main()