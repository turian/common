import inspect
def lineno(depth=1):
    frame, _, lineno, _, _, _ = inspect.stack()[depth]
    return lineno
