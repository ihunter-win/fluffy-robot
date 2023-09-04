import requests
import datetime
import time
import random
import matplotlib.pyplot as plt


def get_friends_avg_age(user_id):
    time.sleep(1)
    fields = 'bdate,education,universities,schools'
    api_url = f'https://api.vk.com/method/users.get?user_ids={user_id}&fields={fields}&access_token={access_token}&v=5.131'
    if not user_id.isnumeric(): 
        api_url = f'https://api.vk.com/method/users.get?user_ids={user_id}&screen_name=1&fields={fields}&access_token={access_token}&v=5.131'
    response = requests.get(api_url).json()
    schools = response['response'][0]['schools'] if 'schools' in response['response'][0] else []
    universities = response['response'][0]['universities'] if 'universities' in response['response'][0] else []
    api_url = f'https://api.vk.com/method/friends.get?user_id={response["response"][0]["id"]}&fields={fields}&access_token={access_token}&v=5.131'
    response = requests.get(api_url).json()
    friends_ages = []
    for friend in response['response']['items']:
        if ('schools' in friend and any(school['id'] in [s['id'] for s in schools] for school in friend['schools'])) \
            or ('universities' in friend and any(university['id'] in [u['id'] for u in universities] for university in friend['universities'])):
            if 'bdate' in friend:
                bdate_parts = friend['bdate'].split('.')
                if len(bdate_parts) == 3:
                    bdate = datetime.datetime.strptime(friend['bdate'], '%d.%m.%Y')
                    age = (datetime.datetime.now() - bdate).days / 365
                    friends_ages.append(age)
    if len(friends_ages) > 0:
        avg_age = sum(friends_ages) // len(friends_ages)
        return avg_age
    else:
        return None

def plot_age_distribution(predicted_ages, real_ages):
    diff = [predicted_ages[i] - real_ages[i] for i in range(len(predicted_ages)) if predicted_ages[i] is not None]
    hist = {}
    for d in diff:
        if d in hist:
            hist[d] += 1
        else:
            hist[d] = 1
    plt.bar(hist.keys(), hist.values(),)
    x_ticks = range(int(min(hist.keys())), int(max(hist.keys())) + 1, 2)
    plt.ylim(0, 20) 
    plt.yticks(range(0, max(hist.values()) + 1, 1))
    plt.xticks(x_ticks)
    plt.xlabel('Разница между возрастом')
    plt.ylabel('Количество совпадений')
    plt.show()



access_token='' #ТОКЕН
users_list = [] # список пользователей
real_age = [] # списко реальных возрастов для проверки
num_users = len(users_list)
num_to_select = int(num_users * 1)
random_users = random.sample(users_list, num_to_select)
random_user_indices = [i for i in range(num_users) if users_list[i] in random_users]

predicted_ages = [get_friends_avg_age(users_list[i]) for i in random_user_indices]
print(predicted_ages)

plot_age_distribution(predicted_ages, real_age)
