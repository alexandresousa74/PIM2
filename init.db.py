import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO clientes (nome, telefone, cidade) VALUES (?, ?, ?)",
            ('Felipe Alves', '19 22399548', 'Americana')
            )

cur.execute("INSERT INTO clientes (nome, telefone, cidade) VALUES (?, ?, ?)",
            ('Alexandre Sousa', '19 92556455', 'Holambra')
            )

cur.execute("INSERT INTO vendas (cliente, produto, qtde, valor_total, pago, entregue) VALUES (?, ?, ?, ?, ?, ?)",
            ('Felipe', 'Pudim', 2, 30, 'Não', 'Sim')
            )

cur.execute("INSERT INTO vendas (cliente, produto, qtde, valor_total, pago, entregue) VALUES (?, ?, ?, ?, ?, ?)",
            ('Alexandre', 'Caldo', 1, 18, 'Sim', 'Não')
            )

cur.execute("INSERT INTO produtos (descricao, peso, volume, sabor, valor_custo, valor_venda) VALUES (?, ?, ?, ?, ?, ?)",
            ('Pudim', 100, 100, 'Leite Condensado', 10, 15)
            )

cur.execute("INSERT INTO produtos (descricao, peso, volume, sabor, valor_custo, valor_venda) VALUES (?, ?, ?, ?, ?, ?)",
            ('Caldo', 200, 50, 'Queijo', 12, 18)
            )

connection.commit()
connection.close()
