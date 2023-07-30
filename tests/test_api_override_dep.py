import pytest
from ..schemas import token
from fastapi import HTTPException

@pytest.mark.api
def test_create_user(client):
    response = client.post("/users", json={"name":"mec",
        "password":"password", "items":["nike", "jeans", "t-shirt"]})
    #print(response.json())
    # new_user = schemas.userOut(**response.json())
    assert response.status_code == 201
    assert response.json().get("name") == "mec"


@pytest.mark.api
def test_login_user(client, test_user):
    response = client.post("/login", data={
        "username": test_user['name'], "password":test_user['password']})
    Token = token(**response.json())
    assert response.status_code == 200


@pytest.mark.api
def test_incorrect_login(client, test_user):
    response = client.post("/login", data={
        "username": test_user['name']+"a", "password":test_user['password']})
    assert response.status_code == 403
