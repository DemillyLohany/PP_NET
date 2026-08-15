from flask import Blueprint, render_template, request, redirect, url_for, session
from dados_estaticos import buscar_usuario_logado

perfil_bp = Blueprint('perfil', __name__)

@perfil_bp.route('/perfil')
def exibir_perfil():
    usuario = buscar_usuario_logado()

    if usuario:
        foto_padrao = usuario.get('foto_url') 
    
    foto_atual = session.get('foto_customizada', foto_padrao)
    
    return render_template('perfil.html', usuario=usuario, foto_atual=foto_atual)


@perfil_bp.route('/atualizar-foto', methods=['POST'])
def atualizar_foto():
    nova_url = request.form.get('foto_url')
    if nova_url:
        session['foto_customizada'] = nova_url
        
    return redirect(url_for('perfil.exibir_perfil'))