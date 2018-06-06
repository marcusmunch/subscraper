import argparse
import time
import os

import praw


def parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("user", help="User account (from praw.ini)")
    parser.add_argument("subreddit", help="A subreddit to scrape", type=str)
    args = parser.parse_args()

    return args

def main():
    parse = parser()

    reddit = praw.Reddit(parse.user, user_agent="Subreddit Scraper")
    print("Logged in as {}. Now scraping /r/{}".format(reddit.user.me(), parse.subreddit))

    post_generator = reddit.subreddit(parse.subreddit).new(limit=None)

    if not os.path.exists('./output/'):
        os.mkdir('output')

    with open('output/{}.txt'.format(parse.subreddit.lower()), 'w') as f:
        f.write('Post titles of subreddit /r/{} as of {}.\n'.format(parse.subreddit, time.strftime('%c')))

    while True:
        try:
            post = post_generator.next()

            with open('output/{}.txt'.format(parse.subreddit.lower()), 'a') as f:
                print(post.title.encode('utf-8'))
                f.write(post.title.encode('utf-8') + '\n')

        except StopIteration:
            break


if __name__ == "__main__":
    main()