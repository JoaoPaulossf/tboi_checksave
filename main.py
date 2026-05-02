import json

def carregarJson():
    with open("isaac_save.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        return dados

def salvarJson(dados):
    with open("isaac_save.json", "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

def personagemExiste(nome,dados):
    if nome in dados["personagens"]:
        return True
    return False

def personagemEhDesbloqueado(nome, dados):
    return dados["personagens"][nome]["desbloqueado"]

def desbloquearPersonagem(nome,dados):
    if personagemExiste(nome,dados):
        dados["personagens"][nome]["desbloqueado"] = True
    else:
        print("Nome invalido!!")

def bloquearPersonagem(nome,dados):
    if personagemExiste(nome,dados):
        dados["personagens"][nome]["desbloqueado"] = False
    else:
        print("Nome invalido!!")

def listarItens(nome,dados):
    if personagemExiste(nome,dados):
        for NomeItem, valor in dados["personagens"][nome]["itens"].items():
            desbloqueado = valor["desbloqueado"]
            requisito = valor["requisito"]
            print(f"{NomeItem} : {desbloqueado} {requisito}")

def listarPersonagens(dados):
    for nome in dados["personagens"]:
        valor = dados["personagens"][nome]["desbloqueado"]
        print(f"{nome} : {valor}")

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

    

def main():
    dados = carregarJson()
    
    #listarPersonagens(dados)

    #nome = input("digita um nome de isaac ai mano:").lower()
    #desbloquearPersonagem(nome,dados)
    marca = input(f"digita uma marca que voce fez:").lower()

    atualizarMarca("isaac",dados,marca)

    salvarJson(dados)

main()