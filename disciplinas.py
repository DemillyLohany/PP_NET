from flask import Blueprint, render_template, request, redirect, url_for
from sqlmodel import Session, select

from database import engine
from models import Disciplina


disciplinas_bp = Blueprint("disciplinas", __name__, url_prefix="/disciplinas")

@disciplinas_bp.route("/")
def disciplinas():
    termo = request.args.get("q", "").strip().lower()

    with Session(engine) as session:
        consulta = select(Disciplina)
        todas_disciplinas = session.exec(consulta).all()

    if termo:
        lista_disciplinas = [
            disciplina
            for disciplina in todas_disciplinas
            if termo in disciplina.nome.lower()
            or termo in disciplina.descricao.lower()
        ]
    else:
        lista_disciplinas = todas_disciplinas

    return render_template(
        "disciplinas.html",
        lista_disciplinas=lista_disciplinas,
        termo=termo
    )

@disciplinas_bp.route("/criar")
def criar():
    return render_template("criar_disciplina.html")

@disciplinas_bp.route("/criar", methods=["POST"])
def criar_disciplina():
    nome = request.form.get("nome", "").strip()
    descricao = request.form.get("descricao", "").strip()

    if not nome or not descricao:
        return render_template(
            "criar_disciplina.html",
            erro="Preencha o nome e a descrição.",
            nome=nome,
            descricao=descricao
        ), 400

    nova_disciplina = Disciplina(
        nome=nome,
        descricao=descricao
    )

    with Session(engine) as session:
        session.add(nova_disciplina)
        session.commit()

    return redirect(url_for("disciplinas.disciplinas"))


@disciplinas_bp.route(
    "/editar/<int:disciplina_id>",
    methods=["GET", "POST"]
)
def editar_disciplina(disciplina_id):
    with Session(engine) as session:
        disciplina = session.get(Disciplina, disciplina_id)

        if disciplina is None:
            return "Disciplina não encontrada", 404

        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            descricao = request.form.get("descricao", "").strip()

            if not nome or not descricao:
                return render_template(
                    "editar_disciplina.html",
                    disciplina=disciplina,
                    erro="Preencha o nome e a descrição."
                ), 400

            disciplina.nome = nome
            disciplina.descricao = descricao

            session.add(disciplina)
            session.commit()

            return redirect(url_for("disciplinas.disciplinas"))

        return render_template(
            "editar_disciplina.html",
            disciplina=disciplina
        )

@disciplinas_bp.route(
    "/excluir/<int:disciplina_id>",
    methods=["POST"]
)
def excluir_disciplina(disciplina_id):
    with Session(engine) as session:
        disciplina = session.get(Disciplina, disciplina_id)

        if disciplina is None:
            return "Disciplina não encontrada", 404

        session.delete(disciplina)
        session.commit()

    return redirect(url_for("disciplinas.disciplinas"))