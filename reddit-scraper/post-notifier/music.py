from auth import reddit, jeff, TELEGRAM_AUTH
import requests
import re


def music_get(sub):
    week_posts = []
    for submission in sub.search('[FRESH', sort='top', limit=10, time_filter='week'):
        if('spotify' in submission.url or 'youtube' in submission.url):
            week_posts.extend([submission.url])
        else:
            if('open.spotify' in submission.selftext):
                # TODO: fix extraneous chars at end of url
                spotify_match = re.search(r'(https:\/\/open\.spotify[^\s]*)',
                                          submission.selftext)
                week_posts.extend([spotify_match.group(1)])

    return week_posts


def send_message(links, person, sub):
    header = ('=========' + sub.upper() + '=========')
    links.insert(0, header)

    for link in links:
        api_call = ('https://api.telegram.org/bot' + TELEGRAM_AUTH
                    + '/sendmessage?chat_id=' + str(person) + '&text=' + link)
        requests.get(api_call)


def weekly():
    for sub in ['hiphopheads', 'indieheads', 'popheads']:
        links = music_get(reddit.subreddit(sub))
        send_message(links, jeff, sub)


if __name__ == '__main__':
    weekly()
