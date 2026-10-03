from flask import Blueprint, render_template, request, redirect, url_for, session

perfil_bp = Blueprint("perfil", __name__)

@perfil_bp.route("/perfil")
def exibir_perfil():
    perfil_edicao = session.get("perfil_edicao", {})
    return render_template(
        "perfil.html",
        perfil_edicao=perfil_edicao
    )

@perfil_bp.route("/salvar", methods=["POST"])
def salvar_perfil():
    session["perfil_edicao"] = {
        "nome": request.form.get("nome", "").strip(),
        "email": request.form.get("email", "").strip(),
        "tipo_vinculo": request.form.get("tipo_vinculo", "").strip()
    }

    return redirect(url_for("perfil.exibir_perfil"))