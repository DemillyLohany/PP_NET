from flask import abort, flash, Blueprint, jsonify, render_template, request, redirect, url_for, session
from sqlmodel import Session, col, select

import os
import requests
import secrets
from urllib.parse import urlencode, urljoin, urlsplit

from servidor.database import engine
from servidor.models import Conteudo, Material, Usuario, Solicitacao


perfil_bp = Blueprint("perfil", __name__)

SUAP_URL = "https://suap.ifrn.edu.br"


MATRICULA_TESTE = "net-professor-teste"


def teste_local_ativo():
    chave = os.getenv("NET_CHAVE_TESTE", "")
    return (len(chave) >= 16 and request.remote_addr in ("127.0.0.1", "::1")
            and request.host in ("localhost:5000", "127.0.0.1:5000"))


def foto_do_suap(dados):
    vinculo = dados.get("vinculo")
    for origem in (dados, vinculo if isinstance(vinculo, dict) else {}):
        for campo in ("foto_url", "url_foto_75x100", "url_foto_150x200", "url_foto", "foto"):
            valor = origem.get(campo)
            if not isinstance(valor, str) or not valor.strip():
                continue
            try:
                endereco = urljoin(SUAP_URL + "/", valor.strip())
                partes = urlsplit(endereco)
                if partes.scheme == "https" and partes.netloc == "suap.ifrn.edu.br":
                    return endereco
            except ValueError:
                continue
    return None


@perfil_bp.route("/teste-professor", methods=["GET", "POST"])
def entrar_teste():
    if not teste_local_ativo():
        abort(404)
    if request.method == "POST":
        chave = request.form.get("chave", "").strip().encode()
        if not secrets.compare_digest(chave, os.environ["NET_CHAVE_TESTE"].encode()):
            return render_template("teste_professor.html", erro="Chave de teste incorreta."), 403
        with Session(engine) as banco:
            pessoa = banco.exec(select(Usuario).where(Usuario.matricula == MATRICULA_TESTE)).first()
            if pessoa is None:
                pessoa = Usuario(matricula=MATRICULA_TESTE, nome="Professor de Teste",
                                 email="teste@exemplo.com", tipo_vinculo="Professor de teste")
                banco.add(pessoa)
                banco.commit()
                banco.refresh(pessoa)
            usuario_id = pessoa.id
        session.clear()
        session["usuario_id"] = usuario_id
        session["professor_teste"] = True
        return redirect(url_for("perfil.exibir_perfil"), code=303)
    return render_template("teste_professor.html")


def usuario_logado():
    """Devolve o usuário que está na sessão, ou None se ninguém entrou."""
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return None

    with Session(engine) as banco:
        pessoa = banco.get(Usuario, usuario_id)
        if pessoa is not None and pessoa.matricula == MATRICULA_TESTE:
            if not session.get("professor_teste") or not teste_local_ativo():
                return None
        return pessoa


def identificar_conta(dados, vinculo):
# procura a matrícula nos campos que o suap envia
    for valor in (dados.get("matricula"), vinculo.get("matricula"), dados.get("identificacao")):
        if type(valor) in (str, int) and str(valor).strip():
            return str(valor).strip()
    return ""


def ler_vinculo(dados, vinculo):
# procura o vínculo que o suap informou
    for valor in (dados.get("tipo_vinculo"), vinculo.get("tipo_vinculo"),
                  dados.get("tipo_usuario"), vinculo.get("tipo_usuario"),
                  dados.get("vinculo")):
        if isinstance(valor, str) and valor.strip():
            return valor.strip()
    return ""


