# test_main.py

import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from app.homeworks.homework_7_2 import app

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
        mock_fetch_todos.assert_called_once()  # Убеждаемся, что fetch_data_from_api был вызван один раз
        mock_data_values_to_upper.assert_called_once_with(mock_response)  # убеждаемся, что process_data был вызван с "mock response"
        self.assertEqual(response.status_code, 200)  # проверяем что status code равен 200
        self.assertEqual(response.json(), mock_processed_data)  # проверяем, что данные ответа соответствуют имитируемым обработанным данным
