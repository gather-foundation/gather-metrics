from datetime import date
from typing import Union

from pydantic import BaseModel, Field, field_validator, model_validator
from typing_extensions import Annotated


class NormalizedPatientData(BaseModel):
    age_years: float
    sex: str
    hcirc_cm: float


class PatientInput(BaseModel):
    age_unit: str
    age_value: Union[float, date] = None  # For years/months/weeks/days or date of birth
    sex: str
    hcirc_value: float
    hcirc_unit: str

    @field_validator("sex")
    def validate_sex(cls, v):
        if v not in {"M", "F"}:
            raise ValueError('Sex must be "M" or "F"')
        return v

    @field_validator("hcirc_unit")
    def validate_hcirc_unit(cls, v):
        if v not in {"cm", "in"}:
            raise ValueError('Head circumference unit must be "cm" or "in"')
        return v

    def to_normalized(self) -> "NormalizedPatientData":
        """Normalize input values to years, sex as 'M' or 'F', and head circumference in cm."""

        # Normalize age to years based on the age_unit
        if self.age_unit == "years":
            age_years = self.age_value
        elif self.age_unit == "months":
            age_years = self.age_value / 12.0
        elif self.age_unit == "weeks":
            age_years = self.age_value / 52.1775  # 52.1775 weeks in a year
        elif self.age_unit == "days":
            age_years = (
                self.age_value / 365.25
            )  # 365.25 days in a year to account for leap years
        elif self.age_unit == "dob":
            today = date.today()
            age_years = (today - self.age_value).days / 365.25
        else:
            raise ValueError("Invalid age unit provided.")

        # Normalize head circumference to cm
        if self.hcirc_value and self.hcirc_unit == "in":
            hcirc_cm = self.hcirc_value * 2.54
        elif self.hcirc_value:
            hcirc_cm = self.hcirc_value
        else:
            raise ValueError("No head circumference value was provided.")

        return NormalizedPatientData(
            age_years=age_years, sex=self.sex, hcirc_cm=hcirc_cm
        )
