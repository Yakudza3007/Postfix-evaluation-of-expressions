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
            print("Попробуйте ещё раз или оставьте пустую строку для возврата в меню.")

    def _generate_expression(self):
        expr = self.generator.generate()
        print(f"Сгенерированное выражение: {expr}")
        return expr

    def _save_result(self, result):
        while True:
            answer = input("Сохранить результат в файл? (д/н или y/n): ").strip().lower()
            if answer in ('д', 'y', 'yes', 'да'):
                while True:
                    filename = input("Введите имя файла для сохранения (пустая строка - отмена): ").strip()
                    if filename == '':
                        print("Сохранение отменено.")
                        return
                    try:
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(str(result))
                        print(f"Результат сохранён в файл '{filename}'.")
                        return
                    except Exception:
                        print("Ошибка: такое название файла не поддерживается.")
            elif answer in ('н', 'n', 'no', 'нет'):
                print("Сохранение отменено.")
                return
            else:
                print("Пожалуйста, ответьте 'д' (да) или 'н' (нет).")

    def _ask_repeat(self, action_name):
        while True:
            answer = input(f"1 - {action_name} ещё раз, 2 - вернуться в главное меню: ").strip()
            if answer == '1':
                return True
            elif answer == '2':
                return False
            else:
                print("Пожалуйста, введите 1 или 2.")

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
                action_name = "прочитать файл"
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
                    try:
                        result = self.calculator.evaluate(expr)
                        print(f"\nРезультат: {result}\n")
                        self._save_result(result)
                    except Exception as e:
                        print(f"Ошибка при вычислении: {e}")
                    if not self._ask_repeat(action_name):
                        break