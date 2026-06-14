from rpn_calculator import RPNCalculator
from expression_generator import ExpressionGenerator
from file_handler import FileHandler

class Menu:
    def __init__(self):
        self.calculator = RPNCalculator()
        self.generator = ExpressionGenerator()
        self.file_handler = FileHandler()

    def _print_menu(self):
        print("\n=== Калькулятор обратной польской записи ===")
        print("1. Ввести выражение вручную")
        print("2. Прочитать выражение из файла")
        print("3. Сгенерировать случайное выражение")
        print("4. Выход")
        print("===========================================")

    def _get_user_choice(self):
        while True:
            choice = input("Выберите пункт меню (1-4): ").strip()
            if choice in ('1', '2', '3', '4'):
                return choice
            print("Некорректный ввод. Пожалуйста, введите 1, 2, 3 или 4.")

    def _input_expression(self):
        print("Введите выражение в постфиксной записи (числа и операции разделены пробелами)")
        print("(для возврата в меню оставьте строку пустой или введите 'menu'):")
        while True:
            expr = input("> ").strip()
            if expr == '' or expr.lower() == 'menu':
                return None
            try:
                self.calculator.evaluate(expr)
                return expr
            except (ValueError, ZeroDivisionError) as e:
                print(f"Ошибка: {e}")
                print("Попробуйте ещё раз или оставьте пустую строку для возврата в меню.")

    def _read_from_file(self):
        print("Введите путь к файлу (пустая строка для возврата в меню):")
        while True:
            filename = input("> ").strip()
            if filename == '':
                return None
            try:
                expr = self.file_handler.read_from_file(filename)
                print(f"Содержимое файла: {expr}")
                self.calculator.evaluate(expr)
                return expr
            except FileNotFoundError:
                print(f"Ошибка: файл '{filename}' не найден.")
            except IOError as e:
                print(f"Ошибка ввода-вывода: {e}")
            except (ValueError, ZeroDivisionError) as e:
                if 'expr' in locals():
                    print(f"Содержимое файла (повторно): {expr}")
                print(f"Ошибка в содержимом файла: {e}")
            except Exception as e:
                print(f"Непредвиденная ошибка: {e}")
            print(
                "Попробуйте ещё раз или оставьте пустую строку для возврата в меню.")

    def _generate_expression(self):
        """Генерирует случайное выражение."""
        expr = self.generator.generate()
        print(f"Сгенерированное выражение: {expr}")
        return expr

    def _save_result(self, result):
        """Предлагает сохранить результат в файл с повторными попытками при ошибке."""
        while True:
            answer = input(
                "Сохранить результат в файл? (д/н или y/n): ").strip().lower()
            if answer in ('д', 'y', 'yes', 'да'):
                while True:
                    filename = input(
                        "Введите имя файла для сохранения (пустая строка - отмена): ").strip()
                    if filename == '':
                        print("Сохранение отменено.")
                        return
                    try:
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(str(result))
                        print(f"Результат сохранён в файл '{filename}'.")
                        return
                    except OSError as e:
                        if e.errno == 22:
                            print(
                                "Ошибка: имя файла содержит недопустимые символы или неправильно сформировано.")
                        elif e.errno == 2:
                            print(
                                "Ошибка: указанный каталог не существует. Проверьте путь.")
                        elif e.errno == 13:
                            print(
                                "Ошибка: недостаточно прав для записи в указанный файл или папку.")
                        elif e.errno == 21:
                            print(
                                "Ошибка: указанное имя является папкой, а не файлом.")
                        else:
                            print(f"Ошибка: {e.strerror}")
                        print("Попробуйте ввести другое имя файла.")
                        continue
            elif answer in ('н', 'n', 'no', 'нет'):
                print("Сохранение отменено.")
                return
            else:
                print("Пожалуйста, ответьте 'д' (да) или 'н' (нет).")

    def run(self):
        while True:
            self._print_menu()
            choice = self._get_user_choice()
            if choice == '4':
                print("Выход из программы.")
                return

            if choice == '1':
                action_name = "ввести выражение"
                while True:
                    expr = self._input_expression()
                    if expr is None:
                        break
                    try:
                        result = self.calculator.evaluate(expr)
                        print(f"\nРезультат: {result}\n")
                        self._save_result(result)
                    except Exception as e:
                        print(f"Ошибка при вычислении: {e}")
                    if not self._ask_repeat(action_name):
                        break
            elif choice == '2':
                action_name = "ввести название файла"
                while True:
                    expr = self._read_from_file()
                    if expr is None:
                        break
                    try:
                        result = self.calculator.evaluate(expr)
                        print(f"\nРезультат: {result}\n")
                        self._save_result(result)
                    except Exception as e:
                        print(f"Ошибка при вычислении: {e}")
                    if not self._ask_repeat(action_name):
                        break
            elif choice == '3':
                action_name = "сгенерировать выражение"
                while True:
                    expr = self._generate_expression()
                    if expr is None:
                        break
                    try:
                        result = self.calculator.evaluate(expr)
                        print(f"\nРезультат: {result}\n")
                        self._save_result(result)
                    except Exception as e:
                        print(f"Ошибка при вычислении: {e}")
                    if not self._ask_repeat(action_name):
                        break