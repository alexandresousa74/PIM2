import sqlite3
import os, datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app = Flask('__name__')
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SECRET_KEY'] = 'your secret key'

db = SQLAlchemy(app)

class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    telefone = db.Column(db.String(10), nullable=False)
    cidade = db.Column(db.String(80), nullable=False)

class Vendas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datahora = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    cliente = db.Column(db.String(80), nullable=False)
    produto = db.Column(db.String(30), nullable=False)
    qtde = db.Column(db.Integer, nullable=False)
    pago = db.Column(db.String(10), nullable=False)
    entregue = db.Column(db.String(10), nullable=False)

class Produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(80), nullable=False)
    peso = db.Column(db.Integer, nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    sabor = db.Column(db.String(80), nullable=False)
    valor_custo = db.Column(db.String(10), nullable=False)
    valor_venda = db.Column(db.String(10), nullable=False)

@app.route('/')
def index():
    clientes = Clientes.query.all()
    return render_template('index.html', clientes = clientes)

def get_cliente(cliente_id):
    cliente = Clientes.query.filter_by(id=cliente_id).first()
    if cliente is None:
        abort(404)
    return cliente

@app.route('/<int:cliente_id>')
def cliente(cliente_id):
    cliente = get_cliente(cliente_id)
    return render_template('cliente.html', cliente = cliente)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        cidade = request.form['cidade']

        if not nome:
            flash('Digite o nome do cliente!')
        else:
            cliente = Clientes(nome=nome, telefone=telefone, cidade=cidade)
            db.session.add(cliente)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('novo_cliente.html')

@app.route('/<int:cliente_id>/edit', methods=('GET', 'POST'))
def edit(cliente_id):
    cliente = get_cliente(cliente_id)

    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        cidade = request.form['cidade']

        if not nome:
            flash('Digite o nome do cliente!')
        else:
            cliente.nome = nome
            cliente.telefone = telefone
            cliente.cidade = cidade
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('edit_cliente.html', cliente=cliente)

@app.route('/<int:cliente_id>/delete', methods=('POST',))
def delete(cliente_id):
    cliente = get_cliente(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    flash('"{}" foi apagado com sucesso!'.format(cliente.nome))
    return redirect(url_for('index'))