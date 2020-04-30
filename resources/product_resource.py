from flask_restful import abort, Resource
from flask import jsonify
from data import db_session, products
import product_argparser

Products = products.Products


def abort_if_product_not_found(product_id):
    session = db_session.create_session()
    product = session.query(Products).get(product_id)
    if not product:
        abort(404, message=f"product {product_id} not found")


class ProductResource(Resource):
    def get(self, product_id):
        abort_if_product_not_found(product_id)
        session = db_session.create_session()
        product = session.query(Products).get(product_id)
        return jsonify({'product': product.to_dict()})

    def delete(self, product_id):
        abort_if_product_not_found(product_id)
        session = db_session.create_session()
        product = session.query(Products).get(product_id)
        session.delete(product)
        session.commit()
        return jsonify({'success': 'OK'})


class ProductsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        return jsonify({'products': [item.to_dict() for item in session.query(Products).all()]})

    def post(self):
        args = product_argparser.parser.parse_args()
        session = db_session.create_session()
        product = Products(
            name=args['name'],
            description=args['description'],
            price=args['price'],
            category=args['category']
        )
        if 'quantity_on_storage' in args:
            product.quantity_on_storage = args['quantity_on_storage']
        if 'image_source' in args:
            product.image_source = args['image_source']
        try:
            session.add(product)
        except Exception:
            abort(404)
        session.commit()
        return jsonify({'success': 'OK'})
