from flask import Blueprint, render_template, redirect, url_for
from dados_estaticos import buscar_conteudo, buscar_disciplina

materiais_bp = Blueprint('materiais', __name__)

@materiais_bp.route('/materiais/<int:conteudo_id>')
def ver_materiais(conteudo_id):
    conteudo_atual = buscar_conteudo(conteudo_id)
    
    if not conteudo_atual:
        return "Conteúdo não encontrado", 404
        
    disciplina_atual = buscar_disciplina(conteudo_atual['disciplina_id'])

    return render_template(
        'materiais.html', disciplina=disciplina_atual, conteudo=conteudo_atual)


# Atenção! As rotas a seguir estão incompletas e foram adicionadas para evitar erros de redirecionamento

# adiciona materiais (Redireciona para atualizar a tela)
@materiais_bp.route('/adicionar_material/<int:conteudo_id>', methods=['POST'])
def adicionar_material(conteudo_id):
    return redirect(url_for('materiais.ver_materiais', conteudo_id=conteudo_id))

# exclue materiais (Redireciona para atualizar a tela)
@materiais_bp.route('/excluir_material/<int:conteudo_id>/<int:index>', methods=['POST'])
def excluir_material(conteudo_id, index):
    return redirect(url_for('materiais.ver_materiais', conteudo_id=conteudo_id))