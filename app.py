from flask import Flask, render_template, url_for
import json
def carregarJson():
    with open("isaac_save.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        return dados
    

app = Flask(__name__)

@app.route("/")
def home():
    titulo = "Projeto isaac"
    dados = carregarJson()
    return render_template("index.html", titulo=titulo,dados=dados)


if __name__ == "__main__":
    app.run(debug=True)