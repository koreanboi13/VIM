from abc import ABC
import curses
from typing import Optional, Dict, List
from interfaces.i_view import IView
from interfaces.i_model import IModel
from interfaces.i_modelObs import IModelObserver
from view.curses_adapter import CursesAdapter

class CursesView(IView, IModelObserver):
    
    def __init__(self):
        self._adapter = CursesAdapter()
        self._top_line = 0
        self._current_line = 0
        self._current_column = 0
        self._mode = "NORMAL"
        self._filename = "[No Name]"
        self._model: Optional[IModel] = None
        self._command_buffer = ""
        self._search_buffer = ""

    def set_model(self, model: IModel) -> None:
        if self._model:
            self._model.remove_observer(self)
        self._model = model
        if self._model:
            self._model.add_observer(self)

    def init(self) -> None:
        self._adapter.init()
        self._refresh_screen()

    def cleanup(self) -> None:
        if self._model:
            self._model.remove_observer(self)
        self._adapter.cleanup()

    def get_input(self) -> Optional[str]:
        return self._adapter.get_key()

    def set_command_buffer(self, buffer: str) -> None:
        self._command_buffer = buffer
        self._refresh_screen()

    def set_search_buffer(self, buffer: str) -> None:
        self._search_buffer = buffer
        self._refresh_screen()

    def display_error(self, message: str) -> None:
        self._adapter.write_status_line(f"Error: {message}", curses.color_pair(2) | curses.A_BOLD)
        self._adapter.refresh()
        curses.napms(2000)
        self._refresh_screen()

    def display_info(self, message: str) -> None:
        self._adapter.write_status_line(message)
        self._adapter.refresh()
        curses.napms(1000) 
        self._refresh_screen()

    def _refresh_screen(self) -> None:
        if not self._model:
            return

        self._adapter.clear()
        self._render_content()
        self._render_status_line()
        self._update_cursor()
        self._adapter.refresh()


    def _render_content(self) -> None:
        if not self._model:
            return
            
        max_y, max_x = self._adapter.get_window_size()
        content_height = max_y - 1 
        
        if self._current_line < self._top_line:
            self._top_line = self._current_line
        elif self._current_line >= self._top_line + content_height:
            self._top_line = self._current_line - content_height +1

        for i in range(content_height):
            screen_y = i
            buffer_line = self._top_line + i
            
            if buffer_line < self._model.get_line_count():
                line = self._model.get_line(buffer_line)
                if len(line) > max_x:
                    line = line[:max_x-1] + '>'
                self._adapter.write_line(screen_y, 0, line)
            else:
                self._adapter.write_line(screen_y, 0, "")
   
    def _render_status_line(self) -> None:
        if not self._model:
            return
            
        line_count = self._model.get_line_count()
        mode = self._mode
        
        if mode == "COMMAND" and self._command_buffer:
            status = self._command_buffer
        elif mode == "SEARCH" and self._search_buffer:
            status = self._search_buffer
        elif mode == "ERROR":
            status = "Error!"
        else:
            status = f"{mode} | {self._filename} | Line {self._current_line + 1} of {line_count}"
        self._adapter.write_status_line(status)

    def _update_cursor(self) -> None:
        screen_y = self._current_line - self._top_line
        screen_x = self._current_column
        self._adapter.move_cursor(screen_y, screen_x)

    def on_text_changed(self) -> None:
        self._refresh_screen()

    def on_cursor_changed(self, line: int, column: int) -> None:
        self._current_line = line
        self._current_column = column
        self._refresh_screen()

    def on_mode_changed(self, mode: str) -> None:
        self._mode = mode
        self._refresh_screen()

    def on_file_changed(self, filename: str) -> None:
        self._filename = filename
        self._refresh_screen()
