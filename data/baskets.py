import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


class Baskets(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'baskets'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), unique=True)
    list_of_products = sqlalchemy.Column(sqlalchemy.String)
