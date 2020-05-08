from requests import get, post, delete, put


print(put(f'http://localhost:5000/api/users/2', json={
            'surname': 'Алешин',
            'name': 'Андрей',
            'address': 'Москва, ул. Обручева, 13'
        }).json())
