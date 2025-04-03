import curses
from typing import Tuple
from interfaces.i_displayAdapter import IDisplayAdapter
class CursesAdapter(IDisplayAdapter):
    def __init__(self):
        self._screen = None
        self._max_y = 0
        self._max_x = 0

    def init(self) -> None:
        self._screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        self._screen.keypad(True)
        self._max_y, self._max_x = self._screen.getmaxyx()
        
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Normal text
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Status line

    def cleanup(self) -> None:
        if self._screen:
            self._screen.keypad(False)
            curses.echo()
            curses.nocbreak()
            curses.endwin()

    def get_key(self) -> str:
        try:
            key = self._screen.getch()
            if key == 27:  # ESC key
                return 'ESC'
            elif key == curses.KEY_LEFT:
                return 'LEFT'
            elif key == curses.KEY_RIGHT:
                return 'RIGHT'
            elif key == curses.KEY_UP:
                return 'UP'
            elif key == curses.KEY_DOWN:
                return 'DOWN'
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                return 'ENTER'
            elif key == curses.KEY_BACKSPACE or key == 127 or key == 8:
                return 'BACKSPACE'
            elif key == curses.KEY_DC:
                return 'DELETE'
            elif key == curses.KEY_PPAGE:
                return 'PG_UP'
            elif key == curses.KEY_NPAGE:
                return 'PG_DOWN'
            elif 32 <= key <= 126:
                return chr(key)
            return ''
        except:
            return ''

    def clear(self) -> None:
        self._screen.clear()

    def refresh(self) -> None:
        self._screen.refresh()

    def get_window_size(self) -> tuple[int, int]:
        return self._max_y, self._max_x

    def move_cursor(self, y: int, x: int) -> None:
        try:
            self._screen.move(min(y, self._max_y - 1), min(x, self._max_x - 1))
        except curses.error:
            pass

    def write_line(self, y: int, x: int, text: str, attr=None) -> None:
        if attr is None:
            attr = curses.color_pair(1)
        try:
            self._screen.addstr(y, x, text[:self._max_x - x], attr)
        except curses.error:
            pass

    def write_status_line(self, text: str, attr=None) -> None:
        if attr is None:
            attr = curses.color_pair(2)
        try:
            self._screen.addstr(self._max_y - 1, 0, text[:self._max_x], attr)
        except curses.error:
            pass