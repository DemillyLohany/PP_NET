import os
import secrets

from flask import Flask, render_template, redirect, url_for, request

from servidor.conteudos import conteudos_bp
from servidor.materiais import materiais_bp
from servidor.disciplinas import disciplinas_bp
from servidor.perfil import perfil_bp, usuario_logado
from servidor.notificacoes import notificacoes_bp


app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY", secrets.token_hex(32))


# registro das partes do sistema
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
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    if usuario_logado() is not None:
        return redirect(url_for("home"))
    return redirect(url_for("home", retorno_suap=1, error=request.args.get("error"), state=request.args.get("state")))


from servidor.regras import registrar_regras, professor
registrar_regras(app)

@app.context_processor
def dados_do_menu():
    pessoa = usuario_logado()
    return {"pessoa": pessoa, "pode_avaliar": professor(pessoa)}

@app.get("/pesquisar")
def pesquisar():
    from flask import request, jsonify
    from sqlmodel import Session, select
    from servidor.database import engine
    from servidor.models import Disciplina, Conteudo, Material
    from unicodedata import normalize, combining

    def normalizar(texto):
        return "".join(letra for letra in normalize("NFD", texto.casefold())
                       if not combining(letra))

    termo = request.args.get("q", "").strip()
    busca = normalizar(termo)
    resultados = []
    if busca:
        with Session(engine) as banco:
            disciplinas = banco.exec(select(Disciplina).order_by(Disciplina.nome)).all()
            for d in disciplinas:
                if busca in normalizar(d.nome + " " + d.descricao):
                    resultados.append(("Disciplina", d.nome, url_for("conteudos.conteudo", disciplina_id=d.id)))
            conteudos = banco.exec(select(Conteudo).join(Disciplina).order_by(Conteudo.titulo)).all()
            for c in conteudos:
                if busca in normalizar(c.titulo + " " + (c.descricao or "")):
                    resultados.append(("Conteúdo", c.titulo, url_for("materiais.ver_materiais", conteudo_id=c.id)))
            materiais = banco.exec(select(Material).join(Conteudo).join(Disciplina).order_by(Material.titulo)).all()
            for m in materiais:
                if busca in normalizar(m.titulo):
                    resultados.append(("Material", m.titulo, url_for("materiais.ver_materiais", conteudo_id=m.conteudo_id)))
    return jsonify(resultados=resultados[:50], total=len(resultados))


if __name__ == "__main__":
    print(app.url_map)

    app.run(
        debug=False,
        host="127.0.0.1",
        port=5000
    )
