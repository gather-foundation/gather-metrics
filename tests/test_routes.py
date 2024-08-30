import re

import pytest
from fastapi.testclient import TestClient

from src.main import app  # Assuming 'app' is your FastAPI instance


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def valid_age_data():
    return {"age_value": 2, "age_unit": "years"}


@pytest.fixture
def high_age_data():
    return {"age_value": 22, "age_unit": "years"}


@pytest.fixture
def future_dob_data():
    return {"age_value": "2100-01-01", "age_unit": "dob"}


@pytest.fixture
def no_age_data():
    return {"age_value": None, "age_unit": "years"}


@pytest.fixture
def low_hcirc_data():
    return {
        "age_unit": "years",
        "age_value": 2,
        "sex": "M",
        "hcirc_value": 25.0,  # Simulated value that would result in < 1 percentile
        "hcirc_unit": "cm",
    }


@pytest.fixture
def high_hcirc_data():
    return {
        "age_unit": "years",
        "age_value": 2,
        "sex": "M",
        "hcirc_value": 75.0,  # Simulated value that would result in > 99 percentile
        "hcirc_unit": "cm",
    }


@pytest.fixture
def mid_hcirc_data():
    return {
        "age_unit": "years",
        "age_value": 2,
        "sex": "M",
        "hcirc_value": 48.0,  # Simulated value that would result in a percentile between 1 and 99
        "hcirc_unit": "cm",
    }


@pytest.fixture
def invalid_data():
    return {
        "age_unit": "years",
        "age_value": "invalid",
        "sex": "M",
        "hcirc_value": 50.0,
        "hcirc_unit": "cm",
    }


@pytest.fixture
def patch_dependencies(monkeypatch):
    # Mock the function that causes the error
    def mock_is_valid_age(*args, **kwargs):
        raise ValueError("Simulated exception")

    def mock_calculate_hcirc_percentile(*args, **kwargs):
        raise RuntimeError("Simulated exception")

    # Ensure the correct import path
    monkeypatch.setattr("src.routes.is_valid_age", mock_is_valid_age)
    monkeypatch.setattr(
        "src.routes.calculate_hcirc_percentile", mock_calculate_hcirc_percentile
    )


def test_root_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>Gather Metrics</title>" in response.text


def test_show_dob_route(client):
    response = client.get("/show-dob")
    assert response.status_code == 200
    assert '<input type="date"' in response.text


def test_show_age_route(client):
    response = client.get("/show-age")
    assert response.status_code == 200
    assert '<input type="number"' in response.text


def test_validate_age_route_valid_age(client, valid_age_data):
    response = client.post("/validate-age", data=valid_age_data)
    assert response.status_code == 200


def test_validate_age_route_age_high(client, high_age_data):
    response = client.post("/validate-age", data=high_age_data)
    assert response.status_code == 200
    assert "Ages over 21 years are accepted" in response.text


def test_validate_age_route_dob_future(client, future_dob_data):
    response = client.post("/validate-age", data=future_dob_data)
    assert response.status_code == 200
    assert "Date of birth cannot be in the future." in response.text


def test_validate_age_route_no_age(client, no_age_data):
    response = client.post("/validate-age", data=no_age_data)
    assert response.status_code == 200


def test_validate_age_route_generic_error(client, patch_dependencies):
    response = client.post("/validate-age", data={"age_value": 10, "age_unit": "years"})
    assert response.status_code == 500
    assert "Something went wrong." in response.text


def test_hcirc_percentile_placeholder(client):
    response = client.get("/")
    assert response.status_code == 200
    assert '<span id="hcirc-percentile">_ _</span>' in response.text


def test_hcirc_percentile_less_than_one(client, low_hcirc_data):
    response = client.post("/head-circumference", data=low_hcirc_data)
    assert response.status_code == 200
    assert '<span id="hcirc-percentile">< 1</span>' in response.text


def test_hcirc_percentile_greater_than_ninety_nine(client, high_hcirc_data):
    response = client.post("/head-circumference", data=high_hcirc_data)
    assert response.status_code == 200
    assert '<span id="hcirc-percentile">> 99</span>' in response.text


def test_hcirc_percentile_between_one_and_ninety_nine(client, mid_hcirc_data):
    response = client.post("/head-circumference", data=mid_hcirc_data)
    assert response.status_code == 200
    # Use a regex to match any number between 1 and 99
    regex = re.compile(r'<span id="hcirc-percentile">([1-9][0-9]?(\.\d+)?)</span>')
    assert regex.search(response.text), "hcirc_percentile not between 1 and 99"


def test_display_result_invalid_data(client, invalid_data):
    response = client.post("/head-circumference", data=invalid_data)
    assert response.status_code == 422  # Check for the error message in the HTML


def test_display_result_generic_error(client, mid_hcirc_data, patch_dependencies):
    response = client.post("/head-circumference", data=mid_hcirc_data)
    print(response)
    assert response.status_code == 500
    assert "Something went wrong." in response.text


def test_calculate_percentile_api_valid(client, valid_age_data):
    response = client.post(
        "/api/v1/head-circumference",
        json={
            "age_unit": valid_age_data["age_unit"],
            "age_value": valid_age_data["age_value"],
            "sex": "M",
            "hcirc_value": 50.0,
            "hcirc_unit": "cm",
        },
    )
    assert response.status_code == 200
    json_response = response.json()
    assert "hcirc_percentile" in json_response
    assert (
        0 <= json_response["hcirc_percentile"] <= 100
    )  # Percentile should be within a valid range


def test_calculate_percentile_api_low_hcirc(client, low_hcirc_data):
    response = client.post("/api/v1/head-circumference", json=low_hcirc_data)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["hcirc_percentile"] < 1  # Expecting a percentile less than 1


def test_calculate_percentile_api_high_hcirc(client, high_hcirc_data):
    response = client.post("/api/v1/head-circumference", json=high_hcirc_data)
    assert response.status_code == 200
    json_response = response.json()
    assert (
        json_response["hcirc_percentile"] > 99
    )  # Expecting a percentile greater than 99


def test_calculate_percentile_api_mid_hcirc(client, mid_hcirc_data):
    response = client.post("/api/v1/head-circumference", json=mid_hcirc_data)
    assert response.status_code == 200
    json_response = response.json()
    assert (
        1 <= json_response["hcirc_percentile"] <= 99
    )  # Expecting a percentile between 1 and 99


def test_calculate_percentile_api_invalid_data(client, invalid_data):
    response = client.post("/api/v1/head-circumference", json=invalid_data)
    assert response.status_code == 422  # Expecting a validation error


# def test_rate_limit():
#     for _ in range(101):  # Assuming the limit is 100 requests/minute
#         response = client.get("/")
#     assert response.status_code == 429  # Too many requests
