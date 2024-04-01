from fastapi.testclient import TestClient

from app.homeworks import app_7_1

client = TestClient(app_7_1)


def test_calculate_sum():
    response = client.get('/sum/?a=5&b=10')
    assert response.status_code == 200
    assert response.json() == {'result': 15}

    response = client.get("/sum/?a=3")
    assert response.status_code == 422  # Unprocessable Entity (validation error)
    assert response.json() == {
        'detail': [
            {'input': None,
             'loc': ['query', 'b'],
             'msg': 'Field required',
             'type': 'missing',
             'url': 'https://errors.pydantic.dev/2.6/v/missing'
             }
        ]
    }
