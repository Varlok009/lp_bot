

def get_clean_string(user_input: str) -> str:
    """
    Возвращает строку, очищенную от знаков пунктуации,
    двойных пробелов и чисел в нижнем регистре.
    """
    user_input = ''.join(
        char for char in user_input.strip().lower()
        if char.isalpha() or char.isspace()
        )

    if ' ' not in user_input:
        return user_input

    user_input = ' '.join(user_input.split())
    return user_input


if __name__ == "__main__":
    pass
