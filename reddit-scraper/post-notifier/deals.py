from auth import reddit, jeff, TELEGRAM_AUTH
import requests

def clothes_get(sub):
    deals = []
    interests = ['Patagonia', 'Reigning Champ', 'Red Wings']
    query = ' OR '.join(interests)

    for submission in sub.search(query, time_filter='day'):
        deals.extend([submission.title, submission.url])
    return deals


def pc_parts_get(sub):
    deals = []
    interests = ['3070', '3700x']
    query = ' OR '.join(interests)

    for submission in sub.search(query, time_filter='day'):
        deals.extend([submission.title, submission.url])
    return deals


def send_message(links, person, sub):
    header = ('=========' + sub.upper() + '=========')
    links.insert(0, header)

    for link in links:
        api_call = ('https://api.telegram.org/bot' + TELEGRAM_AUTH
                    + '/sendmessage?chat_id=' + str(person) + '&text=' + link)
        requests.get(api_call)


def daily():
    clothes = clothes_get(reddit.subreddit('frugalmalefashion'))
    pc_parts = pc_parts_get(reddit.subreddit('buildapcsales'))

    send_message(clothes, jeff, 'frugalmalefashion')
    send_message(pc_parts, jeff, 'buildapcsales')

if __name__ == '__main__':
    daily()
