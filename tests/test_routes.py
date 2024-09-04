import pytest
from app import create_app
from config import Config


class TestConfig(Config):
    TESTING = True


@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        yield client


def test_valid_route_with_data(client):
    response = client.get(
        "/rates?date_from=2016-01-11&date_to=2016-01-20&origin=CNSGH&destination=north_europe_main"
    )
    assert response.status_code == 200
    data = response.json
    assert len(data) == 10
    assert all(item["day"] for item in data)
    assert all(item["average_price"] is not None for item in data)


def test_valid_route_without_data(client):
    response = client.get(
        "/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=GBLGP"
    )
    assert response.status_code == 200
    data = response.json
    assert len(data) == 10
    assert all(item["day"] for item in data)
    assert all(item["average_price"] is None for item in data)


def test_valid_region_to_port(client):
    response = client.get(
        "/rates?date_from=2016-01-01&date_to=2016-01-10&origin=china_east_main&destination=BEANR"
    )
    assert response.status_code == 200


def test_valid_region_to_region(client):
    response = client.get(
        "/rates?date_from=2016-01-01&date_to=2016-01-10&origin=china_south_main&destination=north_europe_main"
    )
    assert response.status_code == 200


def test_valid_port_to_port(client):
    response = client.get(
        "/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=NOTRD"
    )
    assert response.status_code == 200


def test_invalid_date_range(client):
    response = client.get(
        "/rates?date_from=2016-01-10&date_to=2016-01-01&origin=CNSGH&destination=NOTRD"
    )
    assert response.status_code == 400
    assert (
        "Invalid date range. The 'date_from' must be earlier than 'date_to'"
        in response.json["Error"]
    )


def test_invalid_date_format(client):
    response = client.get(
        "/rates?date_from=2016-13-01&date_to=2016-13-10&origin=CNSGH&destination=NOTRD"
    )
    assert response.status_code == 400
    assert "Invalid date format" in response.json["Error"]


def test_missing_parameters(client):
    response = client.get("/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH")
    assert response.status_code == 400
    assert (
        "Error: One or more required parameters (date_from, date_to, origin, destination) are missing."
        in response.json["Error"]
    )


def test_invalid_port_code(client):
    response = client.get(
        "/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=ZZZZZ"
    )
    assert response.status_code == 400
    assert "Invalid destination 'ZZZZZ'. Please provide a valid port code or region slug for the destination."


def test_invalid_region(client):
    response = client.get(
        "/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=china_east"
    )
    assert response.status_code == 400
    assert "Invalid destination 'china_east'. Please provide a valid port code or region slug for the destination."


def test_date_range_exceeds_limit(client):
    response = client.get(
        "/rates?date_from=2016-01-01&date_to=2017-01-02&origin=CNSGH&destination=NOTRD"
    )
    assert response.status_code == 400
    assert (
        "Date range exceeds the maximum allowed period of 365 days"
        in response.json["Error"]
    )


def test_future_dates(client):
    response = client.get(
        "/rates?date_from=2025-01-01&date_to=2025-01-10&origin=CNSGH&destination=NOTRD"
    )
    assert response.status_code == 200
    data = response.json
    assert len(data) == 10
    assert all(item["average_price"] is None for item in data)


def test_very_old_dates(client):
    response = client.get(
        "/rates?date_from=1900-01-01&date_to=1900-01-10&origin=CNSGH&destination=NOTRD"
    )
    assert response.status_code == 200
    data = response.json
    assert len(data) == 10
    assert all(item["average_price"] is None for item in data)
