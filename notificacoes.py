from flask import Blueprint, render_template
from dados_estaticos import NOTIFICACOES

notificacoes_bp = Blueprint('notificacoes', __name__)

@notificacoes_bp.route('/notificacoes')
def tela_notificacoes():
    return render_template('notificacoes.html', dados=NOTIFICACOES)