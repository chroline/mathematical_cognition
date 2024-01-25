import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)


def generate_response(system: str, user: str | None):
    messages = [{"role": "system", "content": system}]
    if user:
        messages.append({"role": "user", "content": user})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content


vector_size = 7


# Convert base 10 number to binary array
def decimal_to_binary_array(number):
    binary_representation = bin(number)[2:]
    binary_array = [int(bit) for bit in binary_representation.zfill(vector_size)]
    return binary_array


# Convert binary array to base 10 number
def binary_array_to_decimal(binary_array):
    binary_string = ''.join(map(str, binary_array))
    decimal_number = int(binary_string, 2)
    return decimal_number
