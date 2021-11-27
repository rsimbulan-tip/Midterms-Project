from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.secret_key = "secretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Users(db.Model):
    __tablename__="Users"
    username = db.Column(db.String(50),primary_key=True)
    userpsw = db.Column(db.String(50))
    user_fname = db.Column(db.String(50))
    user_lname = db.Column(db.String(50))

    def __init__(self,username, userpsw, user_fname, user_lname):
        self.username = username
        self.userpsw = userpsw
        self.user_fname = user_fname
        self.user_lname = user_lname

@app.route('/', methods=["GET","POST"])
def login():
    global username, userpsw
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username= request.form['username']
        userpsw = request.form['userpsw']

        findUser = Users.query.filter_by(username=username, userpsw=userpsw).first()
        if findUser:
            session['name'] = username
            flash("Successfully Logged In")
            return redirect(url_for('index'))
        else: 
            flash("Invalid Credentials")
            return redirect('/')

    return render_template("login.html")

@app.route('/register', methods=["GET","POST"])
def register():
    global reguname, regpsw, fname, lname
    if request.method == "GET":
        return render_template("registration.html")

    if request.method == "POST":
        username = request.form['reguname']
        regpsw = request.form['regpsw']
        fname = request.form['fname']
        lname = request.form['lname']

        checkUser = Users.query.filter_by(username=username).first()
        if checkUser:
            return redirect('/register')
        else:
            new_user = Users(reguname, regpsw, fname, lname)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/register')

    return render_template("registration.html")

@app.route('/index')
def index():
    return render_template("index.html")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)