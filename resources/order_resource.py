from flask_restful import abort, Resource
from flask import jsonify
from data import db_session, orders, users, products
from . import order_argparser

Orders = orders.Orders
User = users.User
Products = products.Products


def abort_if_order_not_found(order_id):
    session = db_session.create_session()
    order = session.query(Orders).get(order_id)
    if not order:
        abort(404, message=f"order {order_id} not found")


class OrderResource(Resource):
    def get(self, order_id):
        abort_if_order_not_found(order_id)
        session = db_session.create_session()
        order = session.query(Orders).get(order_id)
        return jsonify({'order': order.to_dict()})

    def delete(self, order_id):
        abort_if_order_not_found(order_id)
        session = db_session.create_session()
        order = session.query(Orders).get(order_id)
        session.delete(order)
        session.commit()
        return jsonify({'success': 'OK'})


class OrdersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        return jsonify({'orders': [order.to_dict() for order in session.query(Orders).all()]})

    def post(self):
        args = order_argparser.parser.parse_args()
        session = db_session.create_session()
        if not session.query(User).filter(User.id == args['user_id']).first():
            abort(400, message=f"User not found")
        for product_count in args['list_of_products'].split(';'):
            try:
                product, count = product_count.split(':')
            except ValueError:
                abort(400, message=f"Incorrect syntax")
                return
            if not session.query(Products).filter(Products.id == product).first():
                abort(400, message=f"Product not found")
            elif not (count.isdecimal() and int(count) > 0):
                abort(400, message=f"Incorrect number of product")
        order = Orders(
            user_id=args['user_id'],
            list_of_products=args['list_of_products'],
            status=args['status']
        )
        try:
            session.add(order)
        except Exception:
            abort(400)
        session.commit()
        return jsonify({'success': 'OK'})
