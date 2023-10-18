import random




__all__ = [
    'rffr',
    # 'rifr',
    'ff',
]




def rffr(range: tuple[float, float]) -> float:
    return random.uniform(*range)


# def rifr(range: tuple[int, int]) -> int:
#     return random.randint(*range)


def ff(n: float, prec: int = 6) -> str:
    return f'{n:.{prec}f}'
