from requests import get, post, delete


print(get('http://localhost:5000/api/categories').json())
print(post('http://localhost:5000/api/categories', json={
    'name': 'Молочные продукты'
}).json())
print(post('http://localhost:5000/api/categories', json={
    'name': 'Овощи, фрукты, ягоды, зелень, грибы'
}).json())
print(post('http://localhost:5000/api/categories', json={
    'name': 'Мучные изделия'
}).json())
print(post('http://localhost:5000/api/categories', json={
    'name': 'Напитки'
}).json())
print(post('http://localhost:5000/api/categories', json={
    'name': 'Пустышка'
}).json())
print(get('http://localhost:5000/api/categories/999').json())
print(get('http://localhost:5000/api/categories').json())
print(get('http://localhost:5000/api/categories/1').json())
print(get('http://localhost:5000/api/categories/2').json())
print(get('http://localhost:5000/api/categories/3').json())
print(get('http://localhost:5000/api/categories/4').json())
print(get('http://localhost:5000/api/categories').json())
print(delete('http://localhost:5000/api/categories/999').json())
print(delete('http://localhost:5000/api/categories').json())
print(delete('http://localhost:5000/api/categories/5').json())
print(get('http://localhost:5000/api/categories').json())
