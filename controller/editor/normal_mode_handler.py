from controller.editor.base_mode_handler import BaseModeHandler
from interfaces.i_model import IModel
from interfaces.i_view import IView
from interfaces.editor.i_movement_controller import IMovementController
from interfaces.editor.i_command_executor import ICommandExecutor
from typing import Dict, Callable, Optional
from view.curses_view import CursesView

class NormalModeHandler(BaseModeHandler):
    def __init__(self, 
                 model: IModel, 
                 view: IView,
                 command_executor: ICommandExecutor):
        super().__init__(model, view, command_executor)
        self._command_buffer = ""
        self._pending_command = ""
        self._command_handlers = self._init_command_handlers()
        self._movement_keys = {
            'LEFT': lambda: self._move_cursor(column=max(0, self._model.get_cursor_position()[1] - 1)),
            'RIGHT': lambda: self._move_cursor(column=min(len(self._model.get_current_line()), self._model.get_cursor_position()[1] + 1)),
            'UP': lambda: self._move_cursor_vertical(-1),
            'DOWN': lambda: self._move_cursor_vertical(1),
            'PG_UP': self._page_up,
            'PG_DOWN': self._page_down
        }

    def _init_command_handlers(self) -> Dict[str, Callable[[], None]]:
        return {
            'i': self._enter_insert_mode,
            'I': self._insert_start_of_line,
            'A': self._append_end_of_line,
            'S': self._clear_line_and_insert,
            'x': self._delete_char,
            'dd': self._delete_line,
            'yy': self._yank_line,
            'yw': self._yank_word,
            'r': self._replace_char,
            'p': self._paste_after,
            'diw': self._delete_inner_word,
            '0': self._model.move_cursor_to_line_start,
            '^': self._model.move_cursor_to_line_start,
            '$': self._model.move_cursor_to_line_end,
            'w': self._model.move_cursor_word_forward,
            'b': self._model.move_cursor_word_backward,
            'gg': lambda: self._model.set_cursor_position(line=0, column=0),
            'G': self._move_to_last_line,
            'n': lambda: self._model.repeat_last_search(forward=True),
            'N': lambda: self._model.repeat_last_search(forward=False)
        }

    def handle_mode(self, key: str) -> bool:
        if self._pending_command:
            full_command = self._pending_command + key
            if full_command in self._command_handlers:
                self._command_handlers[full_command]()
                self._pending_command = ""
                return True
            elif any(cmd.startswith(full_command) for cmd in self._command_handlers.keys()):
                self._pending_command = full_command
                return True
            self._pending_command = ""
            return True

        potential_commands = [cmd for cmd in self._command_handlers.keys() if cmd.startswith(key)]
        if potential_commands:
            if len(potential_commands[0]) > 1: 
                self._pending_command = key
                return True
        
        if key in self._movement_keys:
            self._movement_keys[key]()
            return True

        if key == ':':
            self._model.set_mode("COMMAND")
            self._command_buffer = ":"
            if isinstance(self._view, CursesView):
                self._view.set_command_buffer(self._command_buffer)
            return True
        elif key == '/':
            self._model.set_mode("SEARCH")
            self._model.set_search_buffer("/")
            if isinstance(self._view, CursesView):
                self._view.set_search_buffer(self._model.get_search_buffer())
            return True
        elif key == '?':
            self._model.set_mode("SEARCH")
            self._model.set_search_buffer("?")
            if isinstance(self._view, CursesView):
                self._view.set_search_buffer(self._model.get_search_buffer())
            return True
        elif key.isdigit() and key != '0': 
            self._command_buffer = key
            return True
        elif key in 'G' and self._command_buffer: 
            try:
                line_num = int(self._command_buffer) - 1
                self._move_cursor(line=min(line_num, self._model.get_line_count() - 1))
            except ValueError:
                pass
            self._command_buffer = ""
            return True
        elif key in self._command_handlers:
            self._command_handlers[key]()
            return True
        return True
    
    def _move_cursor(self, line: Optional[int] = None, column: Optional[int] = None) -> None:
        current_line, current_col = self._model.get_cursor_position()
        new_line = line if line is not None else current_line
        new_col = column if column is not None else current_col
        self._model.set_cursor_position(new_line, new_col)

    def _move_cursor_vertical(self, delta: int) -> None:
        current_line, current_col = self._model.get_cursor_position()
        new_line = max(0, min(self._model.get_line_count() - 1, current_line + delta))
        new_line_length = len(self._model.get_line(new_line))
        new_col = min(current_col, new_line_length)
        self._move_cursor(line=new_line, column=new_col)


    def _page_up(self) -> None:
        current_line = self._model.get_cursor_position()[0]
        self._move_cursor_vertical(-20)

    def _page_down(self) -> None:
        current_line = self._model.get_cursor_position()[0]
        self._move_cursor_vertical(20)


    def _move_to_last_line(self) -> None:
        if self._command_buffer:
            try:
                line_num = int(self._command_buffer) - 1
                self._move_cursor(line=min(line_num, self._model.get_line_count() - 1))
            except ValueError:
                pass
            self._command_buffer = ""
        else:
            self._move_cursor(line=self._model.get_line_count() - 1)

    def _enter_insert_mode(self) -> None:
        self._model.set_mode("INSERT")

    def _insert_start_of_line(self) -> None:
        self._model.move_cursor_to_line_start()
        self._model.set_mode("INSERT")

    def _append_end_of_line(self) -> None:
        self._model.move_cursor_to_line_end()
        self._model.set_mode("INSERT")

    def _clear_line_and_insert(self) -> None:
        self._delete_line()
        self._model.move_cursor_to_line_start()
        self._model.set_mode("INSERT")

    def _delete_char(self) -> None:
        self._model.delete_char()

    def _delete_line(self) -> None:
        self._model.move_cursor_to_line_start()
        self._model.delete_line()

    def _yank_line(self) -> None:
        self._model.yank_line()

    def _delete_inner_word(self) -> None:
        self._model.delete_word()

    def _paste_after(self) -> None:
        self._model.paste_after()
        
    def _replace_char(self) -> None:
        key = self._view.get_input()
        if key and len(key) == 1:
            self._delete_char()
            self._model.insert_text(key)

    def _yank_word(self) -> None:
        self._model.yank_word()