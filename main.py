import json
import random

from database.conexao import conectar

#tirar as duas funções abaixo!!!
def carregarJson():
    with open("isaac_save.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        return dados

def salvarJson(dados):
    with open("isaac_save.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

#verifica se o personagem existe, caso exista, retorna o id
def personagemExiste(personagem):
    
    with conectar() as conn:        
        cursor = conn.cursor()

        cursor.execute(
        "SELECT * FROM personagem WHERE nome = ?",(personagem,)
        )
    
        resultado = cursor.fetchone()

        if resultado is None:
            return False

        return resultado[0]


def personagemEhDesbloqueado(id):
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

def desbloquearPersonagem(id):
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE personagem SET desbloqueado = 1 WHERE id = ?",
            (id,)
        )    

def bloquearPersonagem(id):
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE personagem SET desbloqueado = 0 WHERE id = ?",
            (id,)
        )

    
def listarItens(id):
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT item_id, boss_id FROM unlock WHERE personagem_id = ?",
            (id,)
        )
        

def listarPersonagens():
    saida = []
    with conectar() as conn:
            cursor = conn.cursor()
    
            cursor.execute(
                "SELECT nome FROM personagem",
                (id,)
            )

            saida = cursor.fetchone()

    return saida

def verificarAllMarks(id):
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT concluido FROM progresso WHERE personagem_id = ?",
            (id,)
        )

        progressos = cursor.fetchone()

        for progresso in progressos:
            if progresso:
                return

        print(f"Você tem todas as marcas!")
    
def atualizarMarca(idNome, idMarca):
    
    with conectar() as conn:
            cursor = conn.cursor()
    
            cursor.execute(
                "UPDATE progresso SET concluido = 1 WHERE personagem_id = ? and boss_id = ?",
                (idNome,idMarca,)
            )
    


def exibirProgresso(idNome):
    with conectar() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT nome FROM personagem"
        )
    marcas = []
    estados = []
    for marca, estado in dados["personagens"][nome]["marcas"].items():
        if estado == True:
            saida = "1"
        else:
            saida = "0"
        marcas.append(marca)
        estados.append(saida)

    return marcas,estados

def gerarRun(dados):
    personagensDesbloqueados = [
        chave for chave, valor in dados["personagens"].items()
        if valor["desbloqueado"] 
    ]
    personagemSorteado = random.choice(personagensDesbloqueados)
    objetivosPrimarios = ["The lamb", "Blue baby(???)", "Mega Satan", "Mother", "The beast" , "Greed"]
    objetivosSecundarios = ["Delirium", "Boss Rush", "Hush"]
    primarioSorteado = random.choice(objetivosPrimarios)
    secundarioSorteado = random.choice(objetivosSecundarios)

    print(f"\nPersonagem:{personagemSorteado.capitalize()}\nObjetivo: {primarioSorteado}\nTentar chegar no {secundarioSorteado}\n")

def main():
    nome = input().lower()
    if personagemExiste(nome):
        print("Existe")
        return
    print("Não existe")
    
main()