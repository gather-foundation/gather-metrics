from unittest.mock import patch

import numpy as np
import pytest

from src.models import Patient, Sex

############# PATIENT ###############


@pytest.fixture
def mock_load_csv_data():
    """Fixture to provide mocked CSV data."""
    return {
        "Age": np.array([0, 10, 20, 30, 40]),
        "25": np.array([30.0, 32.0, 34.0, 36.0, 38.0]),
        "75": np.array([50.0, 52.0, 54.0, 56.0, 58.0]),
    }


@pytest.fixture
def mock_norm_from_percentiles():
    """Fixture to provide mocked norm_from_percentiles results."""
    return (35.0, 10.0)  # loc=35.0, scale=10.0


@pytest.fixture
def male_patient():
    return Patient(age=30, sex=Sex.M, hcirc={"value_cm": 55.0})


@pytest.fixture
def female_patient():
    return Patient(age=25, sex=Sex.F, hcirc={"value_cm": 50.0})


@pytest.fixture
def invalid_patient_age():
    # Example of a patient with invalid data for edge case testing
    return {"age": -1, "sex": "F", "hcirc": {"value_cm": 5.0}}


@pytest.fixture
def invalid_patient_sex():
    # Example of a patient with invalid hcirc unit
    return {"age": 1, "sex": "X", "hcirc": {"value_in": 5.0}}


@pytest.fixture
def invalid_patient_hcirc():
    # Example of a patient with invalid hcirc unit
    return {"age": 1, "sex": "M", "hcirc": {"value_in": 5.0}}


@pytest.fixture
def patch_dependencies(monkeypatch, mock_load_csv_data):
    """Fixture to patch load_csv and norm_from_percentiles."""
    monkeypatch.setattr("src.utils.csv_loader.load_csv", lambda x: mock_load_csv_data)
    monkeypatch.setattr(
        "src.utils.hcirc_utils.norm_from_percentiles", lambda *args: (35.0, 10.0)
    )  # Assuming loc=35, scale=10


def test_valid_male_patient(male_patient):
    assert male_patient.age == 30
    assert male_patient.sex == Sex.M
    assert male_patient.hcirc["value_cm"] == 55.0


def test_valid_female_patient(female_patient):
    assert female_patient.age == 25
    assert female_patient.sex == Sex.F
    assert female_patient.hcirc["value_cm"] == 50.0


def test_invalid_patient_data(invalid_patient_age):
    with pytest.raises(ValueError):
        Patient(**invalid_patient_age)


def test_invalid_patient_sex(invalid_patient_sex):
    with pytest.raises(ValueError):
        Patient(**invalid_patient_sex)


def test_invalid_patient_hcirc(invalid_patient_hcirc):
    with pytest.raises(ValueError):
        Patient(**invalid_patient_hcirc)


def test_low_value_returns_zero(patch_dependencies):
    """Test that a very low head circumference returns a percentile close to 0."""
    patient = Patient(
        age=25, sex=Sex.M, hcirc={"value_cm": 20.0}
    )  # Significantly below the 25th percentile
    percentile = patient.calculate_hcirc_percentile()
    assert percentile == 0.0


def test_high_value_returns_hundred(patch_dependencies):
    """Test that a very high head circumference returns a percentile close to 100."""
    patient = Patient(
        age=25, sex=Sex.M, hcirc={"value_cm": 70.0}
    )  # Significantly above the 75th percentile
    percentile = patient.calculate_hcirc_percentile()
    assert percentile == 100.0


def test_mid_value_returns_between_zero_and_hundred(patch_dependencies):
    """Test that a mid-range head circumference returns a percentile between 0 and 100."""
    patient = Patient(
        age=25, sex=Sex.M, hcirc={"value_cm": 55.0}
    )  # Between the 25th and 75th percentiles
    percentile = patient.calculate_hcirc_percentile()
    assert 0.0 < percentile < 100.0


def test_female_percentile_larger_than_male(patch_dependencies):
    """Test that a female always provides a larger percentile than a male for the same value."""
    age = 25
    hcirc_value = 55.0

    male_patient = Patient(age=age, sex=Sex.M, hcirc={"value_cm": hcirc_value})
    female_patient = Patient(age=age, sex=Sex.F, hcirc={"value_cm": hcirc_value})

    male_percentile = male_patient.calculate_hcirc_percentile()
    female_percentile = female_patient.calculate_hcirc_percentile()

    assert female_percentile > male_percentile, (
        f"Expected female percentile to be greater than male percentile for the same "
        f"head circumference {hcirc_value}cm and age {age}, but got {female_percentile}% "
        f"for female and {male_percentile}% for male."
    )
