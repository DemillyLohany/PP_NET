import json
import os
from datetime import datetime, timezone
from urllib.parse import urlsplit

from flask import flash, abort, g, redirect, render_template, request, url_for
from sqlmodel import Session, col, select

from servidor.database import engine
from servidor.models import Conteudo, Disciplina, Material, Solicitacao
from servidor.perfil import usuario_logado

# as telas do acervo continuam iguais. A regra é aplicada antes de gravar.
rotas = {
    "disciplinas.criar_disciplina": (Disciplina, "Cadastro", None, {"nome":"nome_disciplinas", "descricao":"descricao_disciplinas"}),
    "disciplinas.editar_disciplina": (Disciplina, "Edição", "disciplina_id", {"nome":"nome", "descricao":"descricao"}),
    "disciplinas.excluir_disciplina": (Disciplina, "Exclusão", "disciplina_id", {}),
    "conteudos.conteudo": (Conteudo, "Cadastro", "disciplina_id", {"titulo":"titulo_conteudo", "descricao":"descricao_conteudo"}),
    "conteudos.criar_conteudo": (Conteudo, "Cadastro", "disciplina_id", {"titulo":"titulo", "descricao":"descricao"}),
    "conteudos.editar_conteudo": (Conteudo, "Edição", "conteudo_id", {"titulo":"titulo", "descricao":"descricao"}),
    "conteudos.excluir_conteudo": (Conteudo, "Exclusão", "conteudo_id", {}),
    "materiais.adicionar_material": (Material, "Cadastro", "conteudo_id", {"titulo":"titulo", "url":"url"}),
    "materiais.editar_material": (Material, "Edição", "material_id", {"titulo":"titulo", "url":"url"}),
    "materiais.excluir_material": (Material, "Exclusão", "material_id", {}),
}
modelos = {c.__name__: c for c in (Disciplina, Conteudo, Material)}

def professor(pessoa):

# só professores da lista podem aprovar
    matriculas = os.getenv("NET_PROFESSORES", "").split(",")
    return pessoa and pessoa.matricula in {m.strip() for m in matriculas if m.strip()}

def aplicar(banco, pedido):
    modelo = modelos[pedido.entidade]
    dados = json.loads(pedido.dados)
    if pedido.acao == "Cadastro":
        for campo, pai in (("disciplina_id", Disciplina), ("conteudo_id", Conteudo)):
            if campo in dados and banco.get(pai, dados[campo]) is None:
                abort(409, "O registro relacionado não existe mais.")
        if modelo is not Disciplina:
            dados["autor_id"] = pedido.usuario_id
        banco.add(modelo(**dados))
    else:
        item = banco.get(modelo, pedido.alvo_id)
        if item is None:
            abort(409, "O item não existe mais.")
        if pedido.acao == "Exclusão":
            if getattr(item, "conteudos", None) or getattr(item, "materiais", None):
                abort(409, "Retire os itens vinculados antes de excluir.")
            banco.delete(item)
        else:
            for campo, valor in dados.items():
                setattr(item, campo, valor)

