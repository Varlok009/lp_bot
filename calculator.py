import telegram


def clean_expression(expression: str) -> str:
    expression = ''.join([
        char for char in expression
        if char.isdigit() or char in '-/+*()'
        ])
    return expression


def execute_expression(expression: str) -> str:
    expression = clean_expression(expression)
    try:
        result_of_expression = eval(expression)
        return f'Result your expression = {result_of_expression}'
    except ZeroDivisionError:
        return "Can't divide by zero"
    except SyntaxError:
        return "Incorrect expression"


def handle_calculator(update: telegram.Update, context) -> None:
    if update.message and update.message.text and '/calc' in update.message.text:
        expression = update.message.text.replace('/calc', '')
    update.message.reply_text(execute_expression(expression))
