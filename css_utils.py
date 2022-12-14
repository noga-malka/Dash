def spacing(count: int, margin: bool = False):
    return {'margin' if margin else 'padding': f'{count}px'}


def width(option: str = 'inherit'):
    return {'width': option}
