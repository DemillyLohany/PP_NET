from flask import Blueprint, render_template
#from dados_estaticos import TODOS_OS_CONTEUDOS, buscar_disciplina
from sqlmodel import Session,select
from database import engine
from models import Disciplina,Conteudo

conteudos_bp = Blueprint('conteudos', __name__)

@conteudos_bp.route('/conteudo/<int:disciplina_id>')
def conteudo(disciplina_id):
    #disciplina = buscar_disciplina(disciplina_id)
    with Session(engine) as session:
            disciplina = session.get(Disciplina,disciplina_id) #procura a disciplina pelo IDzinho dela
            if not disciplina: #se não existir a tal disciplina
                  return "Não encontramos a disciplina",404
            busca = select(Conteudo).where(Conteudo.disciplina_id==disciplina_id) #os conteúdos são procuraods, mas apenas e somente dessa disciplina
            lista_conteudos = session.exec(busca).all()
            print("CONTEÚDOS ENCONTRADOS:", lista_conteudos) 
            return render_template('conteudos.html', disciplina=disciplina, conteudos=lista_conteudos)
#   conteudos_filtrados = [c for c in TODOS_OS_CONTEUDOS if c['disciplina_id'] == disciplina_id]

#    return render_template('conteudos.html', disciplina=disciplina, conteudos=conteudos_filtrados)