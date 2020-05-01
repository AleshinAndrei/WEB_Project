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


class SearchForm(FlaskForm):
    search = StringField('Картошка', validators=[DataRequired()])


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


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def main():
    search_form = SearchForm()
    if search_form.is_submitted():
        search = search_form.search.data
        list_of_products = []
        for product in product_resource.ProductsListResource().get().json['products']:
            if any(map(
                    lambda key: search in product[key], ['description', 'name', 'category']
            )):
                list_of_products.append(product)
        return render_template('catalog.html', list_of_products=list_of_products, search_form=search_form)

    return render_template('index.html', search_form=search_form)


if __name__ == '__main__':
    app.run(debug=True)
