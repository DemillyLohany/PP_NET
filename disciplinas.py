from flask import Blueprint, render_template,request, redirect, url_for
#from dados_estaticos import DISCIPLINAS
from sqlmodel import Session,select
from database import engine
from models import Disciplina

disciplinas_bp = Blueprint('disciplinas', __name__)
# Vamos fazer o famoso CRUD (Create, Read, Update, Delete)

# Read - essa é a rota que permite que as disciplinas sejam lidas, mostradas
@disciplinas_bp.route('/disciplinas')
def disciplinas():
    with Session(engine) as session:
        busca = select(Disciplina) # procura os dados da disxiplina
        lista_disciplinas = session.exec(busca).all() # mostra todos os dados encontrados na busca e esse resultado é guardado em 'lista_disciplinas'
        return render_template('disciplinas.html', lista_disciplinas=lista_disciplinas)
    #return render_template('disciplinas.html', lista_disciplinas=DISCIPLINAS)

 # serve para mostrar a tela que cria a disciplina
@disciplinas_bp.route('/disciplinas/criar')
def criar():
    return render_template('criar_disciplina.html')

# Create - aqui, as disciplinas são criadas
@disciplinas_bp.route('/disciplinas/criar', methods=['POST'])
def criar_disciplina():
    print("FORMULÁRIO RECEBIDO:", request.form)
    nome = request.form.get('nome') # pega o nome do formulário no html
    descricao = request.form.get('descricao') # mesma lógica
    nova_disciplina = Disciplina(
        nome=nome,
        descricao=descricao
    ) # a disciplina é criada com base nos dados enviados lá pelo formulário
    with Session(engine) as session:
        session.add(nova_disciplina) # a nova disciplina é inserida no banco 
        session.commit() # confirma-se a entrada da disciplina no banco

    return redirect(url_for('disciplinas.disciplinas')) 

# Update - disciplinas editadas
@disciplinas_bp.route('/disciplinas/editar/<int:disciplina_id>', methods=['GET', 'POST'])
def editar_disciplina(disciplina_id):
    with Session(engine) as session:
        disciplina = session.get(Disciplina, disciplina_id) # comn base no id, a ddisciplina é escolhida para  a edição
        if disciplina is None: #se não tiver essa disciplina, volta mensagem do erro 404
            return "Disciplina não encontrada", 404
        if request.method == 'POST':
            disciplina.nome = request.form.get('nome')
            disciplina.descricao = request.form.get('descricao')
            session.add(disciplina)
            session.commit()
            return redirect(url_for('disciplinas.disciplinas')) 
    return render_template('editar_disciplina.html',disciplina=disciplina)

# Delete - a disciplina vai de vasco
@disciplinas_bp.route('/disciplinas/excluir/<int:disciplina_id>', methods=['POST'])
def excluir_disciplina(disciplina_id):
    with Session(engine) as session:
        disciplina = session.get(Disciplina, disciplina_id)
        if disciplina is None:
            return "Disciplina não encontrada", 404
        session.delete(disciplina) # deleta a disciplina do banquinho
        session.commit()
    return redirect(url_for('disciplinas.disciplinas'))