import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.api.service import router

app = FastAPI()

app.include_router(router)

client = TestClient(app)


def test_main_page():
    response = client.get('/')
    assert response.status_code == 200

@pytest.mark.parametrize(
    'url_422, url_200_empty, url_200, query', [
        ('/type', '/type?primary_type=something', '/type?primary_type=HOMICIDE', 'primary_type'),
        ('/date', '/date?date=2034-10-28', '/date?date=2020-07-13', 'date'),
    ]
)
def test_types_and_dates(url_422, url_200_empty, url_200, query):
    response_422 = client.get(url_422)
    assert response_422.status_code == 422
    assert response_422.json() == {
    "detail": [
            {
                "loc": [
                    "query",
                    query
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }

    response_200_empty = client.get(url_200_empty)
    assert response_200_empty.status_code == 200
    assert response_200_empty.json() == []

    response_200 = client.get(url_200)
    assert response_200.status_code == 200
