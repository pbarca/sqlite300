from flask import Flask, render_template, request

app = Flask(__name__)


def gravar(v1, v2):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizador.db')
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS usr (usr text, pwd text)")
    db.execute("INSERT INTO usr VALUES ( ?, ?)", (v1, v2))
    ficheiro.commit()
    ficheiro.close()
    return


def alterar(v1, v2):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizador.db')
    db = ficheiro.cursor()
    db.execute("UPDATE usr SET pwd = ? WHERE usr = ?", (v2, v1))
    ficheiro.commit()
    ficheiro.close()
    return


def existe(v1):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizador.db')
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE usr = ?", (v1,))
    valor = db.fetchone()
    ficheiro.close()
    return valor


def log(v1, v2):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizador.db')
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE usr = ? and pwd = ?", (v1, v2,))
    valor = db.fetchone()
    ficheiro.close()
    return valor


@app.route('/newpass', methods=['POST', 'GET'])
def newpass():
    erro = None
    if request.method == "POST":
        v1 = request.form['usr']
        v2 = request.form['pwd']
        v3 = request.form['cpwd']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif v2 != v3:
            erro = 'A palavra passe não coincide.'
        else:
            alterar(v1, v2)
            erro = 'A palavra passe foi alterada.'
    return render_template('newpass.html', erro=erro)


@app.route('/registo', methods=['POST', 'GET'])
def registo():
    erro = None
    if request.method == "POST":
        v1 = request.form['usr']
        v2 = request.form['pwd']
        v3 = request.form['cpwd']
        if existe(v1):
            erro = 'O Utilizador já existe.'
        elif v2 != v3:
            erro = 'A palavra passe não coincide.'
        else:
            gravar(v1, v2)
            erro = 'Utilizador registado com Sucesso.'
    return render_template('registo.html', erro=erro)


@app.route('/', methods=['POST', 'GET'])
def login():
    erro = None
    if request.method == "POST":
        v1 = request.form['usr']
        v2 = request.form['pwd']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif not log(v1, v2):
            erro = 'A senha está incorreta.'
        else:
            erro = 'Bem-vindo.'
    return render_template('login.html', erro=erro)


if __name__ == '__main__':
    app.run(debug=True)
