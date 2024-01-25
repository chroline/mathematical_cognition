import json
from typing import Type

import numpy as np

from program.networks import multiplication_memory
from program.utils import decimal_to_binary_array, binary_array_to_decimal, generate_response
from .addition import AdditionRouter
from .router import Router
from .utils import DIGIT_EXTRACTION_PROMPT, BaseCase

cases: dict[int, Type[BaseCase]] = {}


class MultiplicationRouter(Router):
    def __init__(self, num1: int, num2: int):
        super().__init__(num1, num2, cases)

    def exec(self) -> int:
        if self.num1 == 0 or self.num2 == 0:
            self.equation = {f"{self.num1} * {self.num2}": 0}
            return 0

        return super().exec()


class Case1(BaseCase):
    _equation = {}

    @property
    def equation(self) -> dict:
        return self._equation

    def exec(self):
        response = generate_response(
            system=DIGIT_EXTRACTION_PROMPT,
            user=str(self.num1)
        )
        num1_digits = json.loads(response)

        r1 = MultiplicationRouter(num1_digits[0], self.num2)
        eq1 = r1.exec() * 10
        r2 = MultiplicationRouter(num1_digits[1], self.num2)
        eq2 = r2.exec()

        self._equation = {f"{self.num1}*{self.num2}": {
            f"({num1_digits[0]}*{self.num2})*10": r1.equation,
            f"{num1_digits[1]}*{self.num2}": r2.equation
        }}

        return AdditionRouter(eq1, eq2).exec()


cases[1] = Case1


class Case2(BaseCase):
    _equation = {}

    @property
    def equation(self) -> dict:
        return self._equation

    def exec(self):
        response = generate_response(
            system=DIGIT_EXTRACTION_PROMPT,
            user=str(self.num2)
        )
        num2_digits = json.loads(response)

        r1 = MultiplicationRouter(self.num1, num2_digits[0])
        eq1 = r1.exec() * 10
        r2 = MultiplicationRouter(self.num1, num2_digits[1])
        eq2 = r2.exec()

        self._equation = {f"{self.num1}*{self.num2}": {
            f"({self.num1}*{num2_digits[0]})*10": r1.equation,
            f"{self.num1}*{num2_digits[1]}": r2.equation
        }}

        return AdditionRouter(eq1, eq2).exec()


cases[2] = Case2


class Case3(BaseCase):
    _equation = ""

    @property
    def equation(self) -> str:
        return self._equation

    def exec(self):
        nn_input = np.concatenate((decimal_to_binary_array(self.num1), decimal_to_binary_array(self.num2)))
        prediction_binary = multiplication_memory.predict([nn_input], verbose=0)[0]
        prediction = binary_array_to_decimal(list(map(lambda n: 0 if n < .5 else 1, prediction_binary)))

        self._equation = {f"({self.num1} * {self.num2})": prediction}

        return prediction


cases[3] = Case3
