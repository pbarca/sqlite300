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


@app.route('/', methods=['POST', 'GET'])
def index():
    erro = None
    if request.method == "POST":
        v1 = request.form['usr']
        v2 = request.form['pwd']
        v3 = request.form['cpwd']
        if v2 != v3:
            erro = 'A palavra passe não coincide.'
        else:
            alterar(v1, v2)
    return render_template('newpass.html', erro=erro)


if __name__ == '__main__':
    app.run(debug=True)
