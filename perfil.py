from flask import Blueprint, render_template, request, redirect, url_for, session


perfil_bp = Blueprint("perfil", __name__)


@perfil_bp.route("/perfil")
def exibir_perfil():
    perfil_edicao = session.get("perfil_edicao", {})

    # Estes dados são apenas uma prévia visual.
    contribuicoes = [
        {
            "tipo": "Conteúdo",
            "disciplina": "Programação de Sistemas para Internet",
            "titulo": "Introdução ao Flask e rotas",
            "acao": "Criado em",
            "data": "13/10/2026",
            "autor": "Camila",
        },
        {
            "tipo": "Material",
            "disciplina": "Banco de Dados",
            "titulo": "Apostila de SQLModel",
            "acao": "Última edição em",
            "data": "12/10/2026",
            "autor": "Demily",
        },
        {
            "tipo": "Material",
            "disciplina": "Design Web",
            "titulo": "Guia de Princípios de design",
            "acao": "Criado em",
            "data": "10/10/2026",
            "autor": "Filipe",
        },
    ]

    return render_template(
        "perfil.html",
        perfil_edicao=perfil_edicao,
        contribuicoes=contribuicoes,
    )


@perfil_bp.route("/salvar", methods=["POST"])
def salvar_perfil():
    session["perfil_edicao"] = {
        "nome": request.form.get("nome", "").strip(),
        "email": request.form.get("email", "").strip(),
        "tipo_vinculo": request.form.get("tipo_vinculo", "").strip(),
    }

    return redirect(url_for("perfil.exibir_perfil"))