from flask import Blueprint, render_template, request, redirect, url_for, session
from app.extensions import db
from app.models import Tarefa
from app.forms import TarefaForm
from functools import wraps

main_bp = Blueprint('main', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # Recuperamos o ID do utilizador atual da sessão
    id_do_dono = session['user_id']

    form = TarefaForm()

    if form.validate_on_submit():
        nova_tarefa = Tarefa(
            titulo=form.titulo.data, 
            descr=form.descricao.data,
            prazo=form.prazo.data,
            prioridade=form.prioridade.data,
            dono_id=id_do_dono
            )
        db.session.add(nova_tarefa)
        db.session.commit()
        return redirect(url_for('main.home'))

    tarefas_banco = Tarefa.query.filter_by(dono_id=id_do_dono).all()

    return render_template(
        'index.html',
        titulo='TO DO LIST',
        tarefas=tarefas_banco,
        form=form
    )

@main_bp.route('/sobre')
def about():
    return render_template('sobre.html')

@main_bp.route('/deletar/<int:id>')
@login_required
def delete(id):
    tarefa = Tarefa.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return redirect(url_for('main.home'))

@main_bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    tarefa = Tarefa.query.get_or_404(id)

    if tarefa.dono_id != session['user_id']:
        return "Você não tem permissão para editar esta tarefa.", 403
    
    form = TarefaForm(obj=tarefa)

    if form.validate_on_submit():
        form.populate_obj(tarefa)
        db.session.commit()
        return redirect(url_for('main.home'))   

    return render_template('update.html', tarefa=tarefa)