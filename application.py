from model.editor_model import EditorModel
from view.curses_view import CursesView
from controller.editor.base_controller import BaseController
from controller.editor.command_executor import CommandExecutor
from controller.editor.input_handler import InputHandler
from controller.editor.normal_mode_handler import NormalModeHandler
from controller.editor.insert_mode_handler import InsertModeHandler
from controller.editor.command_mode_handler import CommandModeHandler
from controller.editor.search_mode_handler import SearchModeHandler
from controller.editor.help_mode_handler import HelpModeHandler
from interfaces.i_model import IModel
from interfaces.i_view import IView
from interfaces.i_controller import IController

class Application:
    def __init__(self):
        self._model: IModel = EditorModel()
        self._view: IView = CursesView()
        
        command_executor = CommandExecutor(self._model, self._view)
        
        mode_handlers = {
            "NORMAL": NormalModeHandler(self._model, self._view, command_executor),
            "INSERT": InsertModeHandler(self._model, self._view, command_executor),
            "COMMAND": CommandModeHandler(self._model, self._view, command_executor),
            "SEARCH": SearchModeHandler(self._model, self._view, command_executor),
            "HELP": HelpModeHandler(self._model, self._view, command_executor)
        }
        
        input_handler = InputHandler(self._model,mode_handlers)
        
        self._controller: IController = BaseController(
            self._model,
            self._view,
            input_handler,
            command_executor
        )
        
        if isinstance(self._view, CursesView):
            self._view.set_model(self._model)

    def run(self, filename: str = None) -> None:
        try:
            self._controller.start()
            if filename:
                self._model.load_file(filename)

            while True:
                key = self._view.get_input()
                if key and not self._controller.handle_input(key):
                    break

        finally:
            self._controller.stop()