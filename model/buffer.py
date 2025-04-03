from typing import List
from model.MyString import MyString as MyStringWrapper
class Buffer:
    def __init__(self):
        self._lines: List[MyStringWrapper] = []
        self._current_line = 0
        self._modified = False
        self._filename = None

    @property
    def lines(self) -> List[MyStringWrapper]:
        return self._lines

    @property
    def current_line(self) -> int:
        return self._current_line

    @current_line.setter
    def current_line(self, value: int):
        self._current_line = max(0, min(value, len(self._lines) - 1))

    @property
    def is_modified(self) -> bool:
        return self._modified

    @property
    def filename(self) -> str:
        return self._filename

    def set_filename(self, filename: str):
        self._filename = filename

    def get_line(self, index: int) -> MyStringWrapper:
        if 0 <= index < len(self._lines):
            return self._lines[index]
        return MyStringWrapper()

    def set_line(self, index: int, text: str) -> None:
        if 0 <= index < len(self._lines):
            self._lines[index] = MyStringWrapper(text)
            self._modified = True

    def get_line_count(self) -> int:
        return len(self._lines)

    def insert_line(self, index: int, text: str = ""):
        self._lines.insert(index, MyStringWrapper(text))
        self._modified = True

    def append_line(self, text: str = ""):
        self._lines.append(MyStringWrapper(text))
        self._modified = True
    
    def delete_line(self, index: int):
        if 0 <= index < len(self._lines):
            del self._lines[index]
            if not self._lines:
                self._lines.append(MyStringWrapper())
            self._modified = True

    def clear(self):
        self._lines = []
        self._current_line = 0
        self._modified = False

    def load_file(self, filename: str):
        try:
            self._lines.clear()
            with open(filename, 'r') as f:
                lines = f.readlines()
                self._lines = [MyStringWrapper(line.rstrip('\n')) for line in lines]
                if not self._lines:
                    self._lines = [MyStringWrapper()]
                self._filename = filename
                self._modified = False
        except Exception as e:
            raise IOError(f"Failed to load file {filename}: {str(e)}")
    
    def save_file(self, filename: str = None):
        save_filename = filename or self._filename
        if not save_filename:
            raise ValueError("No filename specified")
        
        try:
            with open(save_filename, 'w') as f:
                for line in self._lines:
                    f.write(str(line) + '\n')
            self._filename = save_filename
            self._modified = False
        except Exception as e:
            raise IOError(f"Failed to save file {save_filename}: {str(e)}")
    