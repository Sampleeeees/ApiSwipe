import pytest
from house.models import *
from gallery.models import Gallery
from user.models import User, Role

def create_builder():
    builder = User.objects.create(
        name='Builder',
        surname='Builder',
        email='builder1@builder.com',
        role=Role.objects.create(is_builder=True, is_regular=False)
    )
    return builder

def create_house():
    builder = create_builder()
    gallery = Gallery.objects.create(text='New house')
    house = House.objects.create(
        name='House num.1',
        general_image='house/general_photo/general.jpg',
        address='Odessa',
        map_position='12551 1547 545',
        min_price=12000,
        price_for_m2=250,
        area=12200,
        sea_distance=2,
        builder= builder,
        gallery=gallery
    )
    return house

def create_section():
    house = create_house()
    section = Section.objects.create(name='Section 10', house=house)
    return section

def create_floor():
    house = create_house()
    floor = Floor.objects.create(name='Floor 1', house=house)
    return floor

def create_corps():
    house = create_house()
    corps = Corps.objects.create(name='Corps 1', house=house)
    return corps

@pytest.mark.django_db
def test_list_house(client):
    response = client.get("/api/v1/house/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_retrieve_house(client):
    house = create_house()
    response = client.get(f"/api/v1/house/{house.id}/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_house(client):
    house = create_house()
    response = client.delete(f"/api/v1/house/{house.id}/")
    assert response.status_code == 204

@pytest.mark.django_db
def test_list_section_house(client):
    section = create_section()
    response = client.get("/api/v1/section/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_section_house(builder):
    house = create_house()
    response = builder.post(f"/api/v1/section/", data={'name': 'New Section', 'house': house.id}, format='json')
    assert response.status_code == 201
    assert response.data['name'] == 'New Section'

@pytest.mark.django_db
def test_list_floor_house(client):
    floor = create_floor()
    response = client.get("/api/v1/floor/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_floor_house(builder):
    house = create_house()
    response = builder.post(f"/api/v1/floor/", data={'name': 'New Section', 'house': house.id}, format='json')
    assert response.status_code == 201
    assert response.data['name'] == 'New Section'

@pytest.mark.django_db
def test_list_floor_house(client):
    corps = create_corps()
    response = client.get("/api/v1/floor/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_floor_house(builder):
    house = create_house()
    response = builder.post(f"/api/v1/corps/", data={'name': 'New Section', 'house': house.id}, format='json')
    assert response.status_code == 201
    assert response.data['name'] == 'New Section'






