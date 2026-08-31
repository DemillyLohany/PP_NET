# from flask import Blueprint, render_template, request, redirect, url_for, session
# from dados_estaticos import buscar_usuario_logado

# perfil_bp = Blueprint('perfil', __name__)

# @perfil_bp.route('/perfil')
# def exibir_perfil():
#     usuario = buscar_usuario_logado()

#     if usuario:
#         foto_padrao = usuario.get('foto_url') 
    
#     foto_atual = session.get('foto_customizada', foto_padrao)
    
#     return render_template('perfil.html', usuario=usuario, foto_atual=foto_atual)


# @perfil_bp.route('/atualizar-foto', methods=['POST'])
# def atualizar_foto():
#     nova_url = request.form.get('foto_url')
#     if nova_url:
#         session['foto_customizada'] = nova_url
        
#     return redirect(url_for('perfil.exibir_perfil'))

from flask import Blueprint, render_template
from sqlmodel import Session,select
from database import engine
from models import Usuario

perfil_bp = Blueprint('perfil', __name__)

@perfil_bp.route('/perfil')
def exibir_perfil():
    with Session(engine) as session:
        busca = select(Usuario) # procura os dados do usuario
        dados_usuario = session.exec(busca).all() # mostra todos os dados encontrados na busca e esse resultado é guardado em 'dados_usuario'
        return render_template('perfil.html', dados_usuario=dados_usuario)