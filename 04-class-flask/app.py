import os
from flask import Flask, render_template, request, session, redirect, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = "9yM5TWfSCoFFkuB8qSjbuNkRtwU3PZYp"


if not os.getenv("DB_URL"):
    raise RuntimeError("valimos, corran y llamen al ingeniero")

engine = create_engine(os.getenv("DB_URL"))
db = scoped_session(sessionmaker(bind=engine))


Session(app)

@app.route('/')
def index():
    rows = db.execute("SELECT * FROM annotations").fetchall()

    return render_template("index.html", rows=rows)

@app.route("/new-annotation", methods=["POST"])
def new_annotation():
    if not session.get("user_id"):
        flash("Debes iniciar sesión para agregar anotaciones")
        return redirect("/")
    user_id= session["user_id"]
    content = request.form.get('content')
    result = db.execute("""
        INSERT INTO annotations(id_user, content)
        VALUES(:id_user, :content)
    """, {
        "id_user": user_id,
        "content": content
    })
    db.commit()
    flash("Anotación agregada:D")
    return redirect("/")


@app.route('/admin')
def admin():

    rows = db.execute("SELECT * FROM users").fetchall()

    return render_template("admin.html", rows=rows)

@app.route("/users/<int:id_user>")
def user_detail(id_user):

    annotations = db.execute("SELECT * FROM annotations where id_user=:id_user",
    {"id_user": id_user}
    ).fetchall()

    user_detail = db.execute("SELECT username, email FROM users where id_user=:id_user",
    {"id_user": id_user}
    ).fetchone()

    return render_template("user_detail.html", annotations=annotations, user_detail=user_detail)



@app.route("/auth")
def auth():
    return render_template("auth.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/login", methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    result = db.execute("select * from users where username=:username", {"username": username}).fetchone()

    if not result:
        return render_template("auth.html", error= "Usuario no existe.", is_login=True)
    else:
        if check_password_hash(result[2], password):
            
            
            session["user_id"] = result[0]
            session["username"] = result[1]
        else:
            return render_template("auth.html", error= "contraseña incorrecta.", is_login=True)
    flash("Iniciando sesión :D")
    return render_template("index.html")


@app.route("/register", methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email  = request.form.get('email')
    
    validate = db.execute(""" 
        SELECT * FROM users WHERE username=:username OR email=:email
    """,{"username": username, "email": email}).rowcount
    if validate != 0:
        return render_template("auth.html", error="Usuario o correo ya en uso.")

    result = db.execute("""
        INSERT INTO users(username, pass, email)
        VALUES(:username, :password, :email) RETURNING id_user, username
    """, {
        "username": username,
        "password": generate_password_hash(password),
        "email": email
    }).fetchone()

    db.commit()
    session["user_id"] = result[0]
    session["username"] = result[1]
    flash("Se registró satisfactoriamente.")

    return redirect("/")