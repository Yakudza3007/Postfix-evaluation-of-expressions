class ExpressionGenerator:
    """Генерация случайного корректного постфиксного выражения без использования random."""
    def __init__(self, seed=42):
        # Простой линейный конгруэнтный генератор
        self.state = seed
        self.modulus = 2**31
        self.multiplier = 1103515245
        self.increment = 12345

    def _next_float(self):
        """Генерирует псевдослучайное число в диапазоне [0, 1)."""
        self.state = (self.multiplier * self.state + self.increment) % self.modulus
        return self.state / self.modulus

    def _uniform(self, low, high):
        """Случайное число в [low, high)."""
        return low + self._next_float() * (high - low)

    def _randint(self, low, high):
        """Случайное целое число в [low, high]. (включительно)"""
        return int(self._uniform(low, high + 1))

    def _choice(self, seq):
        """Случайный элемент из последовательности."""
        idx = self._randint(0, len(seq) - 1)
        return seq[idx]

    def generate(self, min_operands=2, max_operands=6):
        operations = ['+', '-', '*', '/']

        num_operands = self._randint(min_operands, max_operands)
        # Создаём операнды (положительные вещественные от 1 до 20)
        operands = [round(self._uniform(1, 20), 2) for _ in range(num_operands)]

        # Рекурсивное построение бинарного дерева в постфиксном порядке
        def build_tree(leaf_count):
            if leaf_count == 1:
                return [str(operands.pop(0))]
            left_leaves = self._randint(1, leaf_count - 1)
            right_leaves = leaf_count - left_leaves
            left_expr = build_tree(left_leaves)
            right_expr = build_tree(right_leaves)
            op = self._choice(operations)
            return left_expr + right_expr + [op]

        # Копируем, так как будем изменять список
        operands_copy = operands[:]
        tokens = build_tree(num_operands)
        return ' '.join(tokens)