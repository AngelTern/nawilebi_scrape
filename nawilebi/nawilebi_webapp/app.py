from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12XklsD!?NmG1509@localhost/nawilebi'
app.config["SECRET_KEY"] = 'whatever'
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = 'login_credentials'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False)
    password = db.Column(db.String(80), nullable = False)



@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template("login.html")




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)