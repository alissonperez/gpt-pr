'''Utility to show text with colors in console'''


GREY = '\x1b[38;21m'
BLUE = '\x1b[38;5;39m'
YELLOW = '\x1b[38;5;226m'
RED = '\x1b[38;5;196m'
BOLD_RED = '\x1b[31;1m'
UNDERLINE = '\033[4m'
GREEN = '\033[92m'
BOLD = '\033[1m'
RESET = '\x1b[0m'
ENDC = '\033[0m'

enabled = True


def grey(text):
    return _colorfy(GREY, text)


def blue(text):
    return _colorfy(BLUE, text)


def yellow(text):
    return _colorfy(YELLOW, text)


def red(text):
    return _colorfy(RED, text)


def bold(text):
    return _colorfy(BOLD, text)


def bold_red(text):
    return _colorfy(BOLD, text)


def underline(text):
    return _colorfy(UNDERLINE, text)


def green(text):
    return _colorfy(GREEN, text)


def _colorfy(color, text):
    if not enabled:
        return text

    return f'{color}{text}{ENDC}'
