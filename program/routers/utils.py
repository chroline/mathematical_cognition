from abc import abstractmethod


class BaseCase:
    stack = list()

    def __init__(self, num1: int, num2: int):
        self.num1 = num1
        self.num2 = num2

    @abstractmethod
    def exec(self) -> int:
        pass

    @property
    @abstractmethod
    def equation(self) -> dict:
        pass


DIGIT_EXTRACTION_PROMPT = """\
    Your role is to take an input number and extract the right-most digit, placing it as the last element, and the remaining digits as a list in JSON format.

    Examples: 
    Input: 100, Output: [10, 0]
    Input: 12345, Output: [1234, 5].

    The user will provide you with the number."""
