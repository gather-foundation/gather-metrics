from typing import Union

import numpy as np
from scipy import stats

from utils.csv_loader import load_csv
from utils.hcirc_utils import norm_from_percentiles


class Patient:
    def __init__(
        self,
        age: Union[int, float],
        sex: str,
        head_circumference: dict[str, float],
    ):
        self.age = age
        self.sex = sex
        self.head_circumference = head_circumference

    def calculate_hcirc_percentile(self) -> float:

        male = load_csv("data/hcirc_model/male.tsv")
        maleAge = np.array(male["Age"])
        male25 = np.array(male["25"])
        male75 = np.array(male["75"])

        female = load_csv("data/hcirc_model/female.tsv")
        femaleAge = np.array(female["Age"])
        female25 = np.array(female["25"])
        female75 = np.array(female["75"])

        if self.sex == "M":
            if self.age > max(maleAge):
                self.age = max(maleAge)
            age25 = np.interp(self.age, maleAge, male25)
            age75 = np.interp(self.age, maleAge, male75)
            print("HELLO")
        elif self.sex == "F":
            if self.age > max(femaleAge):
                self.age = max(femaleAge)
            age25 = np.interp(self.age, femaleAge, female25)
            age75 = np.interp(self.age, femaleAge, female75)

        loc, scale = norm_from_percentiles(age25, 0.25, age75, 0.75)

        perc = stats.norm.cdf(self.head_circumference["value"], loc=loc, scale=scale)
        perc_rounded = round(perc * 100, 2)
        self.head_circumference["percentile"] = perc_rounded
        print(perc_rounded)
        return self.head_circumference["percentile"]
