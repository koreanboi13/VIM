from controller.editor.base_mode_handler import BaseModeHandler
from interfaces.i_model import IModel
from interfaces.i_view import IView
from interfaces.editor.i_movement_controller import IMovementController
from interfaces.editor.i_command_executor import ICommandExecutor
from typing import Optional
class InsertModeHandler(BaseModeHandler):
    def __init__(self, 
                 model: IModel, 
                 view: IView,
                 command_executor: ICommandExecutor):
        super().__init__(model, view, command_executor)
        self._movement_keys = {
            'LEFT': lambda: self._move_cursor(column=max(0, self._model.get_cursor_position()[1] - 1)),
            'RIGHT': lambda: self._move_cursor(column=min(len(self._model.get_current_line()), self._model.get_cursor_position()[1] + 1)),
            'UP': self._move_up,
            'DOWN': self._move_down
        }

    def handle_mode(self, key: str) -> bool:
        if key == 'ESC':
            self._exit_insert_mode()
            return True
        if key == 'BACKSPACE':
            if self._model.get_cursor_position()[1] > 0:
                self._model.insert_text('\b')
        if key in ['LEFT', 'RIGHT', 'UP', 'DOWN', 'BACKSPACE', 'ENTER', 'DELETE']:
            if key == 'ENTER':
                self._model.new_line()
            elif key == 'DELETE':
                self._model.delete_char()
            elif key in self._movement_keys:
                self._movement_keys[key]()
        else:
            self._model.insert_text(key)
        return True
    
    def _move_cursor(self, line: Optional[int] = None, column: Optional[int] = None) -> None:
        current_line, current_col = self._model.get_cursor_position()
        new_line = line if line is not None else current_line
        new_col = column if column is not None else current_col
        self._model.set_cursor_position(new_line, new_col)

    def _exit_insert_mode(self) -> bool:
        self._model.set_mode("NORMAL")
        line,col = self._model.get_cursor_position()
        if col > 0:
            self._model.set_cursor_position(line=line,column=col - 1)
        return True

    def _move_up(self) -> None:
        line, col = self._model.get_cursor_position()
        if line > 0:
            self._model.set_cursor_position(line=line - 1,column=col)

    def _move_down(self) -> None:
        line, col = self._model.get_cursor_position()
        if line < self._model.get_line_count() - 1:
            self._model.set_cursor_position(line=line + 1,column=col)


   
