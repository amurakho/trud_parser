from link_parser import LinkParser
from save_data import Pipeline, create_db

KEYWORDS = (
    'python',
)
def main():
    parser = LinkParser(is_paginate=False)
    for keyword in KEYWORDS:
        data = parser.start(keyword)

        Pipeline(data).save_data()



if __name__ == '__main__':
    # create_db()
    main()