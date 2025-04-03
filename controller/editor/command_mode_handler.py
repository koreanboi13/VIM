from controller.editor.base_mode_handler import BaseModeHandler
from interfaces.i_model import IModel
from interfaces.i_view import IView
from interfaces.editor.i_movement_controller import IMovementController
from interfaces.editor.i_command_executor import ICommandExecutor
from view.curses_view import CursesView

class CommandModeHandler(BaseModeHandler):
    def __init__(self, 
                 model: IModel, 
                 view: IView,
                 command_executor: ICommandExecutor):
        super().__init__(model, view, command_executor)
        self._command_buffer = ":"

    def handle_mode(self, key: str) -> bool:
        if key == 'ESC':
            self._exit_command_mode()
            return True
        elif key == 'ENTER':
            result = self._command_executor.execute_command(self._command_buffer[1:])  # Remove the leading ':'
            self._command_buffer = ":"
            if isinstance(self._view, CursesView):
                self._view.set_command_buffer("")
            if self._model.get_mode() == "HELP":
                return result
            else:
                self._model.set_mode("NORMAL")
                return result
        elif key == 'BACKSPACE':
            if len(self._command_buffer) > 1:
                self._command_buffer = self._command_buffer[:-1]
                if isinstance(self._view, CursesView):
                    self._view.set_command_buffer(self._command_buffer)
            return True
        else:
            if key not in ['LEFT', 'RIGHT', 'UP', 'DOWN', 'DELETE']:
                self._command_buffer += key
                if isinstance(self._view, CursesView):
                    self._view.set_command_buffer(self._command_buffer)
            return True

    def enter_mode(self) -> None:
        self._command_buffer = ":"
        if isinstance(self._view, CursesView):
            self._view.set_command_buffer(self._command_buffer)

    def exit_mode(self) -> None:
        self._command_buffer = ":"
        if isinstance(self._view, CursesView):
            self._view.set_command_buffer("")

    def _exit_command_mode(self) -> bool:
        self._model.set_mode("NORMAL")
        self.exit_mode()
        return True