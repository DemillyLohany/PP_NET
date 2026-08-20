#aqui os dados iniciais que estão inseridos no banquinho
from sqlmodel import Session
from database import engine
from models import Disciplina,Conteudo,Material                                                                                                                                                                                       
from dados_estaticos import DISCIPLINAS, TODOS_OS_CONTEUDOS

# with Session(engine) as session: 
#     for dicionario in DISCIPLINAS: #para cada dicionário que está em disciplina...
#         disciplina = Disciplina( #cria uma disciplina nova com base no dicionario já existente
#             id=dicionario['id'],
#             nome= dicionario['nome'],
#             descricao= dicionario['descricao']
#         ) #valores do dicionario são separados 
#         session.add(disciplina) # deixa disciplina para ser salvo no banco
#     session.commit()#faz a alteração no banco e adciona os valores

# #Fazendo o mesmo com conteúdos...
# with Session(engine) as session: 
#     for dicionario in TODOS_OS_CONTEUDOS: 
#         conteudo = Conteudo(
#             id=dicionario['id'],
#             titulo= dicionario['titulo'],
#             descricao= dicionario['descricao'],
#             disciplina_id= dicionario['disciplina_id']
#         ) 
#         session.add(conteudo)
#     session.commit()

# #Fazendo o mesmo com materiais...
# with Session(engine) as session: 
#     for dicionario in TODOS_OS_CONTEUDOS:
#         for material in dicionario['materiais']:
#             material = Material(
#                 titulo = material['titulo'],
#                 url = material['url'],
#                 conteudo_id=dicionario['id']
#             )
#             session.add(material)
#         session.commit()