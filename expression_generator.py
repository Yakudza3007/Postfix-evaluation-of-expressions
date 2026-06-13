class ExpressionGenerator:
    """Генератор случайных постфиксных выражений."""
    def __init__(self, seed=0):
        self.state = seed

    def _next(self):
        """Следующее случайное число от 0 до 99."""
        self.state = (self.state + 1) % 100
        return self.state

    def _randint(self, low, high):
        """Возвращает целое случайное число от low до high."""
        r = self._next()
        return low + (r % (high - low + 1))

    def _choice(self, seq):
        """Случайный элемент из списка."""
        idx = self._randint(0, len(seq) - 1)
        return seq[idx]

    def generate(self, min_operands=2, max_operands=6):
        """Возвращает строку в виде постфиксного выражения."""
        operations = ['+', '-', '*', '/']
        num_operands = self._randint(min_operands, max_operands)
        operands = []

        for i in range(num_operands):
            whole = self._randint(1, 19)
            frac = self._randint(0, 99)
            value = whole + frac / 100.0
            operands.append(round(value, 2))

        operands_copy = operands[:]

        def build_tree(leaf_count):
            """Рекурсивно строит список токенов в постфиксном порядке."""
            if leaf_count == 1:
                return [str(operands_copy.pop(0))]
            left_leaves = self._randint(1, leaf_count - 1)
            right_leaves = leaf_count - left_leaves
            left_expr = build_tree(left_leaves)
            right_expr = build_tree(right_leaves)
            op = self._choice(operations)
            return left_expr + right_expr + [op]

        tokens = build_tree(num_operands)
        return ' '.join(tokens)