from fastapi import status

from .utils import *
from routers.users import get_db, get_current_user


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "user"
    assert response.json()['email'] == "user@user.com"
    assert response.json()['first_name'] == "user"
    assert response.json()['last_name'] == "user"
    assert response.json()['role'] == "admin"        
    assert response.json()['phone_number'] == '111111111' #keeping it an integer fails the test :)


def test_change_password_success(test_user):
    response = client.put("/user/change_password", json = {"password" : "user", "new_password" : "test123"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/change_password",json = {"password" : "wrong_password", "new_password" : "test123"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail' : "Error on password change"}

def test_change_phone_number_success(test_user):
    response = client.put("/user/add_phone_number/2222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT