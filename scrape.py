import argparse
import os
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

    r = requests.get('https://api.pushshift.io/reddit/search/submission/?subreddit={}'.format(parse.subreddit)).json()

    fetch_number = 0

    if not os.path.exists('./output/'):
        os.mkdir('output')

    with open('output/{}.txt'.format(parse.subreddit.lower()), 'w') as f:
        f.write('Post titles of subreddit /r/{} as of {}:\n'.format(parse.subreddit, time.strftime('%c')))

    while True:
        try:
            for i in r['data']:
                to_write = i['title'].encode('utf-8')
                print("{:04d}: {:40}".format(fetch_number, to_write))

                with open('output/{}.txt'.format(parse.subreddit.lower()), 'a') as f:
                    f.write(to_write + '\n')

                fetch_number += 1

            time.sleep(0.2)

            r = requests.get(
                'https://api.pushshift.io/reddit/search/submission/?subreddit={}&before={}'.format(parse.subreddit, r['data'][-1]['created_utc'])).json()

        except IndexError:
            break

    with open('output/{}.txt'.format(parse.subreddit.lower()), 'r') as f:
        my_list = list(l[:-1] for l in f.readlines()[1:])

    from collections import Counter
    counted = dict(Counter(my_list))

    with open('output/{}_sorted.txt'.format(parse.subreddit.lower()), 'w') as f:
        f.write('name\tcounts\n')

    for i in counted:
        with open('output/{}_sorted.txt'.format(parse.subreddit.lower()), 'a') as f:
            f.write('{}\t{}\n'.format(i, counted[i]))


if __name__ == "__main__":
    main()