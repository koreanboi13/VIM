from typing import List, Optional, Tuple
from interfaces.i_model import IModel
from interfaces.i_modelObs import IModelObserver
from model.buffer import Buffer
import re
import os

class EditorModel(IModel):
    def __init__(self):
        self._observers: List[IModelObserver] = []
        self._buffer = Buffer()
        self._cursor_line = 0
        self._cursor_column = 0
        self._mode = "NORMAL"
        self._filename = "[No Name]"
        self._modified = False
        self._yanked_text = ""
        self._last_search = ""
        self._last_search_forward = True
        self.search_buffer = ""

    def add_observer(self, observer: IModelObserver) -> None:
        self._observers.append(observer)

    def remove_observer(self, observer: IModelObserver) -> None:
        self._observers.remove(observer)

    def _notify_text_changed(self) -> None:
        for observer in self._observers:
            observer.on_text_changed()

    def _notify_cursor_changed(self) -> None:
        for observer in self._observers:
            observer.on_cursor_changed(self._cursor_line, self._cursor_column)

    def _notify_mode_changed(self) -> None:
        for observer in self._observers:
            observer.on_mode_changed(self._mode)

    def _notify_file_changed(self) -> None:
        for observer in self._observers:
            observer.on_file_changed(self._filename)

    def get_line(self, line_number: int) -> str:
        return str(self._buffer.get_line(line_number))

    def get_current_line(self) -> str:
        return str(self._buffer.get_line(self._cursor_line))

    def get_line_count(self) -> int:
        return self._buffer.get_line_count()

    def get_cursor_position(self) -> Tuple[int, int]:
        return self._cursor_line, self._cursor_column
    
    def set_search_buffer(self, buffer: str) -> None:
        self.search_buffer += buffer

    def get_search_buffer(self) -> str:
        return self.search_buffer
    
    def clear_search_buffer(self) -> None:
        self.search_buffer = ""

    def set_tmp_filename(self, filename: str) -> None:
        self._tmp_filename = filename

    def get_tmp_filename(self) -> str:
        return self._tmp_filename
    
    def set_last_search(self, text: str) ->None:
        self._last_search = text

    def set_last_search_forward(self, forward: bool) -> None:
        self._last_search_forward = forward
        
    def set_cursor_position(self, line: int, column: int) -> None:
        old_line = self._cursor_line
        old_column = self._cursor_column
        
        line = max(0, min(line, self.get_line_count() - 1))
        
        line_length = len(self.get_line(line))
        column = max(0, min(column, line_length))
        
        if old_line != line or old_column != column:
            self._cursor_line = line
            self._cursor_column = column
            self._notify_cursor_changed()

    def move_cursor_to_line_start(self) -> None:
        self.set_cursor_position(self._cursor_line, 0)

    def move_cursor_to_line_end(self) -> None:
        line_length = len(self.get_current_line())
        self.set_cursor_position(self._cursor_line, max(0, line_length - 1))

    def move_cursor_word_forward(self) -> None:
        text = self.get_current_line()[self._cursor_column:]
        index = text.find(' ')
        if index != -1 and text[1] != ' ':
            self.set_cursor_position(self._cursor_line, self._cursor_column+index)
        elif index != -1 and text[1] == ' ':
            start = 0
            for i in range(1, len(text)):
                if (text[i] != ' '):
                    start = i
                    break
            text = text[start:]
            index = text.find(' ')
            if index != -1 and text[1] != ' ':
                self.set_cursor_position(self._cursor_line, self._cursor_column+index)
            elif index == -1:
                self.set_cursor_position(self._cursor_line, self._cursor_column+len(text)+ start - 1)
        elif index == -1:
            self.set_cursor_position(self._cursor_line, self._cursor_column+len(text))
            
    def move_cursor_word_backward(self) -> None:
        text = self.get_current_line()[:self._cursor_column]
        matches = list(re.finditer(r'\b\w', text))
        if matches:
            self.set_cursor_position(self._cursor_line, matches[-1].start())
        elif self._cursor_line > 0:
            self.set_cursor_position(self._cursor_line - 1, len(self.get_line(self._cursor_line - 1)) - 1)

    def insert_text(self, text: str) -> None:
        if text == '\b': 
            if self._cursor_column > 0:
                current_line = self.get_current_line()
                new_text = current_line[:self._cursor_column - 1] + current_line[self._cursor_column:]
                self._buffer.set_line(self._cursor_line, new_text)
                self.set_cursor_position(self._cursor_line, self._cursor_column - 1)
                self._modified = True
                self._notify_text_changed()
        else:
            current_line = self.get_current_line()
            new_text = current_line[:self._cursor_column] + text + current_line[self._cursor_column:]
            self._buffer.set_line(self._cursor_line, new_text)
            self.set_cursor_position(self._cursor_line, self._cursor_column + len(text))
            self._modified = True
            self._notify_text_changed()

    def delete_char(self) -> None:
        current_line = self.get_current_line()
        if self._cursor_column < len(current_line):
            new_text = current_line[:self._cursor_column] + current_line[self._cursor_column + 1:]
            self._buffer.set_line(self._cursor_line, new_text)
            self._modified = True
            self._notify_text_changed()

    def delete_line(self) -> None:
        self._yanked_text = self.get_current_line()
        self._buffer.delete_line(self._cursor_line)
        if self.get_line_count() == 0:
            self._buffer.insert_line(0)
        if self._cursor_line >= self.get_line_count():
            self.set_cursor_position(self.get_line_count() - 1, 0)
        self._modified = True
        self._notify_text_changed()

    def new_line(self) -> None:
        current_line = self.get_current_line()
        new_line = current_line[self._cursor_column:]
        self._buffer.set_line(self._cursor_line, current_line[:self._cursor_column])
        self._buffer.insert_line(self._cursor_line + 1, new_line)
        self.set_cursor_position(self._cursor_line + 1, 0)
        self._modified = True
        self._notify_text_changed()

    def delete_word(self) -> None:
        line = self.get_current_line()
        word_start = line.rfind(' ', 0, self._cursor_column) + 1
        word_end = line.find(' ', self._cursor_column)
        if word_end == -1:
            word_end = len(line)
        else:
            word_end += 1 
        
        new_text = line[:word_start] + line[word_end:]
        self._buffer.set_line(self._cursor_line, new_text)
        self.set_cursor_position(self._cursor_line, word_start)
        self._modified = True
        self._notify_text_changed()

    def replace_char(self, char: str) -> None:
        if len(char) == 1:
            current_line = self.get_current_line()
            if self._cursor_column < len(current_line):
                new_text = current_line[:self._cursor_column] + char + current_line[self._cursor_column + 1:]
                self._buffer.set_line(self._cursor_line, new_text)
                self._modified = True
                self._notify_text_changed()

    def yank_line(self) -> None:
        self._yanked_text = self.get_current_line()

    def yank_word(self) -> None:
        line = self.get_current_line()
        cursor_pos = self._cursor_column
        length = len(line)

        if cursor_pos >= length:
            self._yanked_text = ""
            return
        
        start = cursor_pos
        end = cursor_pos

        while start > 0 and line[start - 1].isalnum():
            start -= 1

        while end < length and line[end].isalnum():
            end += 1

        if start < end:
            self._yanked_text = line[start:end]
        else:
            self._yanked_text = ""

    def paste_after(self) -> None:
        if not self._yanked_text:
            return
        if '\n' in self._yanked_text:
            self._buffer.insert_line(self._cursor_line + 1, self._yanked_text.rstrip('\n'))
            self.set_cursor_position(self._cursor_line + 1, 0)
        else:
            self.insert_text(self._yanked_text)
        self._modified = True
        self._notify_text_changed()


    def load_file(self, filename: str) -> None:
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            print(lines)
            self._buffer.clear()
            if not lines:
                self._buffer.append_line("")
                self.set_cursor_position(0, 0)
            else:
                for line in lines:
                    self._buffer.append_line(line.rstrip('\n'))
                get_line = self.get_line_count()
                last_line = get_line - 1
                self.set_cursor_position(last_line, len(self.get_line(last_line)))
            self._filename = filename
            self._modified = False
            self._notify_text_changed()
            self._notify_file_changed()
        except Exception as e:
            self.set_mode("ERROR")
            self._notify_mode_changed()
    
    def save_file(self, filename: Optional[str] = None) -> None:
        save_filename = filename or self._filename
        if save_filename == "[No Name]":
            self.set_mode("Error")
            self._notify_mode_changed()
            return
        try:
            with open(save_filename, 'w') as f:
                for i in range(self._buffer.get_line_count()):
                    f.write(str(self._buffer.get_line(i)) + '\n')
            self._filename = save_filename
            self._modified = False
            self._notify_file_changed()
        except Exception as e:
            self.set_mode("Error")
            self._notify_mode_changed()
    
    def get_filename(self) -> str:
        return self._filename

    def is_modified(self) -> bool:
        return self._modified
    
    def get_mode(self) -> str:
        return self._mode

    def set_mode(self, mode: str) -> None:
        if mode != self._mode:
            self._mode = mode
            self._notify_mode_changed()

    def show_help(self) -> None: 
        help_text = """
Editor Commands:
--- Navigation -------------------------------------
RIGHT       - Move the cursor right by 1 position.
LEFT        - Move the cursor left by 1 position.
UP          - Move the cursor up by 1 line.
DOWN        - Move the cursor down by 1 line.
^ (or 0)    - Move the cursor to the beginning of the line.
$           - Move the cursor to the end of the line.
w           - Move to the end of the next word.
b           - Move to the beginning of the previous word.
gg          - Go to the beginning of the file.
G           - Go to the end of the file.
NG          - Go to line number N (e.g., 10G for line 10).
PG_UP       - Move one screen up.
PG_DOWN     - Move one screen down.
--- Editing ----------------------------------------
x           - Delete the character under the cursor.
diw         - Delete the word under the cursor, including the space to the right.
dd          - Cut the current line.
yy          - Copy the current line.
yw          - Copy the word under the cursor.
p           - Paste after the cursor.
r           - Replace one character under the cursor.
i           - Insert text before the cursor.
I           - Move to the beginning of the line and start inserting text.
A           - Move to the end of the line and start inserting text.
S           - Delete the contents of the line and start inserting text.
--- Search -----------------------------------------
/text<CR>   - Search for "text" from the cursor to the end of the file.
?text<CR>   - Search for "text" from the cursor to the beginning of the file.
n           - Repeat the search.
N           - Repeat the search in the reverse direction.
--- File Operations ---
:o filename - Open the file "filename".
:w          - Save the current file.
:w filename - Save to "filename".
:q          - Quit (if no changes were made).
:q!         - Quit without saving.
:wq         - Save and quit.
:wq!        - Save and quit forcefully.
--- Miscellaneous ----------------------------------
number      - Go to line "number".
h           - Display help for commands.
"""
        lines = help_text.split('\n')
        self._buffer.clear()
        for line in lines:
            self._buffer.append_line(line.rstrip('\n'))
        last_line = self.get_line_count() - 1
        self.set_cursor_position(last_line, len(self.get_line(last_line)))
        self._filename = "Help"
        self._modified = False
        self._notify_text_changed()
        self._notify_file_changed()

  
    
    def _perform_search(self, text: str, forward: bool = True) -> None:
        if not text:
            return

        current_line, current_col = self.get_cursor_position()
        start_line = current_line
        
        if forward:
            # Search forward
            for line in range(current_line, self.get_line_count()):
                line_text = self.get_line(line)
                start_col = current_col + 1 if line == current_line else 0
                pos = line_text.find(text, start_col)
                if pos != -1:
                    self._move_cursor(line=line, column=pos)
                    return
            
            for line in range(0, start_line):
                line_text = self.get_line(line)
                pos = line_text.find(text)
                if pos != -1:
                    self._move_cursor(line=line, column=pos)
                    return
        else:
            for line in range(current_line, -1, -1):
                line_text = self.get_line(line)
                end_col = current_col if line == current_line else len(line_text)
                pos = line_text.rfind(text, 0, end_col)
                if pos != -1:
                    self._move_cursor(line=line, column=pos)
                    return
            for line in range(self.get_line_count() - 1, start_line, -1):
                line_text = self.get_line(line)
                pos = line_text.rfind(text)
                if pos != -1:
                    self._move_cursor(line=line, column=pos)
                    return
                
    def _move_cursor(self, line: Optional[int] = None, column: Optional[int] = None) -> None:
        current_line, current_col = self.get_cursor_position()
        new_line = line if line is not None else current_line
        new_col = column if column is not None else current_col
        self.set_cursor_position(new_line, new_col)

    def repeat_last_search(self, forward: bool = True) -> bool:
        print("ZASHEL")
        if self._last_search:
            print(f"last search: {self._last_search}")
            self._perform_search(self._last_search, forward if self._last_search_forward else not forward)
        
    def delete_file(self, filename: str) -> None:
        os.re(filename)