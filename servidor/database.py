from sqlmodel import SQLModel,create_engine,Session  # importa as coisinhas do sqlmodel
from servidor.models import Usuario, Conteudo, Disciplina, Material # importa as classes que estão em models.py, ou seja, do banco

from pathlib import Path

caminho_banco = Path(__file__).resolve().parent.parent / "dados.db"
engine = create_engine("sqlite:///" + caminho_banco.as_posix(), connect_args={"timeout": 15})  # conecta com o banco e, por causa do echo=True, mostra no terminal o que está sendo feito no banco
SQLModel.metadata.create_all(engine)  # cria as tabelas no banco levando em conta as classes criadas em models

# acrescenta o que falta sem apagar os dados
from sqlalchemy import inspect
with engine.begin() as conexao:
    for tabela in ("conteudo", "material"):
        colunas = {c["name"] for c in inspect(conexao).get_columns(tabela)}
        if "autor_id" not in colunas:
            conexao.exec_driver_sql(f"ALTER TABLE {tabela} ADD COLUMN autor_id INTEGER REFERENCES usuario(id)")
        if "criado_em" not in colunas:
            conexao.exec_driver_sql(f"ALTER TABLE {tabela} ADD COLUMN criado_em DATETIME")

    if "destacada" not in {c["name"] for c in inspect(conexao).get_columns("solicitacao")}:
        conexao.exec_driver_sql("ALTER TABLE solicitacao ADD COLUMN destacada BOOLEAN NOT NULL DEFAULT 0")
