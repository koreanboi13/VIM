# VIM-редактор

Консольный текстовый редактор, реализующий основные функции и режимы работы редактора VIM. Проект выполнен с использованием архитектурного паттерна MVC.

## Описание

Этот проект представляет собой легковесный текстовый редактор, работающий в консоли и вдохновленный редактором VIM. Он поддерживает различные режимы работы и основные команды VIM, что делает его удобным инструментом для работы с текстом в терминале.

## Особенности

- **Поддержка различных режимов работы**:
  - Нормальный режим (NORMAL)
  - Режим вставки (INSERT)
  - Командный режим (COMMAND)
  - Режим поиска (SEARCH)
  - Режим справки (HELP)
  
- **Основные функции**:
  - Навигация по тексту
  - Редактирование текста
  - Поиск в тексте
  - Работа с файлами (открытие, сохранение)
  - Отмена/повтор действий


## Архитектура

Проект реализован с использованием паттерна MVC:

- **Модель (model)**: Отвечает за хранение и обработку данных текстового буфера
- **Представление (view)**: Реализует интерфейс пользователя через curses
- **Контроллер (controller)**: Обрабатывает ввод пользователя и управляет режимами работы

## Требования

- Python 3.6 или выше
- Библиотека curses (встроена в Python для Unix/Linux/macOS, для Windows требуется установка windows-curses)


## Использование

```bash
# Запуск редактора
python main.py

# Открытие файла
python main.py путь/к/файлу.txt
```

## Основные команды

### Нормальный режим
-  клавиши со стрелками - навигация (влево, вниз, вверх, вправо)
- `i` - переключение в режим вставки
- `I` - переход к началу строки и переключение в режим вставки
- `A` - переход к концу строки и переключение в режим вставки
- `S` - очистка текущей строки и переключение в режим вставки
- `:` - переключение в командный режим
- `/` - переключение в режим поиска (вперед)
- `?` - переключение в режим поиска (назад)
- `n` - повторить последний поиск вперед
- `N` - повторить последний поиск назад
- `x` - удалить символ под курсором
- `dd` - удалить текущую строку
- `yy` - скопировать текущую строку
- `yw` - скопировать слово
- `p` - вставить скопированный текст
- `diw` - удалить слово под курсором
- `0` или `^` - переход к началу строки
- `$` - переход к концу строки
- `w` - переход к началу следующего слова
- `b` - переход к началу предыдущего слова
- `gg` - переход в начало документа
- `G` - переход в конец документа
- `r` - заменить символ под курсором
- `[число]G` - переход к указанной строке

### Режим вставки
- `Esc` - возврат в нормальный режим
- Клавиши со стрелками - навигация в режиме вставки
- `Enter` - создание новой строки
- `Backspace` - удаление символа перед курсором
- `Delete` - удаление символа под курсором

### Командный режим
- `w` - сохранить файл
- `q` - выйти из редактора
- `q!` - принудительный выход без сохранения
- `wq` или `x` - сохранить и выйти
- `wq!` - принудительно сохранить и выйти
- `h` - показать справку
- `o [имя_файла]` - открыть файл
- `[число]` - переход к указанной строке


### Режим справки
- `Esc` - выход из режима справки и возврат к редактированию
- Клавиши со стрелками - навигация по справке

## Структура проекта

```
.
├── main.py                    # Точка входа в приложение
├── application.py             # Основной класс приложения, связывающий MVC
├── model/                     # Компоненты модели
│   ├── editor_model.py        # Основная модель редактора
│   ├── buffer.py              # Класс для работы с текстовым буфером
│   └── MyString.pyd           # Бинарный модуль для работы со строками
├── view/                      # Компоненты представления
│   ├── curses_view.py         # Представление на основе curses
│   └── curses_adapter.py      # Адаптер для работы с curses
├── controller/                # Компоненты контроллера
│   └── editor/                # Контроллеры редактора
│       ├── base_controller.py         # Базовый контроллер
│       ├── base_mode_handler.py       # Базовый обработчик режимов
│       ├── command_executor.py        # Исполнитель команд
│       ├── command_mode_handler.py    # Обработчик командного режима
│       ├── help_mode_handler.py       # Обработчик режима справки
│       ├── input_handler.py           # Обработчик ввода
│       ├── insert_mode_handler.py     # Обработчик режима вставки
│       ├── normal_mode_handler.py     # Обработчик нормального режима
│       └── search_mode_handler.py     # Обработчик режима поиска
└── interfaces/                # Интерфейсы для обеспечения слабого связывания
    ├── i_controller.py        # Интерфейс контроллера
    ├── i_model.py             # Интерфейс модели
    ├── i_view.py              # Интерфейс представления
    ├── i_modelObs.py          # Интерфейс наблюдателя модели
    ├── i_displayAdapter.py    # Интерфейс адаптера отображения
    └── editor/                # Интерфейсы специфичные для редактора
        ├── i_command_executor.py      # Интерфейс исполнителя команд
        ├── i_input_handler.py         # Интерфейс обработчика ввода
        ├── i_mode_handler.py          # Интерфейс обработчика режимов
        └── i_movement_controller.py   # Интерфейс контроллера перемещения
```