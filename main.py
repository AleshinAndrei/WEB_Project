from data import db_session
from flask import Flask, render_template, redirect, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from flask_restful import Api
from data import products, product_resource, category_resource, categories


class SearchForm(FlaskForm):
    search = StringField('Картошка', validators=[DataRequired()])


db_session.global_init("db/food.sqlite")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)
api.add_resource(product_resource.ProductsListResource, '/api/products')
api.add_resource(product_resource.ProductResource, '/api/product/<int:product_id>')
api.add_resource(category_resource.CategoryResource, '/api/category/<int:category_id>')
api.add_resource(category_resource.CategoriesListResource, '/api/categories')


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def main():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search = search_form.search
        list_of_products = []
        for product in product_resource.ProductsListResource.get()['products'].json():
            if any(map(lambda key: search in product[key], ['description', 'name'])) or \
                    search in category_resource.CategoryResource.get(product['id']):
                list_of_products.append(product)

    return render_template('index.html', search_form=search_form)


if __name__ == '__main__':
    app.run(debug=True)
