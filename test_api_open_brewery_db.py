import random
import requests
import pytest


BASE_URL = "https://api.openbrewerydb.org/v1/breweries"

@pytest.fixture()
def brewery_id():
    response = requests.get(BASE_URL)
    ids = [brewery['id'] for brewery in response.json()]
    return random.choice(ids)

def test_get_all_breweries_list():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert len(response.json()) > 0

@pytest.mark.parametrize("filter_by, value", [
    ("by_city", "san_diego"),
    ("by_dist", "38.8977,77.0365"),
    ("by_name", "cooper"),
    ("by_state", "ohio"),
    ("by_postal", "44107")
])
def test_filter_brewery_by(filter_by, value):
    params = {filter_by: value}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 200
    assert len(response.json()) > 0

@pytest.mark.parametrize("btype", ["large", "micro", "brewpub"])
def test_filter_by_type_of_brewery(btype):
    response = requests.get(f"{BASE_URL}?by_type={btype}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for brewery in data:
        assert brewery["brewery_type"] == btype

def test_get_brewery(brewery_id):
    response = requests.get(f"{BASE_URL}/{brewery_id}")
    assert response.status_code == 200
    assert response.json()["id"] == brewery_id

def test_search_brewery():
    response = requests.get(f"{BASE_URL}/search?query=dog")
    assert response.status_code == 200
    assert len(response.json()) > 0
