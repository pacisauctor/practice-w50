from flask import Flask, render_template, request

from cs50 import SQL

app = Flask(__name__)

db = SQL("sqlite:///ejemplo.db")

@app.route("/")
def index():
    q = request.args.get("q")
    # q=' or '1'='1
    registros = db.execute(f"SELECT * FROM Estudiante WHERE Nombre = '{q}'")
    print(registros)
    return render_template("index.html", filas=registros)