import requests
import time
from typing import List, Dict, Optional
from config import VK_CONFIG as vk


def get(url: str, params={}, timeout=5, max_retries=5, backoff_factor=0.3) -> Optional[requests.models.Response]:
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for i in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=(timeout, 3))
            return response
        except requests.exceptions.RequestException:
            if i == max_retries:
                raise
            delay = backoff_factor * 2 ** i
            time.sleep(delay)


def get_friends(user_id: int, fields="bdate") -> Dict:
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    query_params = {
        'access_token': vk['access_token'],
        'user_id': user_id,
        'fields': fields,
        'v': vk['version']
    }

    url = "https://api.vk.com/method/friends.get?"
    response = get(url, query_params)
    data = response.json()

    return data


def messages_get_history(user_id: int, offset: int = 0, count: int = 20) -> List:
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    query_params = {
        'access_token': vk['access_token'],
        'user_id': user_id,
        'offset': offset,
        'v': vk['version']
    }

    messages = []
    while count > 0:
        if count <= 200:
            query_params['count'] = count
        else:
            query_params['count'] = 200
        url = "https://api.vk.com/method/messages.getHistory?"
        response = get(url, query_params)
        data = response.json()
        fail = data.get('error')
        if fail:
            raise Exception(data['error']['error_msg'])
        messages.extend(data['response']['items'])
        count -= 200
        query_params['offset'] += 200
        time.sleep(1)
    return messages
