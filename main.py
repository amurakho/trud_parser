from link_parser import LinkParser

KEYWORDS = (
    'python',
)

if __name__ == '__main__':
    parser = LinkParser(is_paginate=False)
    for keyword in KEYWORDS:
        parser.start(keyword)