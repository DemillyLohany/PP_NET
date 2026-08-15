from flask import Blueprint, render_template
from dados_estaticos import DISCIPLINAS

disciplinas_bp = Blueprint('disciplinas', __name__)

@disciplinas_bp.route('/disciplinas')
def disciplinas():
    return render_template('disciplinas.html', lista_disciplinas=DISCIPLINAS)