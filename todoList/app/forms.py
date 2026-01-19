from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Fazer Login')

class CadastroForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('Senha', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cadastrar')

class TarefaForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    descricao = TextAreaField('Descrição')
    prazo = DateField('Prazo de Entrega', format='%Y-%m-%d', validators=[DataRequired()])
    prioridade = SelectField('Prioridade', choices=[
        ('Baixa', 'Baixa'),
        ('Média', 'Média'),
        ('Alta', 'Alta')
    ])
    submit = SubmitField('Salvar Tarefa')