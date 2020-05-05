from requests import get, post, delete


print(get('http://localhost:5000/api/baskets').json())
print(post('http://localhost:5000/api/baskets', json={
    'user_id': 1,
    'list_of_products': '1:1;2:1;3:2',
}).json())
print(post('http://localhost:5000/api/baskets', json={
    'user_id': 2,
    'list_of_products': '1:2;3:2',
}).json())
print(post('http://localhost:5000/api/baskets', json={
    'user_id': 1,
    'list_of_products': '1;2:3;',
}).json())
print(post('http://localhost:5000/api/baskets', json={
    'user_id': 1,
    'list_of_products': '4:5;',
}).json())
print(get('http://localhost:5000/api/baskets/999').json())
print(get('http://localhost:5000/api/baskets').json())
print(get('http://localhost:5000/api/baskets/1').json())
print(get('http://localhost:5000/api/baskets/2').json())
print(get('http://localhost:5000/api/baskets/3').json())
print(get('http://localhost:5000/api/baskets').json())
print(delete('http://localhost:5000/api/baskets/999').json())
print(delete('http://localhost:5000/api/baskets').json())
print(delete('http://localhost:5000/api/baskets/2').json())
print(get('http://localhost:5000/api/baskets').json())
