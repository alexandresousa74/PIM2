DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL,
    cidade TEXT NOT NULL
);

DROP TABLE IF EXISTS vendas;

CREATE TABLE vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    datahora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cliente TEXT NOT NULL,
    produto TEXT NOT NULL,
    qtde INTEGER NOT NULL,
    pago TEXT NOT NULL,
    entregue TEXT NOT NULL
);

DROP TABLE IF EXISTS produtos;

CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    peso INTEGER NOT NULL,
    volume INTEGER NOT NULL,
    sabor TEXT NOT NULL,
    valor_custo TEXT NOT NULL,
    valor_venda TEXT NOT NULL
);