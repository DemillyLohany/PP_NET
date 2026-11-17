from datetime import datetime

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

    # liga o usuário ao que ele criou (usado na tela de perfil)
    conteudos: List["Conteudo"] = Relationship(back_populates="autor")
    materiais: List["Material"] = Relationship(back_populates="autor")


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
    
    disciplina_id: int = Field(foreign_key="disciplina.id", nullable=False)

    disciplina: Disciplina = Relationship(back_populates="conteudos")

    # quem criou este conteudo (fica vazio quando a pessoa cria sem estar logada no SUAP)
    autor_id: Optional[int] = Field(default=None, foreign_key="usuario.id")

    autor: Optional[Usuario] = Relationship(back_populates="conteudos")

    # quando este conteudo foi criado (aparece na tela de perfil)
    criado_em: datetime = Field(default_factory=datetime.now)
    
    materiais: List["Material"] = Relationship(back_populates="conteudo")

class Material(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(nullable=False)
    url: str = Field(nullable=False)
    
    conteudo_id: int = Field(foreign_key="conteudo.id", nullable=False)
    
    conteudo: Conteudo = Relationship(back_populates="materiais")

    # quem enviou este material (fica vazio quando a pessoa envia sem estar logada no SUAP)
    autor_id: Optional[int] = Field(default=None, foreign_key="usuario.id")

    # serve para acessar os dados de quem enviou
    autor: Optional[Usuario] = Relationship(back_populates="materiais")

    criado_em: datetime = Field(default_factory=datetime.now)