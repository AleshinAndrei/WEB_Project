from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('surname')
parser.add_argument('name')
parser.add_argument('password')
parser.add_argument('address')
parser.add_argument('card_number')
parser.add_argument('cvv_code')