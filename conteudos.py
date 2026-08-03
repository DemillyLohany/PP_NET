from flask import Blueprint, render_template

conteudos_bp = Blueprint('conteudos', __name__)

todos_os_conteudos = [
        {'id': 101, 'titulo': 'Introdução ao Flask e Rotas', 'disciplina_id': '1',
        'materiais': [{ 'titulo': 'Slides da Aula 1', 'url': 'exemplo.com/flask-slides' },
        { 'titulo': 'Videoaula: Configuração', 'url': 'youtube.com/flask-init' }]
        },

        {'id': 102, 'titulo': 'Uso de Templates com Jinja2', 'disciplina_id': '1',
        'materiais': [{ 'titulo': 'Exercícios de Herança', 'url': 'exemplo.com/jinja-lista' }
        ]
        },

        {'id': 201, 'titulo': 'Modelagem de Tabelas e Chaves', 'disciplina_id': '2',
        'materiais': [{ 'titulo': 'Apostila de SQLModel', 'url': 'exemplo.com/sqlmodel-pdf' },
        { 'titulo': 'Diagrama do Banco', 'url': 'exemplo.com/diagrama' }]
        },

        {'id': 301, 'titulo': 'Cores e Tipografia para Web', 'disciplina_id': '3',
        'materiais': [
        { 'titulo': 'Guia de UI/UX', 'url': 'exemplo.com/design-guia' }]
        }
    ]



@conteudos_bp.route('/conteudo/<disciplina_id>')
def conteudo(disciplina_id):
    # pega apenas os conteudos da disciplina certa
    conteudos_filtrados = [c for c in todos_os_conteudos if c['disciplina_id'] == disciplina_id]

    #cria a estrutura que o template conteudo.html deve receber
    valores = {'id': disciplina_id, 'conteudos': conteudos_filtrados}

    return render_template('conteudo.html', **valores)