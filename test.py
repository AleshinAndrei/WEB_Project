from requests import get, post, delete


print(get('http://localhost:5000/api/products').json())
print(post('http://localhost:5000/api/products', json={
    'name': 'Молоко',
    'category': 1,
    'description': 'Обычное молоко',
    'price': 3230
}).json())
print(post('http://localhost:5000/api/products', json={
    'name': 'Банан',
    'category': 2,
    'description': 'Обычный банан',
    'price': 1299
}).json())
print(post('http://localhost:5000/api/products', json={
    'name': 'Булка',
    'category': 3,
    'description': 'Обычная булка)'
}).json())
print(get('http://localhost:5000/api/products/999').json())
print(get('http://localhost:5000/api/products').json())
print(get('http://localhost:5000/api/products/1').json())
print(get('http://localhost:5000/api/products/2').json())
print(get('http://localhost:5000/api/products/3').json())
print(get('http://localhost:5000/api/products').json())
print(delete('http://localhost:5000/api/products/999').json())
print(delete('http://localhost:5000/api/products').json())
print(delete('http://localhost:5000/api/products/3').json())
print(get('http://localhost:5000/api/products').json())
