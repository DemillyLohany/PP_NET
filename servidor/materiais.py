from flask import Blueprint, render_template, redirect, url_for, request, session
from sqlmodel import Session, select

from servidor.database import engine
from servidor.models import Disciplina, Conteudo, Material


materiais_bp = Blueprint("materiais", __name__)


@materiais_bp.route("/materiais/<int:conteudo_id>")
def ver_materiais(conteudo_id):
    with Session(engine) as banco:
        conteudo_atual = banco.get(Conteudo, conteudo_id)

        if conteudo_atual is None:
            return "Não encontramos o conteúdo.", 404

        disciplina_atual = banco.get(
            Disciplina,
            conteudo_atual.disciplina_id
        )

        lista_materiais = banco.exec(
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
        conteudo_id=conteudo_id,
# guarda quem enviou, para aparecer nas contribuições do perfil
        autor_id=session.get("usuario_id")
    )

    with Session(engine) as banco:
        banco.add(novo_material)
        banco.commit()

    return redirect(
        url_for("materiais.ver_materiais", conteudo_id=conteudo_id)
    )


@materiais_bp.route(
    "/editar_material/<int:material_id>",
    methods=["GET", "POST"]
)
def editar_material(material_id):
    with Session(engine) as session:
        material = session.get(Material, material_id)

        if material is None:
            return "Material não encontrado", 404

        if request.method == "POST":
            titulo = request.form.get("titulo", "").strip()
            url = request.form.get("url", "").strip()

            if not titulo or not url:
                return render_template(
                    "editar_materiais.html",
                    material=material,
                    erro="Preencha o titulo e a url."
                ), 400

            material.titulo = titulo
            material.url = url

            session.add(material)
            session.commit()

            return redirect(url_for("materiais.ver_materiais",conteudo_id=material.conteudo_id))

        return render_template(
            "editar_materiais.html",
            material=material
        )


@materiais_bp.route(
    "/excluir_material/<int:material_id>",
    methods=["POST"]
)
def excluir_material(material_id):
    with Session(engine) as banco:
        material = banco.get(Material, material_id)

        if material is None:
            return "Material não encontrado.", 404

        conteudo_id = material.conteudo_id
        banco.delete(material)
        banco.commit()

    return redirect(
        url_for("materiais.ver_materiais", conteudo_id=conteudo_id)
    )