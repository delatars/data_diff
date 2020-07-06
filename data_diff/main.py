import sys
import argparse
from data_diff.differ import Differ
from data_diff.loaders import DetermineLoader


def show_loaders_info():
    l_format = "   {scheme:<15} - {uri:>15}"
    for loader_group in DetermineLoader.LOADER_GROUPS:
        print(f"{loader_group.group_name}:")
        for loader in loader_group.loaders:
            for scheme in loader.schemes:
                print(l_format.format(scheme=scheme, uri=loader.uri_example.format(scheme=scheme)))


def parse_args():
    parser = argparse.ArgumentParser(description='Data differ')
    parser.add_argument('loader_from_uri', type=str, action="store",
                        default=False, help='loader with actual data.')
    parser.add_argument('loader_to_uri', type=str, action="store",
                        default=False, help='loader where data will be updated.')
    parser.add_argument('--mode', '-m', choices=['auto', 'manual'], default="manual",
                        help='Set differ mode: manual|auto (default: manual)')
    parser.add_argument('--loaders', '-l', action='store_true',
                        help='Show available loaders')

    argv = sys.argv[1:]
    if not len(argv):
        parser.print_help()
        sys.exit(1)
    if "-l" in argv or '--loaders' in argv:
        show_loaders_info()
        sys.exit(0)
    return parser.parse_args(argv)


def main():
    args = parse_args()
    loader_from = DetermineLoader(args.loader_from_uri).get_loader()
    loader_to = DetermineLoader(args.loader_to_uri).get_loader()
    differ = Differ(loader_from, loader_to)
    if args.mode == "auto":
        differ.auto_differences()
    if args.mode == "manual":
        differ.manual_differences()


if __name__ == '__main__':
    main()
