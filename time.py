"""      Есть ресурс «http://worldtimeapi.org/api/timezone/Europe/Moscow», что сделать:
        a) написать скрипт, который выполняет запрос к данному ресурсу, получает ответ,
           результат ответа выводит на экран в сыром виде.
        b) вывести название временной зоны
        c) выводит дельту времени между точкой перед началом выполенения запроса и
           результатом из ответа ресурса о текущем времени с учетом часового пояса
        d) замеры из пункта c) повторить серией из пяти запросв и вывести среднюю дельту на основе данной серии """

import requests
import sys
import time
from datetime import datetime, timezone, time


def delta_time():  # дельта времени локального и ответа от сервера

    url = "http://worldtimeapi.org/api/timezone/Europe/Moscow"
    date_time_local = datetime.now(timezone.utc)
    res = requests.get(url)

    if not res:  # Если сервер не отвечает, проверяем 5 раз через 5 секунд
        for _ in range(5):
            time.sleep(5)
            res = requests.get(url)
            if res:
                break
        else:
            print('Ошибка при обращении к серверу, повторите позже!')
            sys.exit()

    date_time_serv = datetime.strptime(res.json()["utc_datetime"], '%Y-%m-%dT%H:%M:%S.%f%z')
    delta = date_time_serv - date_time_local

    return delta, res


def avg_time(num_of_res):  # вычисление среднего значения дельты

    date_times = []
    for _ in range(num_of_res):
        date_times.append(delta_time()[0])

    total = 0
    for dt in date_times:
        total += dt.seconds + dt.microseconds / 1E6

    avg = total / len(date_times)
    microseconds = int(round(avg - int(avg), 6) * 1E6)
    minutes, seconds = divmod(int(avg), 60)
    hours, minutes = divmod(minutes, 60)

    return time(hours, minutes, seconds, microseconds)


number_of_requests = 5
dl, rs = delta_time()

print()
print(f'Ответ в сыром виде: {rs.text} \n')
print(f'Timezone: {rs.json()["timezone"]} \n')
print(f'Дельта времени локального и ответа сервера: {dl} \n')
print(f'Средняя дельта времени за {number_of_requests} запросов:{avg_time(number_of_requests)}')
