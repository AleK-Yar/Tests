'''        Есть ресурс «http://worldtimeapi.org/api/timezone/Europe/Moscow», что сделать:
        a) написать скрипт, который выполняет запрос к данному ресурсу, получает ответ,
           результат ответа выводит на экран в сыром виде.
        b) вывести название временной зоны
        c) выводит дельту времени между точкой перед началом выполенения запроса и
           результатом из ответа ресурса о текущем времени с учетом часового пояса
        d) замеры из пункта c) повторить серией из пяти запросв и вывести среднюю дельту на основе данной серии '''


import requests
from datetime import datetime, timezone, time, timedelta

res = requests.get("http://worldtimeapi.org/api/timezone/Europe/Moscow")
date_times = []
number_of_requests = 5


def delta_time(request):  # дельта времени локального и ответа от сервера

    date_time_local = datetime.now(timezone.utc)  # + timedelta(hours=0, minutes=0, seconds=0)  # >>> для тестов
    date_time_serv = datetime.strptime(request.json()["utc_datetime"], '%Y-%m-%dT%H:%M:%S.%f%z')
    delta = date_time_local - date_time_serv

    return delta


def avg_time(date_times):  # вычисление среднего значения дельты

    for _ in range(number_of_requests):
        date_times.append(delta_time(res))

    total = 0
    for dt in date_times:
        total += dt.seconds + dt.microseconds / 1E6

    avg = total / len(date_times)
    minutes, seconds = divmod(int(avg), 60)
    hours, minutes = divmod(minutes, 60)
    microseconds = int(round(avg - int(avg), 6) * 1E6)

    return time(hours, minutes, seconds, microseconds)


dl = delta_time(res)
avgTime = avg_time(date_times)

print()
print(f'Ответ в сыром виде: {res.text}')
print()
print(f'Timezone: {res.json()["timezone"]}')
print()
print(f'Дельта времени локального и ответа сервера: {dl}')
print()
print(f'Средняя дельта времени за {number_of_requests} запросов:{avgTime}')
