import itertools
import sys
import time




__all__ = [
    'spinner',
]




FRAMES: dict[str, dict[str, any]] = {
    'dot': {
        'i': 0.25,
        'f': [
            '.  ',
            '.. ',
            '...',
            '   ',
        ],
    },
    'spin': {
        'i': 0.12,
        'f': [
            # '|',
            # '/',
            # '-',
            # '\\',
            '\\',
            '-',
            '/',
            '|',
        ],
    },
    'arrow': {
        'i': 0.1,
        'f': [
            '>>>>>>>',
            ':>>>>>>',
            '>:>>>>>',
            '>>:>>>>',
            '>>>:>>>',
            '>>>>:>>',
            '>>>>>:>',
            '>>>>>>:',
        ],
    },
    'binary': {
        'i': 0.12,
        'f': [
            ':01110100:',
            ':01101000:',
            ':01100101:',
            ':00100000:',
            ':01100110:',
            ':01110101:',
            ':01110100:',
            ':01110101:',
            ':01110010:',
            ':01100101:',
            ':00100000:',
            ':01101001:',
            ':01110011:',
            ':00100000:',
            ':01101010:',
            ':01110101:',
            ':01110011:',
            ':01110100:',
            ':00100000:',
            ':01100001:',
            ':01101110:',
            ':00100000:',
            ':01101001:',
            ':01100100:',
            ':01100101:',
            ':01100001:',
        ],
    },
}




def spinner(duration: float, type: str = 'dot', start: str = '', end: str = '\n') -> None:
    if start != '':
        sys.stdout.write(start)
        sys.stdout.flush()

    until: float = time.time() + duration

    frames = itertools.cycle(FRAMES[type]['f'])

    while time.time() < until:
        f = next(frames)
        sys.stdout.write(f)
        sys.stdout.flush()
        time.sleep(FRAMES[type]['i'])
        sys.stdout.write('\b' * len(f))

    sys.stdout.write(' ' * len(f) + '\b' * len(f))

    if end != '':
        sys.stdout.write(end)

    sys.stdout.flush()
