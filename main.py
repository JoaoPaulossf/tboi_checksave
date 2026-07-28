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
        

def listarPersonagens(dados):
    saida = []
    for nome in dados["personagens"]:
        valor = dados["personagens"][nome]["desbloqueado"]
        if valor == True:
            output = 1
        else:
            output = 0 
        saida.append([nome, output])
    return saida

def verificarAllMarks(nome, dados):
    for valor in dados["personagens"][nome]["marcas"].values():
        if valor == False:
            return
    dados["personagens"][nome]["all marks"] = True
    print(f"Você tem todas as marcas com {nome}!")
    
def atualizarMarca(nome, dados, marca):
    if not personagemExiste(nome, dados):
        print("nome invalido!")
        return
    elif not personagemEhDesbloqueado(nome, dados):
        print(f"Você está tentando atualizar uma marca do {nome} que você ainda não desbloqueou!")
        print("Marque ele como desbloqueado antes de tentar atualizar a marca que voce completou!")
        return
    elif dados["personagens"][nome]["all marks"]:
        print(f"Você já tem todas as marcas com {nome}!")
        return
    if not marca in dados["personagens"][nome]["marcas"]:
        print("nome da marca invalido!")
        return
    else:
        dados["personagens"][nome]["marcas"][marca] = True
        for nomeItem, itemAtributos in dados["personagens"][nome]["itens"].items():
            if itemAtributos["requisito"] == marca:
                itemAtributos["desbloqueado"] = True
                print(f"Você desbloqueeou um item bom!\nCompletando a marca do {marca}, foi desbloqueado o item {nomeItem}")
        verificarAllMarks(nome,dados)
        return


def exibirProgresso(nome, dados):
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
    personagemExiste(nome)
main()