from datetime import date
from typing import Any, Union

from .models import Patient, Sex
from .schemas import AgeUnitEnum, HcircUnitEnum, NormalizedPatientData, PatientInput


def is_valid_age(age_value: Union[float, date], age_unit: str) -> tuple[bool, dict]:
    context: dict[str, Any] = {
        "age_value": age_value,
        "age_unit": AgeUnitEnum(age_unit),
        "error_message": None,
        "info_message": None,
    }

    if not age_value:
        print("no age value", age_value)
        return True, context

    # Inline validation for future date of birth
    if age_unit == "dob":
        assert isinstance(age_value, date)
        if age_value > date.today():
            context["error_message"] = "Date of birth cannot be in the future."
            return True, context  # has_error is True

    # Create a temporary PatientInput instance for validation
    patient_input = PatientInput(
        age_unit=AgeUnitEnum(age_unit),
        age_value=age_value,
        sex=Sex.M,  # Temporarily assign valid values for other fields
        hcirc_value=0,
        hcirc_unit=HcircUnitEnum.cm,
    )

    # Normalize the data and check if age is over 21
    normalized_data = patient_input.to_normalized()
    age_years = normalized_data.age_years

    # Add info message if age is over 21
    if age_years > 21:
        context["info_message"] = (
            "Ages over 21 years are accepted, but they won't affect the result."
        )

    return False, context  # has_error is False


def calculate_hcirc_percentile(patient_data: NormalizedPatientData) -> float:
    patient = Patient(
        age=patient_data.age_years,
        sex=patient_data.sex,
        hcirc={"value_cm": patient_data.hcirc_cm},
    )
    result = patient.calculate_hcirc_percentile()
    return result
