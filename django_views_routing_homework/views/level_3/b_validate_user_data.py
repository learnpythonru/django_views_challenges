"""
В этом задании вам нужно реализовать вьюху, которая валидирует данные о пользователе.

- получите json из тела запроса
- проверьте, что данные удовлетворяют нужным требованиям
- если удовлетворяют, то верните ответ со статусом 200 и телом `{"is_valid": true}`
- если нет, то верните ответ со статусом 200 и телом `{"is_valid": false}`
- если в теле запроса невалидный json, вернуть bad request

Условия, которым должны удовлетворять данные:
- есть поле full_name, в нём хранится строка от 5 до 256 символов
- есть поле email, в нём хранится строка, похожая на емейл
- есть поле registered_from, в нём одно из двух значений: website или mobile_app
- поле age необязательное: может быть, а может не быть. Если есть, то в нём хранится целое число
- других полей нет

Для тестирования рекомендую использовать Postman.
Когда будете писать код, не забывайте о читаемости, поддерживаемости и модульности.
"""

from django.http import HttpResponse, HttpRequest
import json
from django.http import HttpResponse, HttpResponseBadRequest
from django import forms

class UserForm(forms.Form):
    full_name = forms.CharField(min_length=5, max_length=256)
    email = forms.EmailField()
    registered_from = forms.ChoiceField(choices=[('website', 'website'), ('mobile_app', 'mobile_app')])
    age = forms.IntegerField(required=False)

def validate_user_data_view(request: HttpRequest) -> HttpResponse:
    try:
        # Получение JSON из тела запроса
        data = json.loads(request.body)
    except json.JSONDecodeError:
        # Возвращаем Bad Request, если JSON невалидный
        return HttpResponseBadRequest("Invalid JSON")

    # Создание формы с полученными данными
    form = UserForm(data)

    # Проверка валидности данных
    if form.is_valid():
        # Если данные валидны, возвращаем статус 200 и {"is_valid": true}
        return HttpResponse(json.dumps({"is_valid": True}), content_type="application/json")
    else:
        # Если данные невалидны, возвращаем статус 200 и {"is_valid": false}
        return HttpResponse(json.dumps({"is_valid": False}), content_type="application/json")

