from datetime import date
from typing import Union

from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated


class NormalizedPatientData(BaseModel):
    age_years: float
    sex: str
    hcirc_value: float


class PatientInput(BaseModel):
    age_years: Annotated[Union[float, None], Field(strict=True)] = None
    age_months: Annotated[Union[float, None], Field(strict=True)] = None
    date_of_birth: Union[date, None] = None  # Date of birth
    sex: str
    hcirc_value: Annotated[Union[float, None], Field(strict=True)] = None
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
        """Normalize input values to years, sex as "M" or "F", and head circumference in cm."""
        # Convert age to years if given in months or date of birth
        if self.age_years is not None:
            age_years = self.age_years
        elif self.age_months is not None:
            age_years = self.age_months / 12.0
        elif self.date_of_birth is not None:
            today = date.today()
            age_years = (today - self.date_of_birth).days / 365.25
        else:
            raise ValueError(
                "At least one of age_years, age_months, or date_of_birth must be provided."
            )

        # Normalize head circumference to cm
        if self.hcirc_value and self.hcirc_unit == "in":
            hcirc_cm = self.hcirc_value * 2.54
        elif self.hcirc_value:
            hcirc_cm = self.hcirc_value
        else:
            raise ValueError("No head circumference value was provided.")

        return NormalizedPatientData(
            age_years=age_years, sex=self.sex, hcirc_value=hcirc_cm
        )
