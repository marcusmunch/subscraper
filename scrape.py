import argparse
import os
import re
import sys
import time

import requests


def parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("user", help="User account (from praw.ini)")
    parser.add_argument("subreddit", help="A subreddit to scrape", type=str)
    args = parser.parse_args()

    return args


def main():
    parse = parser()

    print("Now scraping /r/{}...".format(parse.subreddit))

    r = requests.get('https://api.pushshift.io/reddit/search/submission/?subreddit={}'.format(parse.subreddit)).json()

    fetch_number = 1

    if not os.path.exists('./output/'):
        os.mkdir('output')

    with open('output/{}.txt'.format(parse.subreddit.lower()), 'w') as f:
        f.write('\t'.join(['title', 'author', 'score', 'created_utc', 'over_18']) + '\n')

    while True:
        try:
            for i in r['data']:
                title = i['title'].encode('utf8')
                author = str(i['author'])
                score = str(i['score'])
                created = str(i['created_utc'])
                over_18 = str(i['over_18'])

                title = re.sub(r'\(.*\)|\[.*\]', '', title).strip()

                sys.stdout.write("{:04d}: {:40.40}\r".format(fetch_number, title))
                sys.stdout.flush()

                with open('output/{}.txt'.format(parse.subreddit.lower()), 'a') as f:
                    to_write = '\t'.join([title, author, score, created, over_18])

                    f.write(to_write + '\n')

                fetch_number += 1

            time.sleep(0.25)

            r = requests.get(
                'https://api.pushshift.io/reddit/search/submission/?subreddit={}&before={}'.format(
                    parse.subreddit, r['data'][-1]['created_utc'])).json()

        except IndexError:
            break
    print("\nDone!")


if __name__ == "__main__":
    main()
