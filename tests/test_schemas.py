from datetime import date

import pytest

from src.models import Sex
from src.schemas import AgeUnitEnum, HcircUnitEnum, PatientInput


@pytest.fixture
def patient_input_years():
    return PatientInput(
        age_unit=AgeUnitEnum.years,
        age_value=5.0,
        sex=Sex.M,
        hcirc_value=50.0,
        hcirc_unit=HcircUnitEnum.cm,
    )


@pytest.fixture
def patient_input_months():
    return PatientInput(
        age_unit=AgeUnitEnum.months,
        age_value=24.0,  # 2 years
        sex=Sex.M,
        hcirc_value=50.0,
        hcirc_unit=HcircUnitEnum.cm,
    )


@pytest.fixture
def patient_input_weeks():
    return PatientInput(
        age_unit=AgeUnitEnum.weeks,
        age_value=104.355,  # 2 years
        sex=Sex.F,
        hcirc_value=50.0,
        hcirc_unit=HcircUnitEnum.cm,
    )


@pytest.fixture
def patient_input_days():
    return PatientInput(
        age_unit=AgeUnitEnum.days,
        age_value=730.5,  # 2 years
        sex=Sex.F,
        hcirc_value=50.0,
        hcirc_unit=HcircUnitEnum.cm,
    )


@pytest.fixture
def patient_input_dob():
    dob = date.today().replace(year=date.today().year - 2)
    return PatientInput(
        age_unit=AgeUnitEnum.dob,
        age_value=dob,
        sex=Sex.M,
        hcirc_value=50.0,
        hcirc_unit=HcircUnitEnum.cm,
    )


@pytest.fixture
def patient_input_inches():
    return PatientInput(
        age_unit=AgeUnitEnum.years,
        age_value=2.0,
        sex=Sex.M,
        hcirc_value=19.685,  # 50 cm in inches
        hcirc_unit=HcircUnitEnum.inch,
    )


def test_normalize_age_in_years(patient_input_years):
    normalized = patient_input_years.to_normalized()
    assert normalized.age_years == 5.0
    assert normalized.hcirc_cm == 50.0
    assert normalized.sex == Sex.M


def test_normalize_age_in_months(patient_input_months):
    normalized = patient_input_months.to_normalized()
    assert normalized.age_years == 2.0
    assert normalized.hcirc_cm == 50.0


def test_normalize_age_in_weeks(patient_input_weeks):
    normalized = patient_input_weeks.to_normalized()
    assert pytest.approx(normalized.age_years, 0.001) == 2.0
    assert normalized.hcirc_cm == 50.0


def test_normalize_age_in_days(patient_input_days):
    normalized = patient_input_days.to_normalized()
    assert pytest.approx(normalized.age_years, 0.001) == 2.0
    assert normalized.hcirc_cm == 50.0


def test_normalize_age_by_dob(patient_input_dob):
    normalized = patient_input_dob.to_normalized()
    assert pytest.approx(normalized.age_years, 0.001) == 2.0
    assert normalized.hcirc_cm == 50.0


def test_normalize_hcirc_in_inches(patient_input_inches):
    normalized = patient_input_inches.to_normalized()
    assert pytest.approx(normalized.hcirc_cm, 0.001) == 50.0


def test_invalid_dob_in_future():
    future_dob = date.today().replace(year=date.today().year + 1)
    with pytest.raises(ValueError, match="Date of birth cannot be in the future."):
        PatientInput(
            age_unit=AgeUnitEnum.dob,
            age_value=future_dob,
            sex=Sex.M,
            hcirc_value=50.0,
            hcirc_unit=HcircUnitEnum.cm,
        )


def test_invalid_hcirc_value():
    with pytest.raises(
        ValueError, match="No valid head circumference value was provided."
    ):
        PatientInput(
            age_unit=AgeUnitEnum.years,
            age_value=2.0,
            sex=Sex.M,
            hcirc_value=-5.0,  # Invalid value
            hcirc_unit=HcircUnitEnum.cm,
        ).to_normalized()  # Ensure normalization is called to trigger validation


def test_invalid_age_value():
    with pytest.raises(ValueError, match="Invalid age value provided."):
        PatientInput(
            age_unit=AgeUnitEnum.years,
            age_value=date(2010, 1, 1),  # Invalid date coerced by Pydantic
            sex=Sex.M,
            hcirc_value=50.0,
            hcirc_unit=HcircUnitEnum.cm,
        ).to_normalized()  # Ensure normalization is called to trigger validation
