"""
В этом задании вам нужно научиться генерировать текст заданной длинны и возвращать его в ответе в виде файла.

- ручка должна получать длину генерируемого текста из get-параметра length;
- дальше вы должны сгенерировать случайный текст заданной длины. Это можно сделать и руками
  и с помощью сторонних библиотек, например, faker или lorem;
- дальше вы должны вернуть этот текст, но не в ответе, а в виде файла;
- если параметр length не указан или слишком большой, верните пустой ответ со статусом 403

Вот пример ручки, которая возвращает csv-файл: https://docs.djangoproject.com/en/4.2/howto/outputting-csv/
С текстовым всё похоже.

Для проверки используйте браузер: когда ручка правильно работает, при попытке зайти на неё, браузер должен
скачивать сгенерированный файл.
"""

import string, random
from django.http import HttpResponse, HttpRequest


def generate_file_with_text_view(request: HttpRequest) -> HttpResponse:
    # Получаем длину текста из GET-параметра 'length'
    length = request.GET.get('length')
    
    # Проверяем, указан ли параметр 'length' и является ли он числом
    if not length or not length.isdigit():
        # Если параметр 'length' не указан или не является числом, возвращаем 403
        return HttpResponse('Bad Request', status=403)
    
    # Преобразуем длину текста в целое число
    length = int(length)
    
    # Проверяем, не слишком ли большой параметр 'length'
    if length > 10000: # Примерное ограничение, можно установить любое другое
        # Если длина слишком большая, возвращаем 403
        return HttpResponse('Bad Request', status=403)
    
    # Генерируем случайный текст заданной длины
    text = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    # Создаем HttpResponse с текстом в качестве содержимого
    response = HttpResponse(text, content_type='text/plain')
    
    # Устанавливаем заголовки для возвращения файла
    response['Content-Disposition'] = 'attachment; filename="generated_text.txt"'
    
    return response