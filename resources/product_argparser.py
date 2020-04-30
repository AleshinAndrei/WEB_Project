from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('description', required=True)
parser.add_argument('category', required=True)
parser.add_argument('price', required=True, type=int)
parser.add_argument('quantity_on_storage', type=int)
parser.add_argument('image_source')
