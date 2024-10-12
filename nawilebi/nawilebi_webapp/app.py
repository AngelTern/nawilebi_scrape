from flask import Flask, render_template, url_for, redirect, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length
from flask_bcrypt import Bcrypt
from sqlalchemy import or_
from datetime import timedelta
import os

app = Flask(__name__)
application = app
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12XklsD!?NmG1509@localhost:3306/nawilebi'  
app.config["SECRET_KEY"] = os.urandom(24) 
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)  
app.config['SESSION_COOKIE_SECURE'] = True  # Set to True in production with HTTPS
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
    is_admin = db.Column(db.Boolean, default=False)  # Added admin field

class CarPart(db.Model):
    __tablename__ = 'nawilebi'
    id = db.Column(db.Integer, primary_key=True)
    part_url = db.Column(db.String(1000))
    car_mark = db.Column(db.String(70))
    car_model = db.Column(db.String(150))
    part_full_name = db.Column(db.String(150))
    alternative_name_1 = db.Column(db.String(255), default=None)  # Added field
    alternative_name_2 = db.Column(db.String(255), default=None)  # Added field
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    price = db.Column(db.Integer)
    in_stock = db.Column(db.Boolean)
    website = db.Column(db.String(255))
    phone = db.Column(db.String(20))  # Added phone field

    def to_dict(self):
        return {
            'id': self.id,
            'part_url': self.part_url,
            'car_mark': self.car_mark,
            'car_model': self.car_model,
            'part_full_name': self.part_full_name,
            'alternative_name_1': self.alternative_name_1,
            'alternative_name_2': self.alternative_name_2,
            'start_year': self.start_year,
            'end_year': self.end_year,
            'price': self.price,
            'website': self.website,
            'phone': self.phone
        }

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "მომხმარებელი", "class": "form-control"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                             render_kw={"placeholder": "პაროლი", "class": "form-control"})
    remember = BooleanField('დაიმახსოვრე', render_kw={"class": "form-check-input"})
    submit = SubmitField("შესვლა", render_kw={"class": "btn btn-primary"})

class AddUserForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "მომხმარებელი", "class": "form-control"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                             render_kw={"placeholder": "პაროლი", "class": "form-control"})
    is_admin = BooleanField('ადმინისტრატორი', render_kw={"class": "form-check-input"})
    submit = SubmitField("დამატება", render_kw={"class": "btn btn-primary"})

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("dashboard"))
        else:
            flash('არასწორი მომხმარებლის სახელი ან პაროლი', 'danger')
    return render_template("login.html", form=form)

@app.route('/data', methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("table_main.html")

@app.route('/api/data')
@login_required
def data():
    query = CarPart.query

    # Filters
    car_mark = request.args.get('car_mark')
    car_model = request.args.get('car_model')
    part_full_name = request.args.get('part_full_name')
    year = request.args.get('year')

    if car_mark:
        query = query.filter(CarPart.car_mark.ilike(f"%{car_mark}%"))
    if car_model:
        query = query.filter(CarPart.car_model.ilike(f"%{car_model}%"))
    if part_full_name:
        query = query.filter(
            or_(
                CarPart.part_full_name.ilike(f'%{part_full_name}%'),
                CarPart.alternative_name_1.ilike(f'%{part_full_name}%'),
                CarPart.alternative_name_2.ilike(f'%{part_full_name}%')
            )
        )
    if year:
        try:
            search_year = int(year)
            query = query.filter(
                CarPart.start_year <= search_year,
                CarPart.end_year >= search_year
            )
        except ValueError:
            pass  # Handle invalid input if necessary

    total_filtered = query.count()

    # Sorting logic
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['part_url', 'car_mark', 'car_model', 'part_full_name', 'alternative_name_1', 'alternative_name_2', 'start_year', 'end_year', 'price', 'website', 'phone']:
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
    car_marks = car_marks_query.order_by(CarPart.car_mark.asc()).all()
    return jsonify([{"label": mark[0], "value": mark[0]} for mark in car_marks])

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
        query = query.filter(CarPart.part_full_name.ilike(f'%{search}%'))
    part_names = query.all()
    return jsonify([part_name[0] for part_name in part_names])

@app.route('/manage_users', methods=["GET", "POST"])
@login_required
def manage_users():
    if not current_user.is_admin:
        flash('წვდომა აკრძალულია. მხოლოდ ადმინისტრატორებს შეუძლიათ მომხმარებლების მართვა.', 'danger')
        return redirect(url_for('dashboard'))
    users = User.query.all()
    form = AddUserForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('მომხმარებლის სახელი უკვე არსებობს', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(username=form.username.data, password=hashed_password, is_admin=form.is_admin.data)
            db.session.add(new_user)
            db.session.commit()
            flash('მომხმარებელი წარმატებით დაემატა', 'success')
        return redirect(url_for('manage_users'))
    return render_template('manage_users.html', users=users, form=form)

@app.route('/delete_user/<int:user_id>', methods=["POST"])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('წვდომა აკრძალულია. მხოლოდ ადმინისტრატორებს შეუძლიათ მომხმარებლების წაშლა.', 'danger')
        return redirect(url_for('manage_users'))
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("საკუთარი ანგარიშის წაშლა შეუძლებელია.", 'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash('მომხმარებელი წარმატებით წაიშალა', 'success')
    return redirect(url_for('manage_users'))

def check_freeze_status():
    try:
        with open('control_file.txt', 'r') as file:
            freeze_value = file.read().strip()
            return freeze_value == '1'
    except FileNotFoundError:
        return False

@app.route('/toggle_freeze', methods=['POST'])
@login_required
def toggle_freeze():
    if not current_user.is_admin:
        return jsonify({'error': 'მხოლოდ ადმინისტრატორებს შეუძლიათ ამ ფუნქციის გამოყენება.'}), 403

    freeze_status = check_freeze_status()
    new_value = '0' if freeze_status else '1'

    try:
        with open('control_file.txt', 'w') as file:
            file.write(new_value)
        return jsonify({'status': 'success', 'freeze_status': new_value})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'შეცდომა მოხდა: {str(e)}'}), 500

    
    
@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
