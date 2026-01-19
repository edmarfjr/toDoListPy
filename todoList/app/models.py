from app.extensions import db

class Conta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # Relacionamento: Uma conta tem muitos itens na lista (tabela Usuario)
    itens = db.relationship('Tarefa', backref='dono', lazy=True)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descr = db.Column(db.String(100), nullable=False)
    prazo = db.Column(db.Date, nullable=True)
    prioridade = db.Column(db.String(20), nullable=True)
    dono_id = db.Column(db.Integer, db.ForeignKey('conta.id'), nullable=False)