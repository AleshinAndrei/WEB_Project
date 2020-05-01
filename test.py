from requests import get, post, delete


print(get('http://localhost:5000/api/users').json())
print(post('http://localhost:5000/api/users', json={
    'surname': 'Иванов',
    'name': 'Иван',
    'email': 'ivan@gmail.com',
    'address': 'Москва, ул. Тверская, 1',
    'password': '12345'
}).json())
print(post('http://localhost:5000/api/users', json={
    'surname': 'Сидоров',
    'name': 'Алексей',
    'email': 'ivan@gmail.com',
    'address': 'Москва, ул. Тверская, 2',
    'password': 'qwerty'
}).json())
print(post('http://localhost:5000/api/users', json={
    'surname': 'Романов',
    'name': 'Владимир',
    'email': 'vlad@gmail.com',
    'address': 'Москва, ул. Тверская, 3',
    'password': 'poiuy'
}).json())
print(get('http://localhost:5000/api/users/999').json())
print(get('http://localhost:5000/api/users').json())
print(get('http://localhost:5000/api/users/1').json())
print(get('http://localhost:5000/api/users/2').json())
print(get('http://localhost:5000/api/users/3').json())
print(get('http://localhost:5000/api/users').json())
print(delete('http://localhost:5000/api/users/999').json())
print(delete('http://localhost:5000/api/users').json())
print(delete('http://localhost:5000/api/users/2').json())
print(get('http://localhost:5000/api/users').json())
