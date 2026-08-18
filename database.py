from sqlmodel import SQLModel,create_engine,Session #importa as coisinhas do sqlmodel
from models import Usuario,Conteudo,Disciplina,Material #importa as classes que estão em models.py, ou seja, do banco

engine = create_engine("sqlite:///dados.db",echo=True)# conecta com o banco e, por causa do echo=True, mostra no terminal o que está sendo feito no banco
SQLModel.metadata.create_all(engine) # cria as tabelas no banco levando em conta as classes criadas em models
