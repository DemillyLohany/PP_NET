from sqlmodel import SQLModel,Field
from pydantic import EmailStr

class Usuario(SQLModel, table=True):
    id:int = Field(default=None, primary_key=True)
    nome:str = Field(default=None, nullable=False)
    email:EmailStr = Field(default=None, nullable=False)
    senha:hash = Field(default=None, nullable=False)

class Disciplina(SQLModel, table=True):
    id:int = Field(default=None, primary_key=True)
    nome:str = Field(default=None, nullable=False)
    descricao:str = Field(default=None, nullable=False)

class Conteudo(SQLModel, table=True):
    id:int = Field(default=None, primary_key=True)
    titulo:str = Field(default=None, nullable=False)

class Material(SQLModel, table=True):
    id:int = Field(default=None, primary_key=True)