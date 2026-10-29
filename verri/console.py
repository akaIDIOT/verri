import argparse

from verri import tasty


def main(args=None):
    parser = argparse.ArgumentParser()

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
    parser.add_argument('flavour', metavar='FLAVOUR', choices=tasty.__all__)
    # let argparse controle the validity of the command line options, (…)
    args = parser.parse_args(args)
    # (…) assume the requested flavour attribute exists
    flavour = getattr(tasty, args.flavour)
    print(flavour(), end=args.end)
