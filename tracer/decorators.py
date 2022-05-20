import os.path
import rich
import inspect
from rich.json import JSON
import json
from rich.console import Console
depth = 0

def trace(show_cookies=False, pprint_caller_args=False):
    console = Console()
    outer_args = locals()

    def outer(f):
        funcname = f.__name__
        fsig = inspect.signature(f)
        # depth = 0
        def assign_color(obj):
            """Randomly assign each function a fixed color used when printing the trace"""
            _colors = ("red", "yellow", "green", "blue", "magenta", "cyan")
            color = _colors[obj.__hash__() % len(_colors)]
            return color

        c1 = assign_color(funcname)

        def inner(*args, **kwargs):
            global depth
            _args = fsig.bind(*args, **kwargs).arguments
            prefix = ''.join("    " * depth)
            caller = inspect.stack()[1][3]
            if caller == '<module>':
                try:
                    ns = os.path.basename(__file__).split(".")[0] + "."
                except:
                    ns = ""
                caller = ns + '__main__'
            c2 = assign_color(caller)
            try:
                cookies = {k: v for k, v in vars()['request'].cookies.items()}
            except KeyError:
                cookies = {}
            rich.print(
                prefix + "λ " + f"[{c1} bold]{funcname}[/] invoked by [{c2} bold]{caller}[/] with args:", end= " "
            )
            if outer_args['pprint_caller_args']:
                rich.print_json(json.dumps(_args, default=lambda x: x if hasattr(x, '__hash__') else str(x)))
            else:
                print(_args)
            if outer_args['show_cookies'] and cookies:
                rich.print(prefix + f"[white]{'=' * 30}COOKIES{'=' * 30}[/]\n")
                rich.print(cookies)
                rich.print(prefix + f"[white]{'=' * (60 + len('COOKIES'))}[/]\n\n")

            depth += 1
            output = f(*args, **kwargs)
            rich.print(
                prefix + "∴ " + f"[{c1} bold]{funcname}[/] replied to [{c2} bold]{caller}[/]: {output}", end="\n\n"
            )

            depth -= 1
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