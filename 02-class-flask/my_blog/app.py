from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("INGRESEBASEDEDATOSAQUI")

db = scoped_session(sessionmaker(bind=engine))



app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        rows = db.execute("SELECT * FROM flask.post").fetchall()
        return render_template("index.html", rows=rows)

    else:
        autor = request.form.get('autor')
        titulo = request.form.get('titulo')
        contenido = request.form.get('contenido')

        db.execute(f"""
            INSERT INTO flask.post(autor, titulo, contenido)
            VALUES ('{autor}','{titulo}', '{contenido}')
        """)
        db.commit()
        return redirect("/")

