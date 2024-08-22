from datetime import date
from typing import Union

from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated


class PatientInput(BaseModel):
    age_years: Annotated[Union[int, None], Field(strict=True)] = None
    age_months: Annotated[Union[int, None], Field(strict=True)] = None
    date_of_birth: Union[date, None] = None  # Date of birth
    sex: str
    hcirc_value: Annotated[Union[int, None], Field(strict=True)] = None
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

    def normalize(self):
        """Normalize input values to years, sex as "M" or "F", and head circumference in cm."""
        # Convert age to years if given in months
        if self.age_months is not None:
            age_years = self.age_months / 12.0
        elif self.date_of_birth is not None:
            today = date.today()
            age_years = (today - self.date_of_birth).days / 365.25
        else:
            age_years = self.age_years

        # Normalize head circumference to cm
        if self.hcirc_unit == "in":
            hcirc_cm = self.hcirc_value * 2.54
        else:
            hcirc_cm = self.hcirc_value

        return {"age_years": age_years, "sex": self.sex, "hcirc_cm": hcirc_cm}
