# test_main.py

from fastapi.testclient import TestClient

from app.homeworks.homework_7_1 import app

client = TestClient(app)


def test_response_with_422_error():
    reponse = client.post(
        url='/user',
        json={
            "usernamee": "string",
            "emaile": "user@example.com",
            "password": "string"
        }
    )

    assert reponse.status_code == 422
    assert reponse.json() == {
        "errors": [
            {
                "field": "username",
                "message": "Incorrect field name or syntax"
            },
            {
                "field": "email",
                "message": "Incorrect field name or syntax"
            }
        ]
    }


if __name__ == '__main__':
    test_response_with_422_error()
