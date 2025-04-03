from interfaces.editor.i_command_executor import ICommandExecutor
from interfaces.i_model import IModel
from interfaces.i_view import IView
from typing import Dict, Callable, Optional
import os

class CommandExecutor(ICommandExecutor):
    def __init__(self, model: IModel, view: IView):
        self._model = model
        self._view = view
        self._commands: Dict[str, Callable] = {}
        self._init_default_commands()

    def _init_default_commands(self) -> None:
        self._commands.update({
            'w': self._save_file,
            'q': self._quit,
            'wq': self._save_and_quit,
            'h': self._model.show_help
        })
    def _enter_help_mode(self) -> None:
        self._model.set_mode("HELP")
        self._model.show_help()
    def execute_command(self, command: str) -> bool:
        if not command:
            return True

        if command.isdigit():
            line_num = int(command) - 1
            self._move_cursor(line=min(line_num, self._model.get_line_count() - 1))
            return True
        
        parts = command.split()
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []

        if cmd == 'w':
            if args:
                self._model.save_file(args[0])
            else:
                self._model.save_file()
        elif cmd == 'q':
            if self._model.is_modified() and not command.endswith('!'):
                return True 
            return False  
        elif cmd == 'q!':
            return False 
        elif cmd == 'wq!':
            if self._model.is_modified():
                self._model.save_file()
            return False 
        
        elif cmd == 'h':
            self._tmp_filename = self._model.get_filename()
            if (self._tmp_filename == "[No Name]"):
                self._model.set_tmp_filename("tmp.txt")
            else:
                self._model.set_tmp_filename(self._tmp_filename)
            self._model.save_file(filename=self._tmp_filename)
            self._enter_help_mode()

        elif cmd == 'o' and args:
            self._model.load_file(args[0])
        elif cmd == 'x':
            self._model.save_file()
            return False 

        return True
    def register_command(self, command: str, handler: Callable) -> None:
        self._commands[command] = handler

    def _save_file(self, filename: str = None) -> bool:
        if filename:
            self._model.save_file(filename)
        else:
            current_file = self._model.get_filename()
            if current_file:
                self._model.save_file(current_file)
            else:
                return False
        return True

    def _quit(self) -> bool:
        self._model.set_running(False)
        return True
    def _move_cursor(self, line: Optional[int] = None, column: Optional[int] = None) -> None:
            current_line, current_col = self._model.get_cursor_position()
            new_line = line if line is not None else current_line
            new_col = column if column is not None else current_col
            self._model.set_cursor_position(new_line, new_col)
    def _save_and_quit(self, filename: str = None) -> bool:
        return self._save_file(filename) and self._quit()
