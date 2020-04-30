from flask_restful import abort, Resource
from flask import jsonify
from data import db_session, categories
from . import category_argparser

Categories = categories.Categories


def abort_if_category_not_found(category_id):
    session = db_session.create_session()
    category = session.query(Categories).get(category_id)
    if not category:
        abort(404, message=f"category {category_id} not found")


class CategoryResource(Resource):
    def get(self, category_id):
        abort_if_category_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Categories).get(category_id)
        return jsonify({'category': category.to_dict()})

    def delete(self, category_id):
        abort_if_category_not_found(category_id)
        session = db_session.create_session()
        category = session.query(Categories).get(category_id)
        session.delete(category)
        session.commit()
        return jsonify({'success': 'OK'})


class CategoriesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        categorys = session.query(Categories).all()
        return jsonify({'categories': [item.to_dict() for item in categorys]})

    def post(self):
        args = category_argparser.parser.parse_args()
        session = db_session.create_session()
        category = Categories(
            name=args['name']
        )
        try:
            session.add(category)
        except Exception as error:
            print(error)
        session.commit()
        return jsonify({'success': 'OK'})
