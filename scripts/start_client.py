#!/usr/bin/env python3
"""
Start the client for testing
"""

import argparse
import sys
from typing import List

sys.path.append(".")

from automation_entities.context import background
from automation_entities.web_browser import WebBrowser


def main(argv: List[str]) -> int:
    """main function"""
    parser = argparse.ArgumentParser(
        description="Start the client for testing",
    )
    _ = parser.add_argument("page", help="The page to navigate to for testing")
    args = parser.parse_args(argv)

    browser = WebBrowser(background, args.page, headless=False)
    browser.page_info_result()

    import pdb

    pdb.set_trace()

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
