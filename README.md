# N.E.T. — Núcleo de Estudos Técnicos

## Rodar localmente

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000/` no navegador.

A pasta `templates/` contém as páginas Jinja. A pasta `templates/componentes/` contém o menu e o rodapé compartilhados. Os arquivos CSS ficam em `static/`.

O arquivo `dados.db` não acompanha o pacote de código corrigido; ele deve ser mantido localmente quando já tiver dados importantes.

passo a passo:

cd PP_NET
python -m venv .venv (se ainda não tiver ambiente virtual, crie)
.venv\Scripts\activate
pip install -r requirements.txt
python app.py

Abra:
http://127.0.0.1:5000/
