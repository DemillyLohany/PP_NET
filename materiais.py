from flask import Blueprint, render_template, request, redirect, url_for

materiais_bp = Blueprint('materiais', __name__)

@materiais_bp.route('/materiais/<int:conteudo_id>')
def ver_materiais(conteudo_id):
    from conteudos import todos_os_conteudos
    
    #busca o conteúdo especifico clicado
    conteudo_encontrado = next((c for c in todos_os_conteudos if c['id'] == conteudo_id), None)
    
    return render_template('materiais.html', conteudo=conteudo_encontrado)

@materiais_bp.route('/material/adicionar/<int:conteudo_id>', methods=['POST'])
def adicionar_material(conteudo_id):
    from conteudos import todos_os_conteudos
    
    titulo = request.form.get('titulo')
    url = request.form.get('url')
    
    for c in todos_os_conteudos:
        if c['id'] == conteudo_id:
            c['materiais'].append({'titulo': titulo, 'url': url})
            return redirect(url_for('materiais.ver_materiais', conteudo_id=conteudo_id))
            
    return redirect(url_for('home'))

@materiais_bp.route('/material/excluir/<int:conteudo_id>/<int:index>', methods=['POST'])
def excluir_material(conteudo_id, index):
    from conteudos import todos_os_conteudos
    
    for c in todos_os_conteudos:
        if c['id'] == conteudo_id:
            if 0 <= index < len(c['materiais']):
                c['materiais'].pop(index)
            return redirect(url_for('materiais.ver_materiais', conteudo_id=conteudo_id))
            
    return redirect(url_for('home'))