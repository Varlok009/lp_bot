

def get_clean_string(user_input: str) -> str:
    """
    Возвращает строку, очищенную от знаков пунктуации, двойных пробелов и чисел в нижнем регистре.
    """
    user_input = ''.join(char for char in user_input.strip().lower() if char.isalpha() or char.isspace())
    while '  ' in user_input:
        user_input = user_input.replace('  ', ' ')
    return user_input


if __name__ == "__main__":
    pass
