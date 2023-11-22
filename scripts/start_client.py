#!/usr/bin/env python3
"""
Start the client for testing
"""

import sys
import argparse

sys.path.append(".")

from automation_entities.context import background
from automation_entities.web_browser import WebBrowser


def main(argv):
    """main function"""
    parser = argparse.ArgumentParser(
        description="Start the client for testing",
    )
    parser.add_argument("page", help="The page to navigate to for testing")
    args = parser.parse_args(argv)

    browser = WebBrowser(background, args.page, headless=False)
    browser.page_info_result()

    import pdb

    pdb.set_trace()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
