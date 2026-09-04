from copy import deepcopy

from flask import (Blueprint, render_template, request, redirect, url_for, session)

from dados_estaticos import NOTIFICACOES


notificacoes_bp = Blueprint("notificacoes", __name__)


@notificacoes_bp.route(
    "/notificacoes",
    methods=["GET", "POST"]
)
def tela_notificacoes():
    if request.method == "POST":
        acao = request.form.get("acao")

        if acao == "aprovar":
            session["status_notificacao"] = "Aprovada"

        elif acao == "reprovar":
            session["status_notificacao"] = "Reprovada"

        elif acao == "destacar":
            session["notificacao_destacada"] = True

        return redirect(
            url_for("notificacoes.tela_notificacoes")
        )

    dados = deepcopy(NOTIFICACOES)

    dados["status_avaliacao"] = session.get(
        "status_notificacao",
        "Aguardando avaliação"
    )

    dados["destacada"] = session.get(
        "notificacao_destacada",
        False
    )

    return render_template(
        "notificacoes.html",
        dados=dados
    )