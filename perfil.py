from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session
from sqlmodel import Session, select

import requests

from database import engine
from models import Conteudo, Material, Usuario


perfil_bp = Blueprint("perfil", __name__)

SUAP_URL = "https://suap.ifrn.edu.br"


def usuario_logado():
    """Devolve o usuário que está na sessão, ou None se ninguém entrou."""
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return None

    with Session(engine) as banco:
        return banco.get(Usuario, usuario_id)


def montar_usuario(dados):
    """Cria ou atualiza o usuário no banco com os dados que vieram do SUAP."""
    matricula = str(dados.get("matricula") or dados.get("id") or "").strip()
    nome = (dados.get("nome_registro") or dados.get("nome")
            or dados.get("nome_usual") or "").strip()
    email = (dados.get("email_preferencial") or dados.get("email") or "").strip()
    tipo_vinculo = dados.get("tipo_vinculo") or ""

    if not isinstance(tipo_vinculo, str):
        tipo_vinculo = ""

    vinculo = dados.get("vinculo")

    if isinstance(vinculo, dict):
        nome = nome or str(vinculo.get("nome", "")).strip()
        tipo_vinculo = tipo_vinculo or str(vinculo.get("tipo_vinculo", "")).strip()

    if not matricula:
        matricula = "sem-matricula"

    if not nome:
        nome = "Usuário do SUAP"

    if not email:
        email = matricula + "@sem-email.local"

    with Session(engine) as banco:
        usuario = banco.exec(
            select(Usuario).where(Usuario.matricula == matricula)
        ).first()

        if usuario is None:
            usuario = Usuario(
                matricula=matricula,
                nome=nome,
                email=email,
                tipo_vinculo=tipo_vinculo,
            )
            banco.add(usuario)
        else:
            usuario.nome = nome or usuario.nome
            usuario.email = email or usuario.email
            usuario.tipo_vinculo = tipo_vinculo or usuario.tipo_vinculo
            banco.add(usuario)

        banco.commit()
        banco.refresh(usuario)

    return usuario


@perfil_bp.route("/entrar/suap", methods=["POST"])
def confirmar_login():
    """Confere no SUAP o token que o navegador pegou e guarda quem entrou.

    É o JavaScript do base.html que chama esta rota, em toda página.
    """
    token = request.form.get("token", "").strip()
    usuario_id_antes = session.get("usuario_id")

    if not token:
        session.pop("usuario_id", None)

        return jsonify({"novo": usuario_id_antes is not None})

    resposta = requests.get(
        SUAP_URL + "/api/rh/eu/",
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
        },
        timeout=20,
    )

    if resposta.status_code != 200:
        return jsonify({"novo": False})

    usuario = montar_usuario(resposta.json())

    session["usuario_id"] = usuario.id

    return jsonify({
        "nome": usuario.nome,
        "novo": usuario.id != usuario_id_antes,
    })

@perfil_bp.route("/perfil")
def exibir_perfil():
    usuario = usuario_logado()

    contribuicoes = []

    if usuario is not None:
        itens = []
        with Session(engine) as banco:
            meus_conteudos = banco.exec(
                select(Conteudo).where(Conteudo.autor_id == usuario.id)
            ).all()

            meus_materiais = banco.exec(
                select(Material).where(Material.autor_id == usuario.id)
            ).all()

            for conteudo in meus_conteudos:
                itens.append((
                    conteudo.criado_em,
                    {
                        "tipo": "Conteúdo",
                        "disciplina": (conteudo.disciplina.nome
                                       if conteudo.disciplina else ""),
                        "titulo": conteudo.titulo,
                        "acao": "Criado em",
                        "data": conteudo.criado_em.strftime("%d/%m/%Y"),
                    },
                ))

            for material in meus_materiais:
                disciplina = ""

                if material.conteudo and material.conteudo.disciplina:
                    disciplina = material.conteudo.disciplina.nome

                itens.append((
                    material.criado_em,
                    {
                        "tipo": "Material",
                        "disciplina": disciplina,
                        "titulo": material.titulo,
                        "acao": "Enviado em",
                        "data": material.criado_em.strftime("%d/%m/%Y"),
                    },
                ))

        # o que foi feito por último aparece primeiro
        itens.sort(key=lambda item: item[0], reverse=True)

        contribuicoes = [item[1] for item in itens]

    return render_template(
        "perfil.html",
        perfil_edicao=session.get("perfil_edicao", {}),
        contribuicoes=contribuicoes,
        usuario=usuario,
    )


@perfil_bp.route("/salvar", methods=["POST"])
def salvar_perfil():
    session["perfil_edicao"] = {
        "nome": request.form.get("nome", "").strip(),
        "email": request.form.get("email", "").strip(),
        "tipo_vinculo": request.form.get("tipo_vinculo", "").strip(),
    }

    return redirect(url_for("perfil.exibir_perfil"))