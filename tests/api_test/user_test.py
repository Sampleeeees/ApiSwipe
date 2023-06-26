from django.urls import reverse
import pytest
from user.models import User, Role

def create_user():
    user = User.objects.create(name='Test', surname='Test', role=Role.objects.create())
    return user

@pytest.mark.django_db
def test_list_user(client):
    response = client.get("/api/v1/user/", format='json')
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_user(client):
    response = client.post("/api/v1/user/", data={
                              "role": Role.objects.create(name_role='Role').id,
                              "password": "swipe1234",
                              "name": "Test",
                              "surname": "Test",
                              "phone_number": 214747,
                              "email": "test@test.com",
                              "switch_call_message": True,
                              "blacklist": True
                            }, format='json')
    assert response.status_code == 201

@pytest.mark.django_db
def test_retrieve_user(client):
    user = create_user()
    response = client.get("/api/v1/user/" + str(user.id) + "/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_patch_user(client):
    user = create_user()
    response = client.patch(f"/api/v1/user/{user.id}/", data={'name': 'New name'})
    assert response.status_code == 200
    assert response.data['name'] == 'New name'

@pytest.mark.django_db
def test_delete_user(client):
    user = create_user()
    response = client.delete(f"/api/v1/user/{user.id}/")
    assert response.status_code == 204

@pytest.mark.django_db
def test_block_user(client):
    user = create_user()
    response = client.post(f"/api/v1/user/{user.id}/user/block/", data={"blacklist": True})
    print(response, user)
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.blacklist == True

@pytest.mark.django_db
def test_unblock_user(client):
    user = create_user()
    user.blacklist = True
    user.save()
    response = client.post(f"/api/v1/user/{user.id}/user/unblock/", data={'blacklist': False})
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.blacklist == False

@pytest.mark.django_db
def test_profile_user(client):
    response = client.get("/api/v1/user/profile/")
    assert response.status_code == 200