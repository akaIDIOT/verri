import argparse

from verri import tasty


def main(args=None):  # noqa: SMP903 (function not aimed at users and not included in docs)
    parser = argparse.ArgumentParser(
        description=(
            'create a tasty, PEP-440 compliant version, '
            "see verri's docs for information on the various version flavours"
        )
    )

    # add an option to mimic the way "echo" handles a trailing newline
    parser.add_argument(
        '-n',
        '--no-newline',
        dest='end',
        action='store_const',
        const='',
        default='\n',
        help='do not output the trailing newline',
    )
    # two positional arguments, the first of which is required to be "tasty", the second being the flavour
    parser.add_argument('tasty', metavar='tasty', choices=('tasty',))
    parser.add_argument('flavour', choices=tasty.__all__, help='a tasty version flavour')
    # let argparse control the validity of the command line options, (…)
    args = parser.parse_args(args)
    # (…) assume the requested flavour attribute exists
    print(getattr(tasty, args.flavour)(), end=args.end)
