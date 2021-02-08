import argparse
import logging

from crawler.executor import Crawler


def main():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s: %(message)s',
        level=logging.DEBUG)
    parser = argparse.ArgumentParser(
        description='Crawler that dumps website data into provided directory.')
    parser.add_argument('start_url',
                        metavar='start-url',
                        help='Starting URL')
    parser.add_argument('out_dir',
                        metavar='out-dir',
                        help='Directory for output')
    args = parser.parse_args()
    crawler = Crawler(args.start_url, args.out_dir)
    crawler.run()


if __name__ == '__main__':
    main()
