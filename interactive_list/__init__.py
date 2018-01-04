from sys import platform

if platform.startswith('linux') or platform == 'darwin':
    from .interactive_list_curses import interactive_list as interactive_list_curses

from .interactive_list import interactive_list
