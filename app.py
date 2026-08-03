from flask import Flask, render_template
from conteudos import conteudos_bp
from materiais import materiais_bp

app = Flask(__name__)
app.secret_key = 'super-secret-key'

#registra os componentes mantendo o mapeamento correto (com blueprints)
app.register_blueprint(conteudos_bp)
app.register_blueprint(materiais_bp)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

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