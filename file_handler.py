class FileHandler:
    """Чтение выражения из текстового файла."""
    def read_from_file(self, filename: str) -> str:
        with open(filename, 'r', encoding='utf-8') as f:
            line = f.readline()
            if not line:
                raise ValueError("Файл пуст")
            return line.strip()