from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'super-secret-key'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/conteudo/<id>')
def conteudo(id):
    valores = { 'id': id }
    valores['titulo'] = 'Funções'
    valores['materiais'] = [
        { 'titulo': 'Slides da Aula', 'url': 'exemplo.com/jsahdfkjsdhf' },
        { 'titulo': 'Videoaula', 'url': 'youtube.com/jsahdfkjsdhf' }
    ]
    return render_template('conteudo.html', **valores)