import requests
import datetime
from collections import Counter
import time
import random
import matplotlib.pyplot as plt


client_id = 'ID приложения'
redirect_uri = 'https://oauth.vk.com/blank.html'
scope = 'users,offline'
avg_c=0
avg_a=0
# процесс аутентификации
auth_url = f'https://oauth.vk.com/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type=token'
print(f'Перейдите по ссылке и разрешите доступ: {auth_url}')
access_token = input('Введите полученный access_token: ')
access_token='ТОКЕН'
n=0 #количество прогонов

while n<3:
    print(n+1)
    print()

    n+=1
    a_count=0
    c_count=0
    # запрос информации о пользователях
    avg_ages=[]
    all_city=[]

    users_list = [] #список пользователей для получения данных
    real_city = [] # список реальных город для дальнейшей проверки
    real_age = [] # список реальных возрастов для проверки

    # выбираем случайные 80% пользователей из users_list
    num_users = len(users_list)
    num_to_select = int(num_users * 1)
    random_users = random.sample(users_list, num_to_select)
    random_user_indices = [i for i in range(num_users) if users_list[i] in random_users]

    
    for i in random_user_indices:
        user_id = users_list[i]
        fields = 'first_name, last_name, city'
        api_url = f'https://api.vk.com/method/users.get?user_ids={user_id}&fields={fields}&access_token={access_token}&v=5.131'
        if not user_id.isnumeric():  # если user_id не является числом, то значит это ScreenName
            api_url = f'https://api.vk.com/method/users.get?user_ids={user_id}&screen_name=1&fields={fields}&access_token={access_token}&v=5.131'
        response = requests.get(api_url).json()
        
        print(response["response"][0]['first_name'], response["response"][0]["last_name"])
        # Запрашиваем список друзей пользователя с городами
        api_url = f'https://api.vk.com/method/friends.get?user_id={response["response"][0]["id"]}&fields={fields}&access_token={access_token}&v=5.131'
        response = requests.get(api_url).json()

        friends_cities = [f['city']['title'] for f in response['response']['items'] if 'city' in f]

        # Выбираем наиболее часто встречающийся город
        most_common_city = Counter(friends_cities).most_common(1)[0][0]
        print(f'Город пользователя по списку друзей: ' + most_common_city)
        if most_common_city == real_city[i]:
            print(f'Значение most_common_city для пользователя {user_id} совпадает с real_city: {real_city[i]}')
            c_count+=1
        else:
            print(f'Значение most_common_city для пользователя {user_id} не совпадает с real_city: {real_city[i]}')
        all_city.append(most_common_city)
        ####возраст
        fields = 'bdate,education, universities, schools'
        api_url = f'https://api.vk.com/method/users.get?user_ids={user_id}&fields={fields}&access_token={access_token}&v=5.131'
        if not user_id.isnumeric():  # если user_id не является числом, то значит это ScreenName
            api_url = f'https://api.vk.com/method/users.get?user_ids={user_id}&screen_name=1&fields={fields}&access_token={access_token}&v=5.131'

        response = requests.get(api_url).json()
        
        # получение информации о школе и университете пользователя
        schools = response['response'][0]['schools'] if 'schools' in response['response'][0] else []
        universities = response['response'][0]['universities'] if 'universities' in response['response'][0] else []

        # получение списка друзей пользователя
        api_url = f'https://api.vk.com/method/friends.get?user_id={response["response"][0]["id"]}&fields={fields}&access_token={access_token}&v=5.131'
        response = requests.get(api_url).json()
        
        # отбор друзей с совпадающей школой и/или университетом
        friends = []
        for friend in response['response']['items']:
            if ('schools' in friend and any(school['id'] in [s['id'] for s in schools] for school in friend['schools'])) \
                or ('universities' in friend and any(university['id'] in [u['id'] for u in universities] for university in friend['universities'])):
                friends.append(friend)
        
        # вычисление возраста друзей
        ages = []
        for friend in friends:
            if 'bdate' in friend:
                bdate_parts = friend['bdate'].split('.')
                if len(bdate_parts) == 3:
                    bdate = datetime.datetime.strptime(friend['bdate'], '%d.%m.%Y')
                    age = (datetime.datetime.now() - bdate).days / 365
                    ages.append(age)
        
        # вычисление среднего возраста друзей
        if len(ages) > 0:
            avg_age = sum(ages) // len(ages)
            print(f'Средний возраст друзей с совпадающей школой и/или университетом: {avg_age}')
        else:
            print('Нет совпадений')
            time.sleep(5)
            
        if avg_age == real_age[i]:
            a_count+=1
            print(f'Значение avg_age для пользователя {user_id} совпадает: {real_age[i]}')
            print()
            time.sleep(5)

        else:
            print(f'Значение avg_age для пользователя {user_id} не совпадает: {real_age[i]}')
            print()
            time.sleep(3)
    v_c_count = c_count/len(random_user_indices)
    
    v_a_count = a_count/len(random_user_indices)
    avg_c += v_c_count
    avg_a+=v_a_count
    print('Вероятность при n для города ', v_c_count)
    print('Вероятность при n для возраста ', v_a_count)
    print()
avg_c_count=avg_c/n
avg_a_count=avg_a/n
print('Экспериментальная вероятность для города: ', avg_c_count)
print('Экспериментальная вероятность для возраста: ', avg_a_count)

