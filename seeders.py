from sqlmodel import Session
from models import Disciplina
from database import engine

def seed_disciplinas():
    with Session(engine) as session:
        #so criar os bagulho
        disciplinas = [
            Disciplina(
                nome="Instalação e Configuração de Servidores",
                descricao="Instalação, configuração e administração básica de infraestrutura de servidores web e de banco de dados. Administração de sistemas operacionais abertos e proprietários."
                ),
            Disciplina(
                nome="Programação de Sistemas para Internet",
                descricao="Conceitos de sistemas para internet. Desenvolvimento de aplicações web com programação no cliente e servidor. Controles de estado e acesso. Ferramentas de relatório. Desenvolvimento com padrão MVC, tecnologia AJAX e mapeamento objetorelacional."
            ),
            Disciplina(
                nome="Banco de Dados",
                descricao="Conceitos de banco de dados. Modelos de dados e linguagens de modelagem. Projeto de banco de dados. Linguagem de consulta estruturada (SQL). Visões, gatilhos, procedimentos armazenados, transações, cursores e funções."
            ),
            Disciplina(
                nome="Analise e Projeto Orientado e Objeto",
                descricao="Conceitos de análise e projeto orientados a objetos. Linguagem de modelagem unificada (UML). Objetivos, fluxo de trabalho e resultados das fases de análise de requisitos, análise e projeto do sistema."
            )
            


        ]

if __name__ == "__main__":
    seed_disciplinas