import rich
import inspect
from rich.json import JSON
import json
from rich.console import Console


def trace(show_cookies=False, pprint_caller_args=False):
    console = Console()
    outer_args = locals()

    def outer(f):
        funcname = f.__name__
        fsig = inspect.signature(f)
        def assign_color(obj):
            """Randomly assign each function a fixed color used when printing the trace"""
            _colors = ("red", "yellow", "green", "blue", "magenta", "cyan")
            color = _colors[obj.__hash__() % len(_colors)]
            return color

        c1 = assign_color(funcname)

        def inner(*args, **kwargs):
            _args = fsig.bind(*args, **kwargs).arguments

            caller = inspect.stack()[1][3]
            caller = '__main__' if caller == '<module>' else caller

            c2 = assign_color(caller)
            try:
                cookies = {k: v for k, v in vars()['request'].cookies.items()}
            except KeyError:
                cookies = {}

            rich.print(
                f"[{c1} bold]{funcname}[/] invoked by [{c2} bold]{caller}[/] with args:", end= " "
            )
            if outer_args['pprint_caller_args']:
                rich.print_json(json.dumps(_args, default=lambda x: x if hasattr(x, '__hash__') else str(x)))
            else:
                print(_args)
            if outer_args['show_cookies'] and cookies:

                rich.print(f"[white]{'=' * 30}COOKIES{'=' * 30}[/]\n")
                rich.print(cookies)
                rich.print(f"[white]{'=' * (60 + len('COOKIES'))}[/]\n\n")
            output = f(*args, **kwargs)
            rich.print(
                f"[{c1} bold]{funcname}[/] returned to [{c2} bold]{caller}[/]: {output}"
            )
            return output

        return inner
    return outer

@trace()
def square(x):
    return x*x
@trace()
def cube(x):
    return square(square(x))

if __name__ == '__main__':
    result = cube(16)
    print(f"Result: {result}")