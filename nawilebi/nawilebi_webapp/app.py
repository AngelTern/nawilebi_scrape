from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
application = app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12XklsD!?NmG1509@localhost/nawilebi'
app.config["SECRET_KEY"] = 'whatever'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'login_credentials'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.String(80), nullable = False)

class CarPart(db.Model):
    __tablename__ = 'nawilebi'
    id = db.Column(db.Integer, primary_key=True)
    part_url = db.Column(db.String(1000))
    car_mark = db.Column(db.String(70))
    car_model = db.Column(db.String(150))
    part_full_name = db.Column(db.String(150))
    year = db.Column(db.String(10))
    price = db.Column(db.Integer)
    in_stock = db.Column(db.Boolean)
    website = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'part_url': self.part_url,
            'car_mark': self.car_mark,
            'car_model': self.car_model,
            'part_full_name': self.part_full_name,
            'year': self.year,
            'price': self.price,
            'in_stock': self.in_stock,
            'website': self.website
        }


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username", "class": "form-control"})
    
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password", "class": "form-control"})
    
    submit = SubmitField("Login", render_kw={"class": "btn btn-primary"})

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("dashboard"))
    return render_template("login.html", form = form)

@app.route('/data', methods = ["GET", "POST"])
@login_required
def dashboard():
    return render_template("table_main.html")

@app.route('/api/data')
@login_required
def data():
    query = CarPart.query
    
    #Apply filters from request
    car_mark = request.args.get('car_mark')
    car_model = request.args.get('car_model')
    part_full_name = request.args.get('part_full_name')
    year = request.args.get('year')
    in_stock = request.args.get('in_stock')
    website = request.args.get('website')

    if car_mark:
        query = query.filter(CarPart.car_mark == car_mark)
    if car_model:
        query = query.filter(CarPart.car_model == car_model)
    if part_full_name:
        query = query.filter(CarPart.part_full_name == part_full_name)
    if year:
        query = query.filter(CarPart.year == year)
    if in_stock is not None and in_stock != "":
        query = query.filter(CarPart.in_stock == (in_stock == "1"))
    if website:
        query = query.filter(CarPart.website == website)

    total_filtered = query.count()

    # Sorting logic
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['part_url', 'car_mark', 'car_model', 'part_full_name', 'year', 'price', 'in_stock', 'website']:
            col_name = 'part_full_name'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(CarPart, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # Pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # Response
    return {
        'data': [car_part.to_dict() for car_part in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': CarPart.query.count(),
        'draw': request.args.get('draw', type=int),
    }

@app.route('/api/filters/car_mark')
def filter_car_mark():
    car_marks = db.session.query(CarPart.car_mark).distinct().all()
    return [mark[0] for mark in car_marks]

@app.route('/api/filters/car_model')
def filter_car_model():
    car_mark = request.args.get('car_mark')
    query = db.session.query(CarPart.car_model).distinct()
    if car_mark:
        query = query.filter(CarPart.car_mark == car_mark)
    car_models = query.all()
    return [model[0] for model in car_models]

@app.route('/api/filters/part_full_name')
def filter_part_full_name():
    car_mark = request.args.get('car_mark')
    query = db.session.query(CarPart.part_full_name).distinct()
    if car_mark:
        query = query.filter(CarPart.car_mark == car_mark)
    part_names = query.all()
    return [part_name[0] for part_name in part_names]

@app.route('/api/filters/year')
def filter_year():
    car_mark = request.args.get('car_mark')
    query = db.session.query(CarPart.year).distinct()
    if car_mark:
        query = query.filter(CarPart.car_mark == car_mark)
    years = query.all()
    return [year[0] for year in years]

@app.route('/api/filters/in_stock')
def filter_in_stock():
    return [{"value": "1", "label": "Yes"}, {"value": "0", "label": "No"}]

@app.route('/api/filters/website')
def filter_website():
    websites = db.session.query(CarPart.website).distinct().all()
    return [website[0] for website in websites]

@app.route('/logout', methods = ["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)