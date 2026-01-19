from flask import Blueprint, render_template, request, redirect, url_for, session
from app.extensions import db
from app.models import Conta
from app.forms import LoginForm, CadastroForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if 'logged_in' in session:
        return redirect(url_for('main.home'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user_digitado = form.username.data
        senha_digitada = form.password.data

        # Verifica se o usuário existe no banco de dados
        conta = Conta.query.filter_by(username=user_digitado, password=senha_digitada).first()
        
        if conta:
            # Autenticação bem-sucedida
            session['logged_in'] = True
            session['user_id'] = conta.id
            session['user_name'] = conta.username
            return redirect(url_for('main.home'))
        else:
            return render_template('login.html', form=form, erro="Usuário ou senha incorretos.")


    return render_template('login.html',form=form)

@auth_bp.route('/logout')
def logout():
    session.clear() # Limpa tudo da sessão
    return redirect(url_for('auth.login'))

@auth_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if 'logged_in' in session:
        return redirect(url_for('main.home'))
    
    form = CadastroForm()

    if form.validate_on_submit():
        if Conta.query.filter_by(username=form.username.data).first():
            return render_template('registrar.html', form=form, erro="Este usuário já existe!")
        novo_usuario = Conta(
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('registrar.html',form=form)
