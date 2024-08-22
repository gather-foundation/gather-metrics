from typing import Union


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
        print(self.age, self.sex, self.head_circumference["value"])
        self.head_circumference["percentile"] = 0.22
        return self.head_circumference["percentile"]
