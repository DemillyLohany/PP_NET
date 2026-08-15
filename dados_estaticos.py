
DISCIPLINAS = [
    { 'id': 1, 'nome': 'Programação de Sistemas para Internet', 'descricao': 'Desenvolvimento com Python e Flask' },
    { 'id': 2, 'nome': 'Banco de Dados', 'descricao': 'Modelagem e uso de SQLModel' },
    { 'id': 3, 'nome': 'Design Web', 'descricao': 'Interface, UI/UX e folhas de estilo CSS' }
]

TODOS_OS_CONTEUDOS = [
    {
        'id': 101, 
        'titulo': 'Introdução ao Flask e Rotas', 
        'descricao': 'Conceitos básicos sobre o microframework Flask, estrutura do projeto e criação de rotas HTTP.',
        'disciplina_id': 1,
        'materiais': [
            { 'titulo': 'Slides da Aula 1', 'url': 'exemplo.com/flask-slides' },
            { 'titulo': 'Videoaula: Configuração', 'url': 'youtube.com/flask-init' }
        ]
    },
    {
        'id': 102, 
        'titulo': 'Uso de Templates com Jinja2', 
        'descricao': 'Renderização dinâmica de páginas HTML, uso de estruturas de controle e herança de templates.',
        'disciplina_id': 1,
        'materiais': [
            { 'titulo': 'Exercícios de Herança', 'url': 'exemplo.com/jinja-lista' }
        ]
    },
    {
        'id': 201, 
        'titulo': 'Modelagem de Tabelas e Chaves', 
        'descricao': 'Criação e estruturação de bancos de dados relacionais, relacionamento entre tabelas e uso do SQLModel.',
        'disciplina_id': 2,
        'materiais': [
            { 'titulo': 'Apostila de SQLModel', 'url': 'exemplo.com/sqlmodel-pdf' },
            { 'titulo': 'Diagrama do Banco', 'url': 'exemplo.com/diagrama' }
        ]
    },
    {
        'id': 301, 
        'titulo': 'Cores e Tipografia para Web', 
        'descricao': 'Fundamentos de design visual para web, teoria das cores, hierarquia tipográfica e acessibilidade.',
        'disciplina_id': 3,
        'materiais': [
            { 'titulo': 'Guia de UI/UX', 'url': 'exemplo.com/design-guia' }
        ]
    }
]

USUARIO_LOGADO = {
    'id': 1,
    'matricula': '2023101110001',
    'nome': 'Aluno Teste',
    'nome_usual': 'Aluno Teste',
    'email': 'aluno.teste@aluno.ifrn.edu.br',
    'tipo_vinculo': 'Aluno',
    'curso': 'Técnico em Informática para Internet',
    'periodo': '4º ano',
    'situacao': 'Matriculado',
    'foto_url': 'https://ui-avatars.com/api/?name=Aluno+Teste&background=0D8ABC&color=fff',
    'disciplinas_matriculadas_ids': [1, 2, 3],
    'disciplinas_matriculadas': [
        'Programação de Sistemas para Internet',
        'Banco de Dados',
        'Design Web'
    ]
}


#funções auxiliares para buscar dados rapidamente

def buscar_usuario_logado():
    return USUARIO_LOGADO

def buscar_disciplina(disciplina_id):
    return next((d for d in DISCIPLINAS if d['id'] == int(disciplina_id)), None)

def buscar_conteudo(conteudo_id):
    return next((c for c in TODOS_OS_CONTEUDOS if c['id'] == int(conteudo_id)), None)

def buscar_conteudos_por_disciplina(disciplina_id):
    return [c for c in TODOS_OS_CONTEUDOS if c['disciplina_id'] == int(disciplina_id)]