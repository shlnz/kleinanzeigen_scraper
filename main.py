import argparse
import logging

from provider.kleinanzeigen_ebay import KleinanzeigenEbay


class SearchStarter(object):
    def __init__(self, provider):
        super(SearchStarter, self).__init__()

        self.provider = provider


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A little helper program that sends you an email if an article suits your needs.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Be Verbose")
    args = parser.parse_args()

    if args.verbose is True:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
