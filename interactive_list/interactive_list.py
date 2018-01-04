import sqlite3
import re
import os

try:
    import readkeys
    read_fn = readkeys.getkey
except:
    import readchar
    read_fn = readchar.readkey
    print('Missing readkeys module, some features might not work properly')

def dellines(n=0):
    if n < 0: return
    print('\r\033[2K', end='')
    if n == 0: return
    print('\033[1A\r\033[2K'*n, end='')

def cutsmart(s, n):
    i = 0
    sf = ''
    while i <= n and i < len(s):
        if s[i] == '\x1b':
            sf += s[i:i+4]
            i+=4
            n+=4
            continue
        sf += s[i]
        i+=1
    return sf

def ceil(n):
    n_int = n//1
    if n > n_int: n_int += 1
    return int(n_int)

def regex_comp(s):
    try:
        if re.search('[A-Z]', s):
            return re.compile(rf'{s}')
        else:
            return re.compile(rf'{s}', flags=re.IGNORECASE)
    except:
        return None

def read_op(s, regex):
    so = s
    op = 0
    
    while True:
        c = read_fn()

        if c in ('\x1b', '\x1b\x1b'):
            return s, regex, 'exit'
        elif c in ('\r', '\n'):
            return s, regex, 'sel'
        elif c == '\x7f':
            if len(s) == 0:
                continue
            s = s[0:-1]
            print('\b \b', end='', flush=True)
            regex = regex_comp(s)
            if op == 0: op = 'rem'
            if not regex:
                continue
        elif re.search('^[^\x00-\x1f]$', c):
            s += c
            print(c,  end='', flush=True)
            regex = regex_comp(s)
            if op == 0: op = 'add'
            if op == 'rem': op = 'redo'
            if not regex:
                continue
        elif c == '\x1b[A':
            return s, regex, 'up'
        elif c == '\x1b[B':
            return s, regex, 'dw'
        else:
            continue

        if s == so:
            continue
        return s, regex, op

def interactive_list(data):
    if type(data) != dict:
        raise TypeError('Function requires dictionary argument')
    results = [[i for i in data]]
    s = ''
    regex = regex_comp(s)
    op = ''
    pos = 0

    while True:
        l = len(results[-1])
        cols, rows = os.get_terminal_size()
        if l > rows - 4: l = rows - 4

        for i in results[-1][pos:pos+l]:
            el = regex.sub("\033[1m\g<0>\033[0m", data[i])
            print(cutsmart(el,cols-1), end='\033[0m\n')
        if l:
            page_t = ceil(len(results[-1])/l)
            page_i = ceil(pos/l) + 1
        else:
            page_t, page_i = 0, 0
        print()
        if page_t > 1:
            print(f'{page_i}/{page_t} ', end='')
        print(f'{len(results[-1])} results')
        print(f'--------')
        print(f'Search: {s}', end='', flush=True)

        s, regex, op = read_op(s, regex)

        if op == 'exit':
            dellines(l+3)
            return None
        elif op == 'sel':
            if l > 0 and all(data[i] == data[results[-1][0]] for i in results[-1]):
                dellines(l+3)
                return results[-1]
        elif op == 'add':
            results.append([i for i in results[-1] if regex.search(data[i])])
            pos = 0
        elif op == 'rem':
            if len(results) > 1:
                results = results[0:-1]
            pos = 0
        elif op == 'redo':
            if len(results) > 1:
                results = results[0:-1]
            results.append([i for i in results[-1] if regex.search(data[i])])
            pos = 0
        elif op == 'dw':
            if pos+l < len(results[-1]):
                pos += l
        elif op == 'up':
            if pos > 0:
                pos -= l
                if pos < 0:
                    pos = 0

        dellines(l+3)
