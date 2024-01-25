import base64

import streamlit as st

from program.routers import MultiplicationRouter

letter = 'A'


def increment_sequence(s):
    s = s.upper()

    incremented_str = ""
    carry = 1
    for char in reversed(s):
        if carry:
            new_ord = ord(char) + 1
            carry = new_ord > ord('Z')
            char = chr((new_ord - ord('A')) % 26 + ord('A'))
        incremented_str = char + incremented_str

    if carry:
        incremented_str = "A" + incremented_str

    return incremented_str


def dict_to_mermaid(data, parent='A'):
    mermaid_code = ""

    if isinstance(data, dict):
        for key1, value1 in data.items():
            if isinstance(value1, dict):
                for key2, value2 in value1.items():
                    global letter
                    letter = increment_sequence(letter)
                    mermaid_code += f"  {parent}[\"{key1}\"] --> |\"{key2}\"| {letter}[\"{key2}\"]\n"
                    mermaid_code += dict_to_mermaid(value2, letter)
            else:
                letter = increment_sequence(letter)
                mermaid_code += f"  {parent}[\"{key1}\"] --> {letter}[\"{value1}\"]\n"

    return mermaid_code


def main():
    st.title("Cognitive Multiplication Router")

    # Get user input
    num1 = st.number_input("Enter the first number:", value=1)
    num2 = st.number_input("Enter the second number:", value=1)

    if st.button("Execute multiplication"):
        # Perform multiplication
        st.write(f"{num1}*{num2} should equal {num1 * num2}")

        router = MultiplicationRouter(num1, num2)
        result = router.exec()

        st.write(f"{num1}*{num2} = {result}")

        # Generate and display Mermaid graph
        graphbytes = f"""\
        graph LR;
        {dict_to_mermaid(router.equation)}
        """.encode("utf8")
        base64_bytes = base64.b64encode(graphbytes)
        base64_string = base64_bytes.decode("ascii")
        st.image("https://mermaid.ink/img/" + base64_string)


if __name__ == "__main__":
    main()
