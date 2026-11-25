import json

from flask import Blueprint, redirect, render_template, url_for
from sqlmodel import Session, col, select

from servidor.database import engine
from servidor.models import Disciplina, Conteudo, Material, Solicitacao, Usuario
from servidor.perfil import usuario_logado
from servidor.regras import professor

notificacoes_bp = Blueprint("notificacoes", __name__)


@notificacoes_bp.get("/notificacoes")
def tela_notificacoes():
    pessoa = usuario_logado()
    if pessoa is None:
        return redirect(url_for("home"))
    pode_avaliar = professor(pessoa)
    notificacoes = []
    if pessoa is not None:
        with Session(engine) as banco:
            consulta = select(Solicitacao)
            if pode_avaliar:
                consulta = consulta.where(Solicitacao.estado == "Pendente")
            else:
                consulta = consulta.where(Solicitacao.usuario_id == pessoa.id)
            consulta = consulta.order_by(col(Solicitacao.destacada).desc(), col(Solicitacao.id).desc())
            for pedido in banco.exec(consulta).all():
                dados = json.loads(pedido.dados)
                autor = banco.get(Usuario, pedido.usuario_id)
                modelos = {"Disciplina": Disciplina, "Conteudo": Conteudo, "Material": Material}
                modelo = modelos.get(pedido.entidade)
                item = banco.get(modelo, pedido.alvo_id) if modelo is not None and pedido.alvo_id is not None and pedido.acao != "Cadastro" else None
                titulo = dados.get("titulo") or dados.get("nome") or getattr(item, "titulo", None) or getattr(item, "nome", None)
                notificacoes.append(dict(
                    pedido=pedido, autor=autor.nome if autor else "Usuário não disponível",
                    titulo=titulo,
                    descricao=dados.get("descricao"), url=dados.get("url"),
                    pode_decidir=pode_avaliar and pedido.usuario_id != pessoa.id,
                ))
    return render_template("notificacoes.html", notificacoes=notificacoes)
