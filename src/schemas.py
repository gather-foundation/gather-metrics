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
    age_value_float: Union[float, None] = None  # For years/months/weeks/days
    age_value_date: Union[date, None] = None  # For date of birth
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

    @model_validator(mode="before")
    def check_age_values(cls, values):
        age_unit = values.get("age_unit")
        age_value_float = values.get("age_value_float")
        age_value_date = values.get("age_value_date")

        if age_unit == "dob" and not age_value_date:
            raise ValueError(
                "Date of birth must be provided when 'dob' is selected as age unit."
            )
        elif age_unit != "dob" and age_value_float is None:
            raise ValueError(f"Age value must be provided when {age_unit} is selected.")

        return values

    def to_normalized(self) -> "NormalizedPatientData":
        """Normalize input values to years, sex as 'M' or 'F', and head circumference in cm."""

        # Normalize age to years based on the age_unit
        if self.age_unit == "years":
            age_years = self.age_value_float
        elif self.age_unit == "months":
            age_years = self.age_value_float / 12.0
        elif self.age_unit == "weeks":
            age_years = self.age_value_float / 52.1775  # 52.1775 weeks in a year
        elif self.age_unit == "days":
            age_years = (
                self.age_value_float / 365.25
            )  # 365.25 days in a year to account for leap years
        elif self.age_unit == "dob":
            today = date.today()
            age_years = (today - self.age_value_date).days / 365.25
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