def montar_usuario(dados):
    """Cria ou atualiza o usuário no banco com os dados que vieram do SUAP."""
    vinculo = dados.get("vinculo")
    vinculo = vinculo if isinstance(vinculo, dict) else {}
    matricula = identificar_conta(dados, vinculo)
    nome = (dados.get("nome_registro") or dados.get("nome")
            or dados.get("nome_usual") or "").strip()
    emails = []
    campos_email = ("email_escolar", "email_preferencial", "email", "email_institucional",
                    "email_academico", "email_pessoal", "email_secundario")
    for origem in (dados, vinculo):
        for campo in campos_email:
            valor = origem.get(campo)
            if isinstance(valor, str) and "@" in valor.strip():
                emails.append(valor.strip())
    email = next((valor for valor in emails if valor.rsplit("@", 1)[1].lower() == "escolar.ifrn.edu.br"),
                 emails[0] if emails else "")
    tipo_vinculo = ler_vinculo(dados, vinculo)
    nome = nome or str(vinculo.get("nome") or "").strip()

    if not matricula or matricula == MATRICULA_TESTE:
        raise ValueError("Matrícula não informada")

    if not nome:
        nome = ""

    if not email:
        email = ""

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
            usuario.email = email
            usuario.tipo_vinculo = tipo_vinculo
            banco.add(usuario)

        usuario.foto_url = foto_do_suap(dados) or usuario.foto_url
        banco.commit()
        banco.refresh(usuario)

    return usuario



@perfil_bp.get("/entrar")
def entrar():
    if usuario_logado() is not None:
        return redirect(url_for("home"))

    if request.host == "127.0.0.1:5000":
        return redirect("http://localhost:5000/entrar")

    estado = secrets.token_urlsafe(32)
    session["estado_login"] = estado
    parametros = urlencode({
        "response_type": "token",
        "grant_type": "implicit",
        "client_id": "8eybcqTXpI6BpyEKwvJ5uhjwbiRA3HXjUyUjnpn0",
        "redirect_uri": "http://localhost:5000/dashboard",
        "scope": "identificacao email documentos_pessoais",
        "state": estado,
    })
    return redirect(SUAP_URL + "/o/authorize/?" + parametros)

@perfil_bp.post("/entrar/suap")
def confirmar_login():
    if usuario_logado() is not None:
        return jsonify(ok=True)

    if request.form.get("falha") == "1":
        session.pop("estado_login", None)
        flash("O SUAP não concluiu o login. Tente entrar novamente.", "login")
        return jsonify(ok=False), 400
    estado = session.get("estado_login")
    if not estado or not secrets.compare_digest(estado, request.form.get("estado", "")):
        flash("Não foi possível confirmar esta tentativa. Clique em Entrar com SUAP para tentar novamente.", "login")
        return jsonify(ok=False), 400
    session.pop("estado_login", None)
    token = request.form.get("token", "")
    if not token:
        flash("O SUAP não retornou um token.", "login")
        return jsonify(ok=False), 400
    try:
        resposta = requests.get(SUAP_URL + "/api/rh/eu/",
                                headers={"Authorization": "Bearer " + token},
                                params={"scope": "identificacao email"},
                                timeout=10, allow_redirects=False)
        if resposta.status_code != 200:
            flash("O SUAP recusou a confirmação da identidade. Entre novamente.", "login")
            return jsonify(ok=False), 401
        try:
            dados = resposta.json()
        except ValueError:
            flash("O SUAP respondeu em um formato inesperado. Tente novamente.", "login")
            return jsonify(ok=False), 502
        if not isinstance(dados, dict):
            raise ValueError()
        pessoa = montar_usuario(dados)
    except requests.RequestException:
        flash("Não foi possível conectar ao SUAP. Confira a internet e tente novamente.", "login")
        return jsonify(ok=False), 502
    except ValueError:
        flash("O SUAP não retornou matrícula nem identificação utilizável para sua conta.", "login")
        return jsonify(ok=False), 502
    session.clear()
    session["usuario_id"] = pessoa.id
    return jsonify(ok=True)

@perfil_bp.post("/sair")
def sair():
    session.clear()
    resposta = redirect(url_for("home"))
    for nome in ("suapToken", "suapTokenExpirationTime", "suapScope"):
        resposta.delete_cookie(nome)
    return resposta

@perfil_bp.get("/perfil")
def exibir_perfil():
    pessoa = usuario_logado()
    if pessoa is None:
        return redirect(url_for("home"))
    with Session(engine) as banco:
        pedidos = banco.exec(select(Solicitacao).where(
            Solicitacao.usuario_id == pessoa.id
        ).order_by(col(Solicitacao.id).desc()).limit(4)).all()
    return render_template("perfil.html", pessoa=pessoa, pedidos=pedidos)
