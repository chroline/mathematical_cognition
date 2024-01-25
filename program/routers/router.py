from typing import Type

from program.networks import digits_classifier
from program.utils import generate_response
from .utils import BaseCase

DECISION_PROMPT = """\
    You will be provided with information on two numbers. Based on this information, you are tasked with determining which of the following cases applies:

    **Case 1:** The first number is more than one digit, irregardless of the second number.
    **Case 2:** The first number is one digit, while the second number is more than one digit.
    **Case 3:** Both numbers are one digit.

    Please respond with ONLY the case number (i.e. 1, 2, or 3), and no other text.
    """


class Router:
    equation = ""

    def __init__(self, num1: int, num2: int, cases: dict[int, Type[BaseCase]]):
        self.num1 = num1
        self.num2 = num2
        self.cases = cases

    def exec(self) -> int:
        classified_nums = digits_classifier.predict([[self.num1], [self.num2]], verbose=0)
        classified_nums = list(map(lambda pred: round(pred[0]), classified_nums))

        first_number_desc = "one digit" if classified_nums[0] == 0 else "more than one digit"
        second_number_desc = "one digit" if classified_nums[1] == 0 else "more than one digit"

        response = generate_response(
            system=DECISION_PROMPT,
            user=f"The first number is {first_number_desc}, the second number is {second_number_desc}."
        )

        case = self.cases.get(int(response))(self.num1, self.num2)

        response = case.exec()

        self.equation = case.equation

        return response
