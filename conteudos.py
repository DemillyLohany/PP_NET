from flask import Blueprint, render_template
from dados_estaticos import TODOS_OS_CONTEUDOS, buscar_disciplina

conteudos_bp = Blueprint('conteudos', __name__)

@conteudos_bp.route('/conteudo/<int:disciplina_id>')
def conteudo(disciplina_id):
    disciplina = buscar_disciplina(disciplina_id)

    # Seleciona somente os conteúdos da disciplina em questão
    conteudos_filtrados = [c for c in TODOS_OS_CONTEUDOS if c['disciplina_id'] == disciplina_id]

    return render_template('conteudos.html', disciplina=disciplina, conteudos=conteudos_filtrados)