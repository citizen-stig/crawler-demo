import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Crawler that dumps website data into provided directory.')
    parser.add_argument('start-url', help='Starting URL')
    parser.add_argument('output-dir', help='Directory for output')
    args = parser.parse_args()


if __name__ == '__main__':
    main()
