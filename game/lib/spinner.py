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
            ' . ',
            '  .',
            ' . ',
        ],
    },
    'spin': {
        'i': 0.15,
        'f': [
            '|',
            '/',
            '-',
            '\\',
        ],
    },
    'spin2': {
        'i': 0.15,
        'f': [
            '\\',
            '-',
            '/',
            '|',
        ],
    },
    'arrow': {
        'i': 0.15,
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
        'i': 0.2,
        'f': [
            '01110100',
            '01101000',
            '01100101',
            '00100000',
            '01100110',
            '01110101',
            '01110100',
            '01110101',
            '01110010',
            '01100101',
            '00100000',
            '01101001',
            '01110011',
            '00100000',
            '01101010',
            '01110101',
            '01110011',
            '01110100',
            '00100000',
            '01100001',
            '01101110',
            '00100000',
            '01101001',
            '01100100',
            '01100101',
            '01100001',
            '00100000',
        ],
    },
    'binary2': {
        'i': 0.2,
        'f': [
            '01100110',
            '-1100110',
            '0+100110',
            '01-00110',
            '011+0110',
            '0110-110',
            '01100+10',
            '011001-0',
            '0110011+',
            '01110101',
            '0111010-',
            '011101+1',
            '01110-01',
            '0111+101',
            '011-0101',
            '01+10101',
            '0-110101',
            '+1110101',
            '01110100',
            '-1110100',
            '0+110100',
            '01-10100',
            '011+0100',
            '0111-100',
            '01110+00',
            '011101-0',
            '0111010+',
            '01110101',
            '0111010-',
            '011101+1',
            '01110-01',
            '0111+101',
            '011-0101',
            '01+10101',
            '0-110101',
            '+1110101',
            '01110010',
            '-1110010',
            '0+110010',
            '01-10010',
            '011+0010',
            '0111-010',
            '01110+10',
            '011100-0',
            '0111001+',
            '01100101',
            '0110010-',
            '011001+1',
            '01100-01',
            '0110+101',
            '011-0101',
            '01+00101',
            '0-100101',
            '+1100101',
        ],
    },
    'heartbeat': {
        'i': 0.17,
        'f': [
            '--------',
            '^~------',
            '~~~-----',
            '-~^~----',
            '--------',
            '--------',
            '----~^~-',
            '-----~~~',
            '------~^',
            '--------',
            '--------',
            '--------',
        ],
    }
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