def registrar_regras(app):
    def voltar_com_aviso(mensagem):
        flash(mensagem, "validacao")
        origem = urlsplit(request.host_url)
        anterior = urlsplit(request.referrer or "")
        if (anterior.scheme, anterior.netloc) == (origem.scheme, origem.netloc):
            return redirect(anterior.geturl(), code=303)
        argumentos = request.view_args or {}
        if request.endpoint == "materiais.adicionar_material":
            destino = url_for("materiais.ver_materiais", conteudo_id=argumentos["conteudo_id"])
        elif request.endpoint == "materiais.editar_material":
            destino = url_for("materiais.editar_material", material_id=argumentos["material_id"])
        elif request.endpoint in ("conteudos.conteudo", "conteudos.criar_conteudo"):
            destino = url_for("conteudos.conteudo", disciplina_id=argumentos["disciplina_id"])
        elif request.endpoint == "conteudos.editar_conteudo":
            destino = url_for("conteudos.editar_conteudo", conteudo_id=argumentos["conteudo_id"])
        elif request.endpoint == "disciplinas.editar_disciplina":
            destino = url_for("disciplinas.editar_disciplina", disciplina_id=argumentos["disciplina_id"])
        else:
            destino = url_for("disciplinas.disciplinas")
        return redirect(destino, code=303)

    @app.before_request
    def checar_alteracao():
        if request.method == "POST":
            origem = request.headers.get("Origin")
            if origem != request.host_url.rstrip("/"):
                abort(403)
        regra = rotas.get(request.endpoint)
        if regra is None or request.method != "POST":
            return
        pessoa = usuario_logado()
        if pessoa is None:
            flash("Você não tem permissão para alterar o acervo sem entrar com o SUAP.", "permissao")
            anterior = urlsplit(request.referrer or "")
            origem = urlsplit(request.host_url)
            if (anterior.scheme, anterior.netloc) == (origem.scheme, origem.netloc) and anterior.path.startswith("/") and not anterior.path.startswith("//") and "\\" not in anterior.path:
                return redirect(anterior.path + ("?" + anterior.query if anterior.query else ""), code=303)
            return redirect(url_for("disciplinas.disciplinas"), code=303)
        modelo, acao, chave, campos = regra
        alvo = (request.view_args or {}).get(chave)
        dados = {campo: request.form.get(entrada, "").strip() for campo, entrada in campos.items()}
        if any(not valor for campo, valor in dados.items() if campo != "descricao"):
            return voltar_com_aviso("Preencha os campos obrigatórios antes de salvar.")
        if "url" in dados:
            url = dados["url"]
            try:
                link = urlsplit(url)
                valido = link.scheme in ("http", "https") and bool(link.hostname) and not any(c.isspace() for c in url)
            except ValueError:
                valido = False
            if not valido:
                return voltar_com_aviso("Endereço do material inválido. Cole um link completo, começando com https:// ou http://, sem espaços.")
        if acao == "Cadastro" and chave:
            dados[chave] = alvo
        with Session(engine) as banco:
            if chave:
                pai = (Disciplina if modelo is Conteudo else Conteudo) if acao == "Cadastro" else modelo
                if banco.get(pai, alvo) is None:
                    abort(404)
            pedido = Solicitacao(usuario_id=pessoa.id, entidade=modelo.__name__, acao=acao,
                                  alvo_id=alvo, dados=json.dumps(dados, ensure_ascii=False))
            if professor(pessoa):
                aplicar(banco, pedido)
                pedido.estado = "Aprovada"
                pedido.avaliador_id = pessoa.id
                pedido.avaliado_em = datetime.now(timezone.utc)
            banco.add(pedido)
            banco.commit()
        if professor(pessoa):
            return render_template("pedidos.html", mensagem="Alteração aplicada.", pedidos=[])
        return render_template("pedidos.html", mensagem="Pedido enviado para avaliação.", pedidos=[]), 202

    @app.get("/avaliacoes")
    def avaliacoes():
        if not professor(usuario_logado()):
            abort(403)
        with Session(engine) as banco:
            pedidos = banco.exec(select(Solicitacao).where(Solicitacao.estado == "Pendente").order_by(col(Solicitacao.destacada).desc(), col(Solicitacao.id))).all()
        return render_template("pedidos.html", pedidos=pedidos)

    @app.post("/avaliacoes/<int:pedido_id>")
    def avaliar(pedido_id):
        pessoa = usuario_logado()
        if not professor(pessoa):
            abort(403)
        decisao = request.form.get("decisao")
        if decisao not in ("aprovar", "reprovar", "destacar"):
            abort(400)
        with Session(engine) as banco:
            banco.connection().exec_driver_sql("BEGIN IMMEDIATE")
            pedido = banco.get(Solicitacao, pedido_id)
            if pedido is None:
                abort(404)
            if decisao == "destacar":
                if pedido.estado != "Pendente":
                    abort(409)
                pedido.destacada = not pedido.destacada
                banco.commit()
                return redirect(url_for("avaliacoes"))
            if pedido.estado != "Pendente" or pedido.usuario_id == pessoa.id:
                abort(409, "Pedido já avaliado ou feito pela sua própria conta.")
            if decisao == "aprovar":
                aplicar(banco, pedido)
            pedido.estado = "Aprovada" if decisao == "aprovar" else "Reprovada"
            pedido.avaliador_id = pessoa.id
            pedido.avaliado_em = datetime.now(timezone.utc)
            banco.commit()
        return redirect(url_for("avaliacoes"))
