import curses, os
from .interactive_list import cutsmart, ceil, regex_comp

def interactive_list_main(data):
    if type(data) != dict:
        raise TypeError('Function requires dictionary argument')
    for i in data:
        if type(data[i]) != str:
            raise TypeError('Function requires dictionary of string elements')

    results = [[i for i in data]]

    max_line = 0
    for i in data:
        if len(data[i]) > max_line: max_line = len(data[i])

    os.environ.setdefault('ESCDELAY', '5')

    curses.initscr()
    curses.noecho()
    curses.curs_set(False)

    pad = curses.newpad(len(data), max_line)
    for l in range(0, len(results[-1])):
        pad.addstr(l,0, data[results[-1][l]])
    pad.keypad(True)

    search = curses.newpad(2, 200)
    search.addstr(0,0, '--------')

    ghost = curses.newpad(1000, 1000)
    for l in range(0, 1000):
        ghost.addstr(l,0, ' '*999)

    s, regex, op = '', regex_comp(''), 0
    y = 0
    refill, search_upd = False, False
    search.addstr(1,0, f'Search: ')

    while True:
        if refill:
            pad.clear()
            pad.erase()
            for l in range(0, len(results[-1])):
                el = data[results[-1][l]]
                pad.addstr(l,0, el)
        refill = False

        if search_upd:
            search.deleteln()
            search.addstr(1,0, f'Search: {s}')
        search_upd = False

        cols, rows = os.get_terminal_size()
        if curses.is_term_resized(rows, cols):
            curses.resizeterm(rows, cols)
            pad.getch()
        ghost.refresh(0,0, 0,0, rows-1,cols-1)
        pad.refresh(y,0, 0,0, rows-2,cols-1)
        search.refresh(0,0, rows-2,0, rows-1,cols-1)

        c = pad.getch()

        if c == 127:
            s = s[0:-1]
            regex = regex_comp(s)
            if op == 0: op = 'rem'
            search_upd = True
        elif c <= 126 and c >= 32:
            s += chr(c)
            regex = regex_comp(s)
            if op == 0: op = 'add'
            if op == 'rem': op = 'redo'
            search_upd = True
        elif c == 27:
            return_data = None
            break
        elif c == 10:
            if len(results[-1]) > 0 and all(data[i] == data[results[-1][0]] for i in results[-1]):
                return_data = results[-1]
                break
        elif c == 259:
            y -= rows-2
            if y < 0: y = 0
        elif c == 258:
            y += rows-2
            if y+rows-2 > len(results[-1]):
                y = len(results[-1])-(rows-2)
                if y < 0: y = 0

        if not regex:
            continue

        elif op == 'add':
            results.append([i for i in results[-1] if regex.search(data[i])])
            y = 0
            refill= True
        elif op == 'rem':
            if len(results) > 1:
                results = results[0:-1]
                y = 0
                refill= True
        elif op == 'redo':
            if len(results) > 1:
                results = results[0:-1]
            results.append([i for i in results[-1] if regex.search(data[i])])
            y = 0
            refill= True
        op = 0

    pad.clear() ; pad.erase()
    search.clear() ; search.erase()
    curses.endwin()

    return return_data

def interactive_list(data):
    try:
        return interactive_list_main(data)
    except:
        raise
    finally:
        try:
            curses.endwin()
        except:
            pass
