from flask import Flask, render_template, redirect, url_for
from conteudos import conteudos_bp
from materiais import materiais_bp
from disciplinas import disciplinas_bp
from perfil import perfil_bp
from notificacoes import notificacoes_bp
from database import engine

app = Flask(__name__)
app.secret_key = 'super-secret-key'

#registra os componentes mantendo o mapeamento correto (com blueprints)
app.register_blueprint(conteudos_bp)
app.register_blueprint(materiais_bp)
app.register_blueprint(disciplinas_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(notificacoes_bp)

# Redireciona a raiz '/' para a tela de disciplinas
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def tela_login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True, port=5000)