from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from typing import List, Optional

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # identificação Única (do SUAP)
    matricula: str = Field(nullable=False, unique=True, index=True)
    nome: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False)
    
    tipo_vinculo: str = Field(nullable=False) # Ex: "aluno", "servidor (Docente)".
    
    curso: Optional[str] = Field(default=None)   
    setor: Optional[str] = Field(default=None)   
    campus: Optional[str] = Field(default=None) 
    
    # Obs.: seria legal que a foto viesse do SUAP (foto_url), mas podesse ser alterada pelo usuário
    foto_url: Optional[str] = Field(default=None)



class Disciplina(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(nullable=False)
    descricao: str = Field(nullable=False)
    
    # isso serve para listar todos os conteudos vinculados a esta disciplina
    conteudos: List["Conteudo"] = Relationship(back_populates="disciplina")

class Conteudo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(nullable=False)
    descricao: Optional[str] = Field(default=None)
    
    # faz a ligacao direta deste conteudo com o id de uma disciplina
    disciplina_id: int = Field(foreign_key="disciplina.id", nullable=False)

    # serve para acessar os dados da disciplina dona deste conteudo
    disciplina: Disciplina = Relationship(back_populates="conteudos")
    
    materiais: List["Material"] = Relationship(back_populates="conteudo")

class Material(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(nullable=False)
    url: str = Field(nullable=False)
    
    # faz a ligacao deste material especifico com o id de um conteudo
    conteudo_id: int = Field(foreign_key="conteudo.id", nullable=False)
    
    # serve para acessar as informacoes do conteudo dono deste material
    conteudo: Conteudo = Relationship(back_populates="materiais")