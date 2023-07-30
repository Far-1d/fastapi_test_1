from ..fast4 import app
from fastapi.testclient import TestClient
import pytest
# from .. import schemas
client = TestClient(app)

@pytest.mark.api
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message" : "hello user"}


@pytest.mark.api
def test_create_user():
    response = client.post("/users", json={"name":"mec",
        "password":"password", "items":["nike", "jeans", "t-shirt"]})
    #print(response.json())
    # new_user = schemas.userOut(**response.json())
    assert response.status_code == 201
    assert response.json().get("name") == "mec"
