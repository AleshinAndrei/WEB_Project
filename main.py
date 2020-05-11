from data import db_session
from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from flask_restful import Api
from data import users
from resources import product_resource, category_resource, user_resource, basket_resource, order_resource
from requests import get, post, delete, put


class SearchForm(FlaskForm):
    search = StringField('Поиск', validators=[DataRequired()])


class EditForm(FlaskForm):
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


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
api.add_resource(basket_resource.BasketsListResource, '/api/baskets')
api.add_resource(basket_resource.BasketResource, '/api/baskets/<int:basket_id>')
api.add_resource(order_resource.OrderResource, '/api/order/<int:order_id>')
api.add_resource(order_resource.OrdersListResource, '/api/orders')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)


@login_required
@app.route('/orders', methods=['GET'])
def orders():
    search_form = SearchForm()
    all_orders = get('http://localhost:5000/api/orders').json()['orders']
    my_orders = []
    for order in all_orders:
        if order['user_id'] == current_user.id:
            my_orders.append(order)
    if my_orders:
        return render_template('order.html', orders=my_orders, search_form=search_form)
    else:
        return render_template('order.html', orders=my_orders, no_orders=True, search_form=search_form)



@login_required
@app.route('/basket', methods=['POST', 'GET'])
def look_basket():
    search_form = SearchForm()
    for basket in get('http://localhost:5000/api/baskets').json()['baskets']:
        if basket['user_id'] == current_user.id:
            user_basket = basket
            break
    else:
        return render_template('basket.html', list_of_products=[], search_form=search_form, no_basket=True)

    if request.method == "POST":
        post('http://localhost:5000/api/orders', json={
            'user_id': current_user.id,
            'list_of_products': user_basket['list_of_products'],
            'status': 'На обработке'
        })  # знаю, что тут нужно сделать foreigner key, но мне было лень его делать
        return redirect('/orders')

    all_products = get(f'http://localhost:5000/api/products').json()['products']
    list_of_products = []
    for pair in user_basket['list_of_products'].split(';'):
        product_id = int(pair.split(':')[0])
        quantity = int(pair.split(':')[1])
        product = list(filter(lambda x: x['id'] == product_id, all_products))[0]
        product['quantity'] = quantity
        list_of_products.append(product)
    return render_template('basket.html', list_of_products=list_of_products, search_form=search_form)


@login_required
@app.route('/edit', methods=['POST', 'GET'])
def edit_user():
    edit_form = EditForm()
    search_form = SearchForm()
    if edit_form.validate_on_submit():
        put(f'http://localhost:5000/api/users/{current_user.id}', json={
            'surname': edit_form.surname.data,
            'name': edit_form.name.data,
            'address': edit_form.address.data
        })
        return redirect('/profile')

    edit_form.name.data = current_user.name
    edit_form.surname.data = current_user.surname
    edit_form.address.data = current_user.address
    return render_template('edit.html', form=edit_form, search_form=search_form)


@login_required
@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        search_form = SearchForm()
        return render_template('profile.html', search_form=search_form)
    return redirect('/')


@login_required
@app.route('/in_basket', methods=['POST', 'GET'])
def in_basket():
    data = request.args.to_dict()
    products_in_basket = dict()
    user_basket = {
            'user_id': current_user.id,
            'list_of_products': []
    }

    for basket in get('http://localhost:5000/api/baskets').json()['baskets']:
        if basket['user_id'] == current_user.id:
            delete(f'http://localhost:5000/api/baskets/{basket["id"]}')
            for pair in basket['list_of_products'].split(';'):
                product_id = pair.split(':')[0]
                quantity = pair.split(':')[1]
                if product_id in data and int(data[product_id]) != 0:
                    products_in_basket[product_id] = data[product_id]
                else:
                    products_in_basket[product_id] = quantity

    for product_id, quantity in data.items():
        if product_id not in products_in_basket and int(quantity) != 0:
            products_in_basket[product_id] = quantity
    user_basket['list_of_products'] = ';'.join(
        map(lambda pair: f"{pair[0]}:{pair[1]}", products_in_basket.items())
    )
    post('http://localhost:5000/api/baskets', json=user_basket)
    return redirect('/basket')


@app.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm()
    if search_form.is_submitted():
        search_text = search_form.search.data
        list_of_products = []
        bought_products = dict()
        if current_user.is_authenticated:
            for basket in get('http://localhost:5000/api/baskets').json()['baskets']:
                if basket['user_id'] == current_user.id:
                    for pair in basket['list_of_products'].split(';'):
                        bought_products[int(pair.split(':')[0])] = int(pair.split(':')[1])
                    break
        for product in get('http://localhost:5000/api/products').json()['products']:
            if any(map(
                    lambda key: search_text in product[key].lower(), ['description', 'name', 'category']
            )):

                if len(product['description']) > 30:
                    product['description'] = product['description'][:30] + '...'
                if product['id'] in bought_products:
                    product['bought'] = bought_products[product['id']]
                else:
                    product['bought'] = 0

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
                               form=login_form, search_form=search_form)
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


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def main():
    search_form = SearchForm()
    return render_template('index.html', search_form=search_form)


if __name__ == '__main__':
    app.run(debug=True)
