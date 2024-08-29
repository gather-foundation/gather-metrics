import re

from fastapi.testclient import TestClient

from src.main import app  # Assuming 'app' is your FastAPI instance

client = TestClient(app)


def test_root_route():
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>Gather Metrics</title>" in response.text


def test_show_dob_route():
    response = client.get("/show-dob")
    assert response.status_code == 200
    assert '<input type="date"' in response.text


def test_show_age_route():
    response = client.get("/show-age")
    assert response.status_code == 200
    assert '<input type="number"' in response.text


def test_validate_age_route_valid_age():
    response = client.post("/validate-age", data={"age_value": 2, "age_unit": "years"})
    assert response.status_code == 200


def test_validate_age_route_age_high():
    response = client.post("/validate-age", data={"age_value": 22, "age_unit": "years"})
    assert response.status_code == 200
    assert "Ages over 21 years are accepted" in response.text


def test_validate_age_route_dob_future():
    response = client.post(
        "/validate-age", data={"age_value": "2100-01-01", "age_unit": "dob"}
    )
    assert response.status_code == 200
    assert "Date of birth cannot be in the future." in response.text


def test_hcirc_percentile_placeholder():
    """Test when hcirc_percentile is undefined or None."""
    response = client.get("/")
    assert response.status_code == 200
    assert '<span id="hcirc-percentile">_ _</span>' in response.text


def test_hcirc_percentile_less_than_one():
    """Test when hcirc_percentile is less than 1."""
    response = client.post(
        "/head-circumference",
        data={
            "age_unit": "years",
            "age_value": 2,
            "sex": "M",
            "hcirc_value": 25.0,  # Simulated value that would result in < 1 percentile
            "hcirc_unit": "cm",
        },
    )
    assert response.status_code == 200
    assert '<span id="hcirc-percentile">< 1</span>' in response.text


def test_hcirc_percentile_greater_than_ninety_nine():
    """Test when hcirc_percentile is greater than 99."""
    response = client.post(
        "/head-circumference",
        data={
            "age_unit": "years",
            "age_value": 2,
            "sex": "M",
            "hcirc_value": 75.0,  # Simulated value that would result in > 99 percentile
            "hcirc_unit": "cm",
        },
    )
    assert response.status_code == 200
    assert '<span id="hcirc-percentile">> 99</span>' in response.text


def test_hcirc_percentile_between_one_and_ninety_nine():
    """Test when hcirc_percentile is between 1 and 99."""
    response = client.post(
        "/head-circumference",
        data={
            "age_unit": "years",
            "age_value": 2,
            "sex": "M",
            "hcirc_value": 48.0,  # Simulated value that would result in a percentile between 1 and 99
            "hcirc_unit": "cm",
        },
    )
    assert response.status_code == 200
    # Use a regex to match any number between 1 and 99
    regex = re.compile(r'<span id="hcirc-percentile">([1-9][0-9]?(\.\d+)?)</span>')
    assert regex.search(response.text), "hcirc_percentile not between 1 and 99"


def test_display_result_invalid_data():
    response = client.post(
        "/head-circumference",
        data={
            "age_unit": "years",
            "age_value": "invalid",
            "sex": "M",
            "hcirc_value": 50.0,
            "hcirc_unit": "cm",
        },
    )
    assert response.status_code == 422  # Check for the error message in the HTML


# def test_calculate_percentile_api():
#     response = client.post(
#         "/api/v1/head-circumference",
#         json={
#             "age_unit": "years",
#             "age_value": 2,
#             "sex": "M",
#             "hcirc_value": 50.0,
#             "hcirc_unit": "cm",
#         },
#     )
#     assert response.status_code == 200
#     json_response = response.json()
#     assert "hcirc_percentile" in json_response
#     assert (
#         0 <= json_response["hcirc_percentile"] <= 100
#     )  # Ensure the percentile is valid


# def test_rate_limit():
#     for _ in range(101):  # Assuming the limit is 100 requests/minute
#         response = client.get("/")
#     assert response.status_code == 429  # Too many requests
