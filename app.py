from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "123"

# conexão
def conectar():
    return sqlite3.connect("database.db")

# criar banco
def init_db():
    con = conectar()
    cur = con.cursor()

    # tabela usuario
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        senha TEXT
    )
    """)

    # tabela produto (projeto real)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        descricao TEXT,
        categoria TEXT,
        status TEXT,
        usuario_id INTEGER
    )
    """)

    con.commit()
    con.close()

init_db()

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        con = conectar()
        cur = con.cursor()

        cur.execute("SELECT * FROM usuario WHERE email = ? AND senha = ?", (email, senha))
        usuario = cur.fetchone()

        if usuario:
            session['usuario_id'] = usuario[0]
            return redirect('/')

    return render_template('login.html')

# ---------------- CADASTRO ----------------
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        con = conectar()
        cur = con.cursor()

        cur.execute("INSERT INTO usuario (nome, email, senha) VALUES (?, ?, ?)",
                    (nome, email, senha))

        con.commit()
        con.close()

        return redirect('/login')

    return render_template('cadastro.html')

# ---------------- INDEX (BUSCA + FILTRO) ----------------
@app.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect('/login')

    busca = request.args.get('busca', '')
    categoria = request.args.get('categoria', '')

    con = conectar()
    cur = con.cursor()

    query = "SELECT * FROM produto WHERE 1=1"
    params = []

    if busca:
        query += " AND nome LIKE ?"
        params.append(f"%{busca}%")

    if categoria:
        query += " AND categoria = ?"
        params.append(categoria)

    cur.execute(query, params)
    produtos = cur.fetchall()

    return render_template('index.html', produtos=produtos)

# ---------------- CRIAR PRODUTO ----------------
@app.route('/criar', methods=['GET', 'POST'])
def criar():
    if 'usuario_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        usuario_id = session['usuario_id']

        con = conectar()
        cur = con.cursor()

        cur.execute("""
        INSERT INTO produto (nome, descricao, categoria, status, usuario_id)
        VALUES (?, ?, ?, 'disponível', ?)
        """, (nome, descricao, categoria, usuario_id))

        con.commit()
        con.close()

        return redirect('/')

    return render_template('criar.html')

# ---------------- INTERESSE ----------------
@app.route('/interesse/<int:id>')
def interesse(id):
    if 'usuario_id' not in session:
        return redirect('/login')

    con = conectar()
    cur = con.cursor()

    cur.execute("UPDATE produto SET status = 'interessado' WHERE id = ?", (id,))

    con.commit()
    con.close()

    return redirect('/')

# ---------------- DELETAR ----------------
@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_id' not in session:
        return redirect('/login')

    con = conectar()
    cur = con.cursor()

    cur.execute("DELETE FROM produto WHERE id = ?", (id,))

    con.commit()
    con.close()

    return redirect('/')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# rodar
if __name__ == '__main__':
    app.run(debug=True)
