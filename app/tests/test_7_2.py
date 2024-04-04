# test_main.py
import pytest
import responses
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.homeworks.homework_7_2 import app, SomeResourceClient

client = TestClient(app)


class TestMain(unittest.TestCase):

    @patch("app.homeworks.homework_7_2.data_values_to_upper")
    @patch("app.homeworks.homework_7_2.fetch_todos")
    def test_get_and_process_data(self, mock_fetch_todos, mock_data_values_to_upper):
        # Имитируем функцию mock_fetch_todos, чтобы вернуть пример ответа
        mock_response = {"key": "value"}
        mock_fetch_todos.return_value = mock_response

        # имитируем функцию mock_data_values_to_upper
        mock_processed_data = {"key": "VALUE"}
        mock_data_values_to_upper.return_value = mock_processed_data

        # отправляем запрос на конечную точку /todos
        response = client.get("/todos")

        # наши assertions
        mock_fetch_todos.assert_called_once()  # Убеждаемся, что fetch_todos была вызвана один раз
        mock_data_values_to_upper.assert_called_once_with(
            mock_response)  # убеждаемся, что data_values_to_upper была вызвана с "mock response"
        self.assertEqual(response.status_code, 200)  # проверяем что status code равен 200
        self.assertEqual(response.json(),
                         mock_processed_data)  # проверяем, что данные ответа соответствуют имитируемым обработанным данным


@responses.activate  # мокаем ответ
def test_some_web_client():
    valid_resp = {
        "userId": 1,
        "id": 1,
        "title": "1",
        "body": "1"
    }
    # responses Блокирует все запросы происходящие из теста во внешние сервисы: connection refused by responses
    responses.add(
        method=responses.GET,
        url='https://jsonplaceholder.typicode.com/posts/1',
        json=valid_resp,
        status=200
    )

    some_resource_client = SomeResourceClient(
        'https://jsonplaceholder.typicode.com/posts/1')  # попробовать изменить url на некорректный
    res = some_resource_client.get_url_data()
    res_status = some_resource_client.get_url_status_code()

    assert res_status == 200
    assert res == valid_resp


@responses.activate
def test_some_web_client_with_404():
    ivalid_resp = {}

    responses.add(
        method=responses.GET,
        url='https://jsonplaceholder.typicode.com/posts/101',
        json=ivalid_resp,
        status=404
    )

    some_resource_client = SomeResourceClient('https://jsonplaceholder.typicode.com/posts/101')
    res_status = some_resource_client.get_url_status_code()
    res_data = some_resource_client.get_url_data()

    assert res_status == 404
    assert res_data == 'URL status code is invalid'


if __name__ == '__main__':
    TestMain()
    test_some_web_client()
