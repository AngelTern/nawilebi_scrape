from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_bcrypt import Bcrypt
from sqlalchemy import or_, func, Integer, case, and_

app = Flask(__name__)
application = app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:12XklsD!?NmG1509@localhost/nawilebi'
app.config["SECRET_KEY"] = 'am_chem_fexebs'
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
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class CarPart(db.Model):
    __tablename__ = 'nawilebi'
    id = db.Column(db.Integer, primary_key=True)
    part_url = db.Column(db.String(1000))
    car_mark = db.Column(db.String(70))
    car_model = db.Column(db.String(150))
    part_full_name = db.Column(db.String(150))
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
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
            'start_year': self.start_year,
            'end_year': self.end_year,
            'price': self.price,
            'in_stock': self.in_stock,
            'website': self.website
        }

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username", "class": "form-control"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password", "class": "form-control"})
    submit = SubmitField("Login", render_kw={"class": "btn btn-primary"})

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
    return render_template("login.html", form=form)

@app.route('/data', methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("table_main.html")

@app.route('/api/data')
@login_required
def data():
    query = CarPart.query

    # Apply filters from request
    car_mark = request.args.get('car_mark')
    car_model = request.args.get('car_model')
    part_full_name = request.args.get('part_full_name')
    year = request.args.get('year')
    in_stock = request.args.get('in_stock')
    price = request.args.get('price')

    if car_mark:
        query = query.filter(CarPart.car_mark == car_mark)
    if car_model:
        query = query.filter(CarPart.car_model == car_model)
    if part_full_name:
        query = query.filter(CarPart.part_full_name == part_full_name)
    if year:
        try:
            search_year = int(year)
            query = query.filter(
                CarPart.start_year <= search_year,
                CarPart.end_year >= search_year
            )
        except ValueError:
            pass  # Handle invalid input if necessary
    if in_stock is not None and in_stock != "":
        query = query.filter(CarPart.in_stock == (in_stock == "1"))
    if price:
        try:
            query = query.filter(CarPart.price == int(price))
        except ValueError:
            pass  # Handle invalid price input

    total_filtered = query.count()

    # Sorting logic
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['part_url', 'car_mark', 'car_model', 'part_full_name', 'start_year', 'end_year', 'price', 'in_stock']:
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
    start = request.args.get('start', type=int) or 0
    length = request.args.get('length', type=int) or 10
    query = query.offset(start).limit(length)

    # Response
    return jsonify({
        'data': [car_part.to_dict() for car_part in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': CarPart.query.count(),
        'draw': request.args.get('draw', type=int, default=1),
    })

@app.route('/api/filters/car_mark')
@login_required
def filter_car_mark():
    search = request.args.get('search', '')
    car_marks_query = db.session.query(CarPart.car_mark).distinct()
    if search:
        car_marks_query = car_marks_query.filter(CarPart.car_mark.like(f'%{search}%'))
    car_marks = car_marks_query.all()
    return jsonify([mark[0] for mark in car_marks])

@app.route('/api/filters/car_model')
@login_required
def filter_car_model():
    car_mark = request.args.get('car_mark')
    search = request.args.get('search', '')
    query = db.session.query(CarPart.car_model).distinct()
    if car_mark:
        query = query.filter(CarPart.car_mark == car_mark)
    if search:
        query = query.filter(CarPart.car_model.like(f'%{search}%'))
    car_models = query.all()
    return jsonify([model[0] for model in car_models])

@app.route('/api/filters/part_full_name')
@login_required
def filter_part_full_name():
    car_mark = request.args.get('car_mark')
    car_model = request.args.get('car_model')
    search = request.args.get('search', '')
    query = db.session.query(CarPart.part_full_name).distinct()
    if car_mark:
        query = query.filter(CarPart.car_mark == car_mark)
    if car_model:
        query = query.filter(CarPart.car_model == car_model)
    if search:
        query = query.filter(CarPart.part_full_name.like(f'%{search}%'))
    part_names = query.all()
    return jsonify([part_name[0] for part_name in part_names])

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
