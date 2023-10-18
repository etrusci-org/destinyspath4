import os




__all__ = [
    'clear_terminal',
    'disable_terminal_cursor',
    'enable_terminal_cursor',
]




def clear_terminal() -> None:
    # investigate solution for B607: start_process_with_partial_path
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        print('\033c', end='')


# investigate better solutions to toggle the cursor, e.g. without ansi codes

def disable_terminal_cursor() -> None:
    print('\033[?25l', end='')


def enable_terminal_cursor() -> None:
    print('\033[?25h', end='')
