from flask_restful import abort, Resource
from flask import jsonify
from data import db_session, baskets, users, products
from . import basket_argparser

Baskets = baskets.Baskets
User = users.User
Products = products.Products


def abort_if_basket_not_found(basket_id):
    session = db_session.create_session()
    basket = session.query(Baskets).get(basket_id)
    if not basket:
        abort(404, message=f"Basket {basket_id} not found")


class BasketResource(Resource):
    def get(self, basket_id):
        abort_if_basket_not_found(basket_id)
        session = db_session.create_session()
        basket = session.query(Baskets).get(basket_id)
        return jsonify({'basket': basket.to_dict()})

    def delete(self, basket_id):
        abort_if_basket_not_found(basket_id)
        session = db_session.create_session()
        basket = session.query(Baskets).get(basket_id)
        session.delete(basket)
        session.commit()
        return jsonify({'success': 'OK'})


class BasketsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        return jsonify({'baskets': [basket.to_dict() for basket in session.query(Baskets).all()]})

    def post(self):
        args = basket_argparser.parser.parse_args()
        session = db_session.create_session()
        if not session.query(User).filter(User.id == args['user_id']).first():
            abort(400, message=f"User not found")
        for product_count in args['list_of_products'].split(';'):
            try:
                product, count = product_count.split(':')
            except ValueError:
                abort(400, message=f"Incorrect syntax")
            if not session.query(Products).filter(Products.id == product).first():
                abort(400, message=f"Product not found")
            elif not (count.isdecimal() and int(count) > 0):
                abort(400, message=f"Incorrect number of product")
        basket = Baskets(
            user_id=args['user_id'],
            list_of_products=args['list_of_products'],
        )
        try:
            session.add(basket)
        except Exception:
            abort(400)
        session.commit()
        return jsonify({'success': 'OK'})
