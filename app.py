from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'super-secret-key'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# carrega os conteudos filtrados pelo id da disciplina clicada
@app.route('/conteudo/<disciplina_id>')
def conteudo(disciplina_id):
    # simula uma tabela de conteudos com chave estrangeira (disciplina_id)
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

    # varre a lista e pegar apenas os conteudos da disciplina certa
    conteudos_filtrados = [c for c in todos_os_conteudos if c['disciplina_id'] == disciplina_id]

    # cria a estrutura que o template conteudo.html espera receber
    valores = {'id': disciplina_id, 'conteudos': conteudos_filtrados}

    return render_template('conteudo.html', **valores)

@app.route('/disciplinas')
def disciplinas():
    valores = {}
    valores['lista_disciplinas'] = [
        { 'id': 1, 'nome': 'Programação de Sistemas para Internet', 'descricao': 'Desenvolvimento com Python e Flask' },
        { 'id': 2, 'nome': 'Banco de Dados', 'descricao': 'Modelagem e uso de SQLModel' },
        { 'id': 3, 'nome': 'Design Web', 'descricao': 'Interface, UI/UX e folhas de estilo CSS' }
    ]
    return render_template('disciplinas.html', **valores)

if __name__ == '__main__':
    app.run(debug=True, port=5000)