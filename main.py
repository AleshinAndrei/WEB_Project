from data import db_session
from flask import Flask, render_template, redirect, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from flask_restful import Api
from data import products, categories, users
from resources import product_resource, category_resource, user_resource
from requests import get, post, delete


class SearchForm(FlaskForm):
    search = StringField('Поиск', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    email = EmailField('Login / email', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rep_password = PasswordField('Repeat password', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


db_session.global_init("db/food.sqlite")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
api.add_resource(product_resource.ProductsListResource, '/api/products')
api.add_resource(product_resource.ProductResource, '/api/products/<int:product_id>')
api.add_resource(category_resource.CategoryResource, '/api/categories/<int:category_id>')
api.add_resource(category_resource.CategoriesListResource, '/api/categories')
api.add_resource(user_resource.UsersListResource, '/api/users')
api.add_resource(user_resource.UserResource, '/api/users/<int:user_id>')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def main():
    search_form = SearchForm()
    return render_template('base.html', search_form=search_form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm()
    if search_form.is_submitted():
        search_text = search_form.search.data
        list_of_products = []
        for product in get('http://localhost:5000/api/products').json()['products']:
            if any(map(
                    lambda key: search_text in product[key], ['description', 'name', 'category']
            )):
                list_of_products.append(product)
        return render_template('catalog.html', list_of_products=list_of_products, search_form=search_form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    search_form = SearchForm()
    login_form = LoginForm()
    if login_form.validate_on_submit():
        session = db_session.create_session()
        for user in session.query(users.User).filter(users.User.email == login_form.email.data).all():
            if user.check_password(login_form.password.data):
                login_user(user, remember=login_form.remember_me.data)
                return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=login_form)
    return render_template('login.html', title='Авторизация', form=login_form, message='', search_form=search_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/register", methods=['GET', 'POST'])
def register():
    search_form = SearchForm()
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        if register_form.password.data != register_form.rep_password.data:
            return render_template('register.html', title='Регистрация',
                                   form=register_form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.email == register_form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=register_form,
                                   message="Такой пользователь уже есть")
        post('http://localhost:5000/api/users', json={
            'surname': register_form.surname.data,
            'name': register_form.name.data,
            'email': register_form.email.data,
            'address': register_form.address.data,
            'password': register_form.password.data
        })
        login_user(session.query(users.User).filter(users.User.email == register_form.email.data).first())
        return redirect('/')
    return render_template('register.html', title='Регистрация',
                           form=register_form, message='', search_form=search_form)


if __name__ == '__main__':
    app.run(debug=True)
