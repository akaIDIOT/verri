import argparse

from verri import tasty


def main(args=None):
    parser = argparse.ArgumentParser()

    # two positional arguments, the first of which is required to be "tasty", the second being the flavour
    parser.add_argument('tasty', metavar='tasty', choices=('tasty',))
    parser.add_argument('flavour', metavar='FLAVOUR', choices=tasty.__all__)
    # let argparse controle the validity of the command line options, (…)
    args = parser.parse_args(args)
    # (…) assume the requested flavour attribute exists
    flavour = getattr(tasty, args.flavour)
    print(flavour())
