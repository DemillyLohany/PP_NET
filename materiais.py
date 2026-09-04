from flask import Blueprint, render_template, redirect, url_for, request
from sqlmodel import Session, select

from database import engine
from models import Disciplina, Conteudo, Material


materiais_bp = Blueprint("materiais", __name__)


@materiais_bp.route("/materiais/<int:conteudo_id>")
def ver_materiais(conteudo_id):
    with Session(engine) as session:
        conteudo_atual = session.get(Conteudo, conteudo_id)

        if conteudo_atual is None:
            return "Não encontramos o conteúdo.", 404

        disciplina_atual = session.get(
            Disciplina,
            conteudo_atual.disciplina_id
        )

        lista_materiais = session.exec(
            select(Material).where(
                Material.conteudo_id == conteudo_id
            )
        ).all()

        return render_template(
            "materiais.html",
            disciplina=disciplina_atual,
            conteudo=conteudo_atual,
            materiais=lista_materiais
        )


@materiais_bp.route(
    "/adicionar_material/<int:conteudo_id>",
    methods=["POST"]
)
def adicionar_material(conteudo_id):
    titulo = request.form.get("titulo", "").strip()
    url = request.form.get("url", "").strip()

    if not titulo or not url:
        return redirect(
            url_for("materiais.ver_materiais", conteudo_id=conteudo_id)
        )

    novo_material = Material(
        titulo=titulo,
        url=url,
        conteudo_id=conteudo_id
    )

    with Session(engine) as session:
        session.add(novo_material)
        session.commit()

    return redirect(
        url_for("materiais.ver_materiais", conteudo_id=conteudo_id)
    )


@materiais_bp.route(
    "/excluir_material/<int:material_id>",
    methods=["POST"]
)
def excluir_material(material_id):
    with Session(engine) as session:
        material = session.get(Material, material_id)

        if material is None:
            return "Material não encontrado.", 404

        conteudo_id = material.conteudo_id
        session.delete(material)
        session.commit()

    return redirect(
        url_for("materiais.ver_materiais", conteudo_id=conteudo_id)
    )
