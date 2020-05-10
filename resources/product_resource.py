from flask_restful import abort, Resource
from flask import jsonify
from data import db_session, products
from . import product_argparser
from . import category_resource

CategoryResource = category_resource.CategoryResource

Products = products.Products


def abort_if_product_not_found(product_id):
    session = db_session.create_session()
    product = session.query(Products).get(product_id)
    if not product:
        abort(404, message=f"Product {product_id} not found")


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
        res = []
        for product in session.query(Products).all():
            item = product.to_dict()
            item['category'] = category_resource.CategoryResource().get(item['category']).json['category']['name']
            res.append(item)

        return jsonify({'products': res})

    def post(self):
        args = product_argparser.parser.parse_args()
        session = db_session.create_session()
        product = Products(
            name=args['name'],
            description=args['description'],
            price=args['price'],
            category=args['category']
        )
        if args['quantity_on_storage'] is not None:
            product.quantity_on_storage = args['quantity_on_storage']
        if args['image_source'] is not None:
            product.image_source = args['image_source']
        try:
            session.add(product)
        except Exception:
            abort(400)
        session.commit()
        return jsonify({'success': 'OK'})
