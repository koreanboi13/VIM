from controller.editor.base_mode_handler import BaseModeHandler
from interfaces.i_model import IModel
from interfaces.i_view import IView
from interfaces.editor.i_movement_controller import IMovementController
from interfaces.editor.i_command_executor import ICommandExecutor
from view.curses_view import CursesView
import re

class SearchModeHandler(BaseModeHandler):
    def __init__(self, 
                 model: IModel, 
                 view: IView,
                 command_executor: ICommandExecutor):
        super().__init__(model, view,  command_executor)
        self._search_buffer = ""
        self._last_search = ""
        self._last_search_forward = True

    def handle_mode(self, key: str) -> bool:
        if key == 'ESC':
            self._model.set_mode("NORMAL")
            self._model.clear_search_buffer()
            if isinstance(self._view, CursesView):
                self._view.set_search_buffer("")
            return True
        elif key == 'ENTER':
            search_type = self._model.get_search_buffer()
            search_text = self._search_buffer
            if search_text:
                self._model.set_last_search(search_text)
                if(search_type == '/'):
                    self._model.set_last_search_forward(True)
                    self._model._perform_search(search_text,True)
                else:
                    self._model.set_last_search_forward(False)
                    self._model._perform_search(search_text,False)
                    
            self._model.clear_search_buffer()
            self._search_buffer = ""
            if isinstance(self._view, CursesView):
                self._view.set_search_buffer("")
            self._model.set_mode("NORMAL")
            return True
        elif key == 'BACKSPACE':
            if len(self._search_buffer) >=1:
                self._search_buffer = self._search_buffer[:-1]
                
                if isinstance(self._view, CursesView):
                    self._view.set_search_buffer(self._model.get_search_buffer()+self._search_buffer)
            return True
        else:
            if key not in ['LEFT', 'RIGHT', 'UP', 'DOWN', 'DELETE']:
                self._search_buffer += key
                
                if isinstance(self._view, CursesView):
                    self._view.set_search_buffer(self._model.get_search_buffer() + self._search_buffer)
            return True
