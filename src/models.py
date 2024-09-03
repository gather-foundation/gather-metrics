from enum import Enum
from typing import Union

import numpy as np
from scipy import stats  # type: ignore

from .utils.csv_loader import load_csv
from .utils.hcirc_utils import norm_from_percentiles


class Sex(str, Enum):
    M = "M"
    F = "F"


class Patient:
    def __init__(
        self,
        age: Union[int, float],
        sex: str,
        hcirc: dict[str, float],
    ):
        if age < 0:
            raise ValueError("Age must not be a negative number.")

        if "value_cm" not in hcirc or hcirc["value_cm"] < 0:
            raise ValueError(
                "Head circumference (value_cm) must not be a negative number."
            )

        if not isinstance(sex, Sex):
            raise ValueError(
                f"Sex must be an instance of the Sex enum, got {sex} instead."
            )

        self.age = age
        self.sex = Sex(sex)
        self.hcirc = hcirc

    def calculate_hcirc_percentile(self) -> float:

        male = load_csv("data/hcirc_model/male.tsv")
        maleAge = np.array(male["Age"])
        male25 = np.array(male["25"])
        male75 = np.array(male["75"])

        female = load_csv("data/hcirc_model/female.tsv")
        femaleAge = np.array(female["Age"])
        female25 = np.array(female["25"])
        female75 = np.array(female["75"])

        if self.sex == Sex.M:
            if self.age > max(maleAge):
                self.age = max(maleAge)
            age25 = np.interp(self.age, maleAge, male25)
            age75 = np.interp(self.age, maleAge, male75)
        elif self.sex == Sex.F:
            if self.age > max(femaleAge):
                self.age = max(femaleAge)
            age25 = np.interp(self.age, femaleAge, female25)
            age75 = np.interp(self.age, femaleAge, female75)

        loc, scale = norm_from_percentiles(age25, 0.25, age75, 0.75)

        perc = stats.norm.cdf(self.hcirc["value_cm"], loc=loc, scale=scale)
        perc_rounded = round(perc * 100, 2)
        self.hcirc["percentile"] = perc_rounded
        return self.hcirc["percentile"]
