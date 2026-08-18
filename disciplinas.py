from flask import Blueprint, render_template
#from dados_estaticos import DISCIPLINAS
from sqlmodel import Session,select
from database import engine
from models import Disciplina

disciplinas_bp = Blueprint('disciplinas', __name__)

@disciplinas_bp.route('/disciplinas')
def disciplinas():
    with Session(engine) as session:
        busca = select(Disciplina) # procura os dados da disxiplina
        lista_disciplinas = session.exec(busca).all() # mostra todos os dados encontrados na busca e esse resultado é guardado em 'lista_disciplinas'
        return render_template('disciplinas.html', lista_disciplinas=lista_disciplinas)
    #return render_template('disciplinas.html', lista_disciplinas=DISCIPLINAS)