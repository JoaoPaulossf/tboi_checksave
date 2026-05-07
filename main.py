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
            if desbloqueado == True:
                status = "✅ Desbloqueado"
            else:
                status = "❌ Bloqueado"
            print(f"Item: {NomeItem} Status: {status} Marca necessária: {requisito}")

def listarPersonagens(dados):
    for nome in dados["personagens"]:
        valor = dados["personagens"][nome]["desbloqueado"]
        if valor == True:
            output = "✅ Desbloqueado"
        else:
            output = "❌ Bloqueado" 
        print(f"{nome} : {output}")

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
    if not personagemExiste(nome, dados):
        print("Nome invalido!")
        return
    for marca, estado in dados["personagens"][nome]["marcas"].items():
        if estado == True:
            saida = "✅ Concluido!"
        else:
            saida = "❌ Não concluido!"
        print(f"{marca} : {saida}")
    

def main():
    dados = carregarJson()
    
    opcao = -1

    while opcao != 0:
        print("1 - Listar personagens\n 2 - Listar itens de um personagem\n 3 - Desbloquear personagem\n 4 - Bloquear personagem\n 5 - Atualizar marca de um personagem")
        opcao = int(input("Coloque o numero correspondente a sua escolha:"))
        match opcao:
            case 1:
                listarPersonagens(dados)
            case 2:
                nome = input("Digite o nome do personagem que quer ver os itens:")
                listarItens(nome,dados)
            case 3:
                nome = input("Digite o nome do personagem que quer desbloquear:")
                desbloquearPersonagem(nome,dados)
            case 4:
                nome = input("Digite o nome do personagem que quer bloquear:")
                bloquearPersonagem(nome,dados)
            case 5:
                nome = input("Digite o nome do persoagem que quer atualizar uma marca:")
                exibirProgresso(nome, dados)
                marca = input("Digite o nome da marca que quer atualizar:")
                atualizarMarca(nome,dados,marca)
            case 0:
                print("fechando o programa...")
            case _:
                print("opcao invalida!tente novamente")
        salvarJson(dados)
        dados = carregarJson()    
    

main()