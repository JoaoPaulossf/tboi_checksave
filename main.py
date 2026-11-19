import random

from database.conexao import conectar

def personagemExiste(personagem): #verifica se o personagem existe, caso exista, retorna o id
    
    with conectar() as conn:        
        cursor = conn.cursor()

        cursor.execute(
        "SELECT id_personagem FROM personagem WHERE nome = ?",
        (personagem,)
        )
    
        resultado = cursor.fetchone()

        if resultado is None:
            return False

        return resultado[0]


def personagemEhDesbloqueado(idPersonagem): #verifica se o personagem é desbloqueado atraves do id do personagem
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT desbloqueado FROM personagem WHERE id_personagem = ?",
            (idPersonagem,)
        )

        situacao = cursor.fetchone()[0]

        if situacao == 0:
            return False
        
        return True

def desbloquearPersonagem(idPersonagem): # desbloqueia um personagem
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE personagem SET desbloqueado = 1 WHERE id_personagem = ?",
            (idPersonagem,)
        )

        conn.commit()    

def bloquearPersonagem(idPersonagem): # bloqueia um personagem
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE personagem SET desbloqueado = 0 WHERE id_personagem = ?",
            (idPersonagem,)
        )

        conn.commit()

# Função testada !
def listarItens(idPersonagem): # lista todos os itens de um personagem
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id_progresso,id_boss, concluido FROM progresso WHERE id_personagem = ?",
            (idPersonagem,)
        )

        id_progresso = cursor.fetchall()

        for tupla in id_progresso:
            
            id_progresso = tupla[0]
            
            id_boss = tupla[1]

            desbloqueado = "Sim" if tupla[2] else "Não"
            cursor.execute(
                "SELECT nome, qualidade, item_bom FROM item WHERE id_progresso = ?",
                (id_progresso,)
            )

            dados_item = cursor.fetchone()
            itemBom = "Sim" if dados_item[2] else "Não"

            cursor.execute(
                "SELECT nome FROM boss WHERE id_boss = ?",
                (id_boss,)
            )

            nome_boss = cursor.fetchone()

            print(f"Item: {dados_item[0]} | requisito: {nome_boss[0]} | Desbloqueado?: {desbloqueado} | qualidade: {dados_item[1]} | Item bom : {itemBom}")

# função testada ! 
def listarPersonagens():# apenas lista o nome de todos os personagens
    saida = []
    with conectar() as conn:
            cursor = conn.cursor()
    
            cursor.execute(
                "SELECT nome FROM personagem"
            )

            for personagem in cursor.fetchall():
                saida.append(personagem[0])

    return saida

# função testada !
def verificarAllMarks(idPersonagem): # verifica se o personagem tem todos os boss concluidos
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT concluido FROM progresso WHERE id_personagem = ?",
            (idPersonagem,)
        )

        progressos = cursor.fetchall()

        for progresso in progressos:
            if not progresso[0]:
                return False

        return True

#ainda tem que ser testada!   
def atualizarMarca(idPersonagem, idBoss): # desbloqueia uma marca de um determinado boss em um determinado personagem
    
    with conectar() as conn:
            cursor = conn.cursor()
    
            cursor.execute(
                "UPDATE progresso SET concluido = 1 WHERE id_personagem = ? and id_boss = ?",
                (idPersonagem,idBoss,)
            )

            conn.commit()
    

# função validada !!
def exibirProgresso(idPersonagem): # Pega os dados do progresso de determinado personagem e exibe eles no terminal
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id_boss, concluido FROM progresso WHERE id_personagem = ?",
            (idPersonagem,)
        )

        saida = cursor.fetchall()

        for status in saida:
            idBoss = status[0]
            
            cursor.execute(
                "SELECT nome FROM boss WHERE id_boss = ?",
                (idBoss,)
            )

            nome_boss = cursor.fetchone()[0]

            situacao = "Concluido" if status[1] else "Não Concluído"

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
    gerarRun()
main()