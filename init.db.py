import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO clientes (nome, telefone, cidade) VALUES (?, ?, ?)",
            ('João Grilo', '99548', 'Taperoá')
            )

cur.execute("INSERT INTO clientes (nome, telefone, cidade) VALUES (?, ?, ?)",
            ('Chicó', '56455', 'Taperoá')
            )

cur.execute("INSERT INTO vendas (cliente, produto, qtde, pago, entregue) VALUES (?, ?, ?, ?, ?)",
            ('João Grilo', 'Doce', 2, 'Não', 'Sim')
            )

cur.execute("INSERT INTO vendas (cliente, produto, qtde, pago, entregue) VALUES (?, ?, ?, ?, ?)",
            ('Chicó', 'Salgado', 5, 'Sim', 'Não')
            )

cur.execute("INSERT INTO produtos (descricao, peso, volume, sabor, valor_custo, valor_venda) VALUES (?, ?, ?, ?, ?, ?)",
            ('Doce', 50, 200, 'Doce', 10, 15)
            )

cur.execute("INSERT INTO produtos (descricao, peso, volume, sabor, valor_custo, valor_venda) VALUES (?, ?, ?, ?, ?, ?)",
            ('Salgado', 100, 50, 'Salgado', 12, 14)
            )

connection.commit()
connection.close()
