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
                self.calculator.evaluate(expr)
                return expr
            except FileNotFoundError:
                print(f"Ошибка: файл '{filename}' не найден.")
            except IOError as e:
                print(f"Ошибка ввода-вывода: {e}")
            except (ValueError, ZeroDivisionError) as e:
                print(f"Ошибка в содержимом файла: {e}")
            except Exception as e:
                print(f"Непредвиденная ошибка: {e}")
            print("Попробуйте ещё раз или оставьте пустую строку для возврата в меню.")

    def _generate_expression(self):
        print("Генерируется случайное выражение...")
        expr = self.generator.generate()
        print(f"Сгенерированное выражение: {expr}")
        return expr

    def _save_result(self, result):
        while True:
            answer = input("Сохранить результат в файл? (д/н или y/n): ").strip().lower()
            if answer in ('д', 'y', 'yes', 'да'):
                filename = input("Введите имя файла для сохранения: ").strip()
                if filename == '':
                    print("Имя файла не может быть пустым. Сохранение отменено.")
                    return
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(str(result))
                    print(f"Результат сохранён в файл '{filename}'.")
                except IOError as e:
                    print(f"Ошибка сохранения: {e}")
                return
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

            expr = None
            if choice == '1':
                expr = self._input_expression()
            elif choice == '2':
                expr = self._read_from_file()
            elif choice == '3':
                expr = self._generate_expression()

            if expr is None:
                continue

            try:
                result = self.calculator.evaluate(expr)
                print(f"\nРезультат: {result}\n")
                self._save_result(result)
            except Exception as e:
                print(f"Ошибка при вычислении: {e}")
            input("Нажмите Enter, чтобы продолжить...")