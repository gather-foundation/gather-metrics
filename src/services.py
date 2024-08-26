from fastapi.exceptions import HTTPException

from models import Patient
from schemas import NormalizedPatientData


def calculate_hcirc_percentile(patient_data: NormalizedPatientData) -> float:
    patient = Patient(
        age=patient_data.age_years,
        sex=patient_data.sex,
        hcirc={"value_cm": patient_data.hcirc_cm},
    )
    result = patient.calculate_hcirc_percentile()
    return result
