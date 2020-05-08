from flask_restful import abort, Resource
from flask import jsonify
from data import db_session, users
from . import user_argparser, user_edit_argparser
User = users.User


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict()})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        try:
            session.delete(user)
            session.commit()
            return jsonify({'success': 'OK'})
        except Exception:
            return abort(500)

    def put(self, user_id):
        session = db_session.create_session()
        args = user_edit_argparser.parser.parse_args()
        user = session.query(User).get(user_id)
        if 'user' in args:
            user.name = args['name']
        if 'surname' in args:
            user.surname = args['surname']
        if 'address' in args:
            user.address = args['address']
        if 'card_number' in args:
            user.card_number = args['card_number']
        if 'password' in args:
            user.set_password(args['password'])
        if 'cvv_code' in args:
            user.set_cvv_code(args['cvv_code'])
        try:
            session.commit()
            return jsonify({'success': 'OK'})
        except Exception:
            return abort(500)


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict() for item in users]})

    def post(self):
        args = user_argparser.parser.parse_args()
        session = db_session.create_session()
        if session.query(User).filter(User.email == args['email']).first():
            return abort(400, message=f"This email already exist")
        user = User(
            surname=args['surname'],
            name=args['name'],
            email=args['email'],
            address=args['address']
        )
        if 'card_number' in args and 'hashed_cvv_code' in args:
            user.card_number = args['card_number']
            user.hashed_cvv_code = args['hashed_cvv_code']
        user.set_password(args['password'])
        session.add(user)
        try:
            session.add(user)
            session.commit()
            return jsonify({'success': 'OK'})
        except Exception:
            return abort(500)
