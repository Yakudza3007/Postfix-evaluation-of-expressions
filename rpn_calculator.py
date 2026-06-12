from stack import Stack

class RPNCalculator:
    """Вычисление арифметических выражений в постфиксной записи."""
    def evaluate(self, expression: str) -> float:
        stack = Stack()
        tokens = expression.strip().split()
        if not tokens:
            raise ValueError("Пустое выражение")

        for token in tokens:
            try:
                number = float(token)
                stack.push(number)
            except ValueError:
                if token in ('+', '-', '*', '/'):
                    if stack.size() < 2:
                        raise ValueError(f"Недостаточно операндов для операции '{token}'")
                    b = stack.pop()
                    a = stack.pop()
                    if token == '+':
                        res = a + b
                    elif token == '-':
                        res = a - b
                    elif token == '*':
                        res = a * b
                    elif token == '/':
                        if b == 0:
                            raise ZeroDivisionError("Деление на ноль")
                        res = a / b
                    stack.push(res)
                else:
                    raise ValueError(f"Недопустимый токен: '{token}'")

        if stack.size() != 1:
            raise ValueError("Некорректное выражение: в стеке осталось больше одного значения")
        return stack.pop()