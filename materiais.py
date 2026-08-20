from flask import Blueprint, render_template, redirect, url_for
# from dados_estaticos import buscar_conteudo, buscar_disciplina
from sqlmodel import Session,select
from database import engine
from models import Disciplina, Conteudo, Material

materiais_bp = Blueprint('materiais', __name__)

@materiais_bp.route('/materiais/<int:conteudo_id>')
def ver_materiais(conteudo_id):
    with Session(engine) as session:
        busca = select(Conteudo).where(Conteudo.id==conteudo_id)
        conteudo_atual = session.exec(busca).first()
        if not conteudo_atual: #se não existir a tal disciplina
            return "Não encontramos o conteúdo",404
        busca = select(Disciplina).where(Disciplina.id==conteudo_atual.disciplina_id) 
        disciplina_atual = session.exec(busca).first()
        busca = select(Material).where(Material.conteudo_id==conteudo_id)
        lista_materiais= session.exec(busca).all()
        print("MATERIAIS ENCONTRADOOOOS:", lista_materiais) 
        return render_template('materiais.html', disciplina=disciplina_atual, conteudo=conteudo_atual,materiais=lista_materiais)
    # conteudo_atual = buscar_conteudo(conteudo_id)ss
    
    # if not conteudo_atual:
    #     return "Conteúdo não encontrado", 404
        
    # disciplina_atual = buscar_disciplina(conteudo_atual['disciplina_id'])

    # return render_template(
    #     'materiais.html', disciplina=disciplina_atual, conteudo=conteudo_atual)


# # Atenção! As rotas a seguir estão incompletas e foram adicionadas para evitar erros de redirecionamento

# # adiciona materiais (Redireciona para atualizar a tela)
# @materiais_bp.route('/adicionar_material/<int:conteudo_id>', methods=['POST'])
# def adicionar_material(conteudo_id):
#     return redirect(url_for('materiais.ver_materiais', conteudo_id=conteudo_id))

# # exclue materiais (Redireciona para atualizar a tela)
# @materiais_bp.route('/excluir_material/<int:conteudo_id>/<int:index>', methods=['POST'])
# def excluir_material(conteudo_id, index):
#     return redirect(url_for('materiais.ver_materiais', conteudo_id=conteudo_id))