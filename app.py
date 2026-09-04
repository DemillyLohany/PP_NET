import os

from flask import Flask, render_template

from conteudos import conteudos_bp
from materiais import materiais_bp
from disciplinas import disciplinas_bp
from perfil import perfil_bp
from notificacoes import notificacoes_bp


app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY", "chave-temporaria-apenas-para-desenvolvimento")


# Registro das partes do sistema
app.register_blueprint(conteudos_bp)
app.register_blueprint(materiais_bp)
app.register_blueprint(disciplinas_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(notificacoes_bp)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def tela_login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    print(app.url_map)

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )