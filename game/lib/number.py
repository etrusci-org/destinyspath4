import random




def rffr(range: tuple[float, float]) -> float:
    return random.uniform(*range)


def ff(n: float, prec: int = 6) -> str:
    return f'{n:.{prec}f}'
