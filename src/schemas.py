from datetime import date
from enum import Enum
from typing import Union

from pydantic import BaseModel, Field, field_validator

from .models import Sex


class HcircUnitEnum(str, Enum):
    cm = "cm"
    inch = "inch"


class AgeUnitEnum(str, Enum):
    years = "years"
    months = "months"
    weeks = "weeks"
    days = "days"
    dob = "dob"


class NormalizedPatientData(BaseModel):
    age_years: float
    sex: Sex
    hcirc_cm: float


class PatientInput(BaseModel):
    age_unit: AgeUnitEnum
    age_value: Union[float, date] = Field(
        union_mode="left_to_right"
    )  # For years/months/weeks/days or date of birth
    sex: Sex
    hcirc_value: float
    hcirc_unit: HcircUnitEnum

    @field_validator("age_value")
    def validate_age_value(cls, v, values):
        if isinstance(v, date) and v > date.today():
            raise ValueError("Date of birth cannot be in the future.")
        return v

    def to_normalized(self) -> "NormalizedPatientData":
        """Normalize input values to years, sex as 'M' or 'F', and head circumference in cm."""
        # Normalize age to years based on the age_unit
        if self.age_unit == AgeUnitEnum.dob:
            assert isinstance(self.age_value, date)
            today = date.today()
            age_years = (today - self.age_value).days / 365.25
        else:
            if isinstance(self.age_value, date) and self.age_value == date(1970, 1, 1):
                # TODO: Stop Pydantic coercing 0.0 into a date
                age_value_float = 0.0
            elif isinstance(self.age_value, float):
                age_value_float = self.age_value
            else:
                raise ValueError("Invalid age value provided.")

            if age_value_float == 0.0:
                age_years = 0.0
            elif self.age_unit == AgeUnitEnum.years:
                age_years = age_value_float
            elif self.age_unit == AgeUnitEnum.months:
                age_years = age_value_float / 12.0
            elif self.age_unit == AgeUnitEnum.weeks:
                age_years = age_value_float / 52.1775
            elif self.age_unit == AgeUnitEnum.days:
                age_years = age_value_float / 365.25
            else:
                raise ValueError("Invalid age unit provided.")

        # Normalize head circumference to cm
        if self.hcirc_value is None or self.hcirc_value < 0:
            raise ValueError("No valid head circumference value was provided.")

        if self.hcirc_unit == HcircUnitEnum.inch:
            hcirc_cm = self.hcirc_value * 2.54
        else:
            hcirc_cm = self.hcirc_value

        return NormalizedPatientData(
            age_years=age_years, sex=self.sex, hcirc_cm=hcirc_cm
        )
