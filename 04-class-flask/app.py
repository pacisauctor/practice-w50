import os
from flask import Flask, render_template, request, session, redirect
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
    return render_template("index.html")


@app.route('/admin')
def admin():

    rows = db.execute("SELECT * FROM users").fetchall()

    return render_template("admin.html", rows=rows)

@app.route("/users/<int:id_user>")
def user_detail(id_user):

    rows = db.execute("SELECT * FROM users where id_user=:id_user",
    {"id_user": id_user}
    ).fetchall()


    return render_template("admin.html", rows=rows)



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
        print("valimos")
    else:
        if check_password_hash(result[2], password):
            print("iniciando sesión...")
            
            session["user_id"] = result[0]
            session["username"] = result[1]
        else:
            print("contraseña incorrecta")

    return render_template("index.html")


@app.route("/register", methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email  = request.form.get('email')

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

    return redirect("/")