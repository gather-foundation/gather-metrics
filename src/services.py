from fastapi.exceptions import HTTPException

from models import Patient
from schemas import NormalizedPatientData


def calculate_hcirc_percentile(patient_data: NormalizedPatientData) -> float:
    try:
        patient = Patient(
            age=patient_data.age_years,
            sex=patient_data.sex,
            hcirc={"value_cm": patient_data.hcirc_cm},
        )
        result = patient.calculate_hcirc_percentile()
        return result
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="There was an unexpected error processing your request",
        )
