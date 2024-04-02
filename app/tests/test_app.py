from fastapi.testclient import TestClient

from app.homeworks.homework_7_1 import app as app_7_1

client = TestClient(app_7_1)


class TestMain:
    #
    # @staticmethod
    # def test_correct_reg_user():
    #     response = client.post(
    #         url='/user',
    #         json={
    #             "username": "1",
    #             "email": "1@example.com",
    #             "password": "string"
    #         }
    #     )
    #     assert response.status_code == 200
    #     assert response.json() == {
    #         "username": "1",
    #         "email": "1@example.com",
    #         "id": 2
    #     }
    #
    # @staticmethod
    # def test_incorrect_reg_user():
    #     response = client.post(
    #         url='/user',
    #         json={
    #             "username": "1",
    #             "email": "1@example.com",
    #             "password": "string"
    #         }
    #     )
    #     assert response.status_code == 409
    #     assert response.json() == {
    #         "errors": [
    #             "NOT UNIQUE USERNAME OR EMAIL"
    #         ]
    #     }

    @staticmethod
    def test_correct_me():
        response = client.post(
            url='/user',
            json={
                "username": "1",
                "email": "1@example.com",
                "password": "string"
            }
        )
        assert response.status_code == 200
        assert response.json() ==  {'username': '1', 'email': '1@example.com', 'id': 1}
        #

        response = client.get(url='/user/1')
        assert response.status_code == 200
        assert response.json() == {
            "username": "1",
            "email": "1@example.com",
            "id": 1
        }

    @staticmethod
    def test_incorrect_me():
        response = client.get(url='/user/100500')

        assert response.status_code == 404
        assert response.json() == {
            "detail": "User not found"
        }

    @staticmethod
    def test_correct_delete():
        response = client.delete(url='/user/1')

        assert response.status_code == 200
        assert response.text.strip('"') == "Deleted user with id 1 succesfully"

    @staticmethod
    def test_incorrect_delete():
        response = client.delete(url='/user/100500')

        assert response.status_code == 404
        assert response.json() == {
            "detail": "User not found"
        }

    @staticmethod
    def test_get_all_users():
        response = client.get(url='/users')

        assert response.status_code == 200
        assert response.json() == {}
