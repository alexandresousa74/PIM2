import os, datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))

app = Flask('__name__')
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SECRET_KEY'] = 'V$3423faghYtGs'

db = SQLAlchemy(app)

class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    telefone = db.Column(db.String(10), nullable=False)
    cidade = db.Column(db.String(80), nullable=False)

class Vendas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datahora = db.Column(db.DateTime, default=datetime.datetime.now)
    cliente = db.Column(db.String(80), nullable=False)
    produto = db.Column(db.String(30), nullable=False)
    qtde = db.Column(db.Integer, nullable=False)
    valor_total = db.Column(db.String(10), nullable=False)
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
    vendas = Vendas.query.all()
    return render_template('index.html', vendas = vendas)

@app.route('/clientes')
def clientes():
    clientes = Clientes.query.all()
    return render_template('clientes.html', clientes = clientes)

@app.route('/produtos')
def produtos():
    produtos = Produtos.query.all()
    return render_template('produtos.html', produtos = produtos)

def get_cliente(cliente_id):
    cliente = Clientes.query.filter_by(id=cliente_id).first()
    if cliente is None:
        abort(404)
    return cliente

def get_venda(venda_id):
    venda = Vendas.query.filter_by(id=venda_id).first()
    if venda is None:
        abort(404)
    return venda

def get_produto(produto_id):
    produto = Produtos.query.filter_by(id=produto_id).first()
    if produto is None:
        abort(404)
    return produto

@app.route('/vendas/<int:venda_id>')
def venda(venda_id):
    venda = get_venda(venda_id)
    return render_template('venda.html', venda = venda)

@app.route('/clientes/<int:cliente_id>')
def cliente(cliente_id):
    cliente = get_cliente(cliente_id)
    return render_template('cliente.html', cliente = cliente)

@app.route('/produtos/<int:produto_id>')
def produto(produto_id):
    produto = get_produto(produto_id)
    return render_template('produto.html', produto = produto)

@app.route('/novo_cliente', methods=('GET', 'POST'))
def novo_cliente():
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
            return redirect(url_for('clientes'))
    return render_template('novo_cliente.html')

@app.route('/nova_venda', methods=('GET', 'POST'))
def nova_venda():
    if request.method == 'POST':
        cliente = request.form['cliente']
        produto = request.form['produto']
        qtde = request.form['qtde']
        valor_total = request.form['valor_total']
        pago = request.form['pago']
        entregue = request.form['entregue']

        if not cliente or not produto:
            flash('Digite o nome do cliente e do produto!')
        else:
            venda = Vendas(cliente=cliente, produto=produto, qtde=qtde, valor_total=valor_total, pago=pago, entregue=entregue)
            db.session.add(venda)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('nova_venda.html')

@app.route('/novo_produto', methods=('GET', 'POST'))
def novo_produto():
    if request.method == 'POST':
        descricao = request.form['descricao']
        peso = request.form['peso']
        volume = request.form['volume']
        sabor = request.form['sabor']
        valor_custo = request.form['valor_custo']
        valor_venda = request.form['valor_venda']

        if not descricao:
            flash('Digite a descrição do produto!')
        else:
            produto = Produtos(descricao=descricao, peso=peso, volume=volume, sabor=sabor, valor_custo=valor_custo, valor_venda=valor_venda)
            db.session.add(produto)
            db.session.commit()
            return redirect(url_for('produtos'))
    return render_template('novo_produto.html')

@app.route('/clientes/<int:cliente_id>/edit', methods=('GET', 'POST'))
def edit_cliente(cliente_id):
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
            return redirect(url_for('clientes'))

    return render_template('edit_cliente.html', cliente=cliente)

@app.route('/clientes/<int:cliente_id>/delete', methods=('POST',))
def delete_cliente(cliente_id):
    cliente = get_cliente(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    flash('"{}" foi apagado com sucesso!'.format(cliente.nome))
    return redirect(url_for('clientes'))

@app.route('/vendas/<int:venda_id>/edit', methods=('GET', 'POST'))
def edit_venda(venda_id):
    venda = get_venda(venda_id)

    if request.method == 'POST':
        cliente = request.form['cliente']
        produto = request.form['produto']
        qtde = request.form['qtde']
        valor_total = request.form['valor_total']
        pago = request.form['pago']
        entregue = request.form['entregue']

        if not cliente or not produto:
            flash('Digite o nome do cliente e do produto!')
        else:
            venda.cliente=cliente
            venda.produto=produto
            venda.qtde=qtde
            venda.valor_total=valor_total
            venda.pago=pago
            venda.entregue=entregue
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('edit_venda.html', venda=venda)

@app.route('/<int:venda_id>/delete', methods=('POST',))
def delete_venda(venda_id):
    venda = get_venda(venda_id)
    db.session.delete(venda)
    db.session.commit()
    flash('"{}" foi apagado com sucesso!'.format(venda.datahora))
    return redirect(url_for('index'))

@app.route('/produtos/<int:produto_id>/edit', methods=('GET', 'POST'))
def edit_produto(produto_id):
    produto = get_produto(produto_id)

    if request.method == 'POST':
        descricao = request.form['descricao']
        peso = request.form['peso']
        volume = request.form['volume']
        sabor = request.form['sabor']
        valor_custo = request.form['valor_custo']
        valor_venda = request.form['valor_venda']

        if not descricao:
            flash('Digite a descrição do produto!')
        else:
            produto.descricao = descricao
            produto.peso = peso
            produto.volume = volume
            produto.sabor = sabor
            produto.valor_custo = valor_custo
            produto.valor_venda = valor_venda
            db.session.commit()
            return redirect(url_for('produtos'))

    return render_template('edit_produto.html', produto=produto)

@app.route('/produtos/<int:produto_id>/delete', methods=('POST',))
def delete_produto(produto_id):
    produto = get_produto(produto_id)
    db.session.delete(produto)
    db.session.commit()
    flash('"{}" foi apagado com sucesso!'.format(produto.descricao))
    return redirect(url_for('produtos'))