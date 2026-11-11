from flask import Blueprint, render_template, redirect, url_for, request
from sqlmodel import Session, select

from database import engine
from models import Disciplina, Conteudo


conteudos_bp = Blueprint("conteudos", __name__)


@conteudos_bp.route("/conteudos")
def conteudos():
    """Rota geral acessada pelo menu."""
    return redirect(url_for("disciplinas.disciplinas"))


@conteudos_bp.route("/conteudo/<int:disciplina_id>", methods=["GET", "POST"])
def conteudo(disciplina_id):
    with Session(engine) as session:
        disciplina = session.get(Disciplina, disciplina_id)

        if disciplina is None:
            return "Não encontramos a disciplina.", 404

        if request.method == "POST":
            titulo = request.form.get("titulo_conteudo", "").strip()
            descricao = request.form.get("descricao_conteudo", "").strip()

            if not titulo:
                return render_template(
                    "conteudos.html",
                    disciplina=disciplina,
                    conteudos=session.exec(
                        select(Conteudo).where(
                            Conteudo.disciplina_id == disciplina_id
                        )
                    ).all(),
                    erro="Digite o título do conteúdo."
                ), 400

            novo_conteudo = Conteudo(
                titulo=titulo,
                descricao=descricao,
                disciplina_id=disciplina_id
            )

            session.add(novo_conteudo)
            session.commit()

            return redirect(
                url_for(
                    "conteudos.conteudo",
                    disciplina_id=disciplina_id
                )
            )

        busca = select(Conteudo).where(
            Conteudo.disciplina_id == disciplina_id
        )

        lista_conteudos = session.exec(busca).all()

        return render_template(
            "conteudos.html",
            disciplina=disciplina,
            conteudos=lista_conteudos
        )


@conteudos_bp.route(
    "/conteudo/excluir/<int:conteudo_id>",
    methods=["POST"]
)
def excluir_conteudo(conteudo_id):
    with Session(engine) as session:
        conteudo_atual = session.get(Conteudo, conteudo_id)

        if conteudo_atual is None:
            return "Conteúdo não encontrado.", 404

        disciplina_id = conteudo_atual.disciplina_id
        session.delete(conteudo_atual)
        session.commit()

    return redirect(
        url_for(
            "conteudos.conteudo",
            disciplina_id=disciplina_id
        )
    )


@conteudos_bp.route("/criar")
def criar():
    return render_template("criar_conteudos.html")

@conteudos_bp.route("/criar/<int:disciplina_id>", methods=["POST"])
def criar_conteudo(disciplina_id):
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()
    with Session(engine) as session:
        disciplina = session.get(Disciplina, disciplina_id)

        if disciplina is None:
            return "Disciplina não encontrada.", 404

        if request.method == "POST":
            titulo = request.form.get("titulo", "").strip()
            descricao = request.form.get("descricao", "").strip()

            if not titulo or not descricao:
                return render_template(
                    "criar_conteudo.html",
                    disciplina=disciplina,
                    erro="Preencha o titulo e a descrição.",
                    titulo=titulo,
                    descricao=descricao
                ), 400

            novo_conteudo = Conteudo(
                titulo=titulo,
                descricao=descricao,
                disciplina_id=disciplina_id
            )

            session.add(novo_conteudo)
            session.commit()

            return redirect(url_for("conteudos.conteudo",disciplina_id=disciplina_id))
    return render_template("criar_conteudos.html",disciplina=disciplina)

@conteudos_bp.route(
    "/editar/<int:conteudo_id>",
    methods=["GET", "POST"]
)
def editar_conteudo(conteudo_id):
    with Session(engine) as session:
        conteudo = session.get(Conteudo, conteudo_id)

        if conteudo is None:
            return "Conteúdo não encontrado", 404

        if request.method == "POST":
            titulo = request.form.get("titulo", "").strip()
            descricao = request.form.get("descricao", "").strip()

            if not titulo or not descricao:
                return render_template(
                    "editar_conteudos.html",
                    conteudo=conteudo,
                    erro="Preencha o titulo e a descrição."
                ), 400

            conteudo.titulo = titulo
            conteudo.descricao = descricao

            session.add(conteudo)
            session.commit()

            return redirect(url_for("conteudos.conteudo",  disciplina_id=conteudo.disciplina_id))

        return render_template(
            "editar_conteudos.html",
            conteudo=conteudo
        )
