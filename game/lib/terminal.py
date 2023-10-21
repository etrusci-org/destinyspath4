import os
import sys
import subprocess




__all__ = [
    'clear_terminal',
    'disable_terminal_cursor',
    'enable_terminal_cursor',
]




# Thanks to James Spencer for the 'nt' part in the code below


if os.name == 'nt':
    import msvcrt
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [
            ('size', ctypes.c_int),
            ('visible', ctypes.c_byte),
        ]


def clear_terminal() -> None:
    if os.name == 'posix':
        subprocess.run(['clear'], shell=True)
    elif os.name == 'nt':
        subprocess.run(['cls'], shell=True)
    else:
        print('\033c', end='')


def disable_terminal_cursor() -> None:
    if os.name == 'posix':
        sys.stdout.write('\033[?25l')
        sys.stdout.flush()

    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))


def enable_terminal_cursor() -> None:
    if os.name == 'posix':
        sys.stdout.write('\033[?25h')
        sys.stdout.flush()

    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
