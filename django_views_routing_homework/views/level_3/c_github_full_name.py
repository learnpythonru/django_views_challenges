"""
В этом задании вам нужно реализовать ручку, которая принимает на вход ник пользователя на Github,
а возвращает полное имя этого пользователя.

- имя пользователя вы узнаёте из урла
- используя АПИ Гитхаба, получите информацию об этом пользователе (это можно сделать тут: https://api.github.com/users/USERNAME)
- из ответа Гитхаба извлеките имя и верните его в теле ответа: `{"name": "Ilya Lebedev"}`
- если пользователя на Гитхабе нет, верните ответ с пустым телом и статусом 404
- если пользователь на Гитхабе есть, но имя у него не указано, верните None вместо имени
"""

import requests, json
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound


def fetch_name_from_github_view(request: HttpRequest, github_username: str) -> HttpResponse:
    # URL для запроса к API Github
    url = f"https://api.github.com/users/{github_username}"
    
    try:
        # Отправляем запрос к API Github
        response = requests.get(url)
        response.raise_for_status() # Проверяем статус ответа
    except requests.exceptions.HTTPError as e:
        # Если пользователя на Github нет, возвращаем 404
        if response.status_code == 404:
            return HttpResponseNotFound()
        else:
            return HttpResponse(str(e), status=500)
    
    # Извлекаем имя пользователя из ответа
    user_data = response.json()
    name = user_data.get('name')
    
    # Если имя пользователя не указано, возвращаем None
    if not name:
        return HttpResponse(json.dumps({"name": None}), content_type="application/json")
    
    # Возвращаем имя пользователя в теле ответа
    return HttpResponse(json.dumps({"name": name}), content_type="application/json")
