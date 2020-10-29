import praw 
import pandas as pd

auth = pd.read_csv('reddit.csv').squeeze()
reddit = praw.Reddit(client_id = auth[0],
                     client_secret = auth[1],
                     user_agent = 'my user agent',
                     username = auth[2],
                     password = auth[3])

def get_data():    
    ID, Date, Title, Subreddit, Selftext, Score, Ratio, Link = ([] for i in range(8))

    all_posts = []

    saved = list(reddit.redditor(auth[2]).saved())
    upvoted = list(reddit.redditor(auth[2]).upvoted())
    downvoted = list(reddit.redditor(auth[2]).downvoted())

    post_lengths = [len(saved), len(upvoted), len(downvoted)]
    post_names = ['Saved', 'Upvoted', 'Downvoted']
    
    all_posts.extend([saved, upvoted, downvoted])

    for i, post_type in enumerate(all_posts):
        for j, post in enumerate(post_type, start = 1):
            print('Getting data from ' + post_names[i] + ' Posts (' 
            + str(j) +  '/' + str(post_lengths[i]) + ')')

            post_submission = reddit.submission(post)
            try: 
                Date.append(post_submission.created_utc)
                Title.append(post_submission.title)
                Subreddit.append(post_submission.subreddit)
                Selftext.append(post_submission.selftext)
                Score.append(post_submission.score)
                Ratio.append(post_submission.upvote_ratio)
                Link.append(post_submission.permalink)
                ID.append(post)

            except:
                continue

    return ID, Date, Title, Subreddit, Selftext, Score, Ratio, Link, post_lengths

def output_data(results):
    post_lengths = results[8]

    output_df = pd.DataFrame(columns=['ID', 'Date', 'Title', 'Subreddit',
                                      'Selftext', 'Ratio', 'Link'])

    for column in output_df:
        output_df[column] = results[output_df.columns.get_loc(column)]

    type_list = [['Saved'] * post_lengths[0],
                 ['Upvoted'] * post_lengths[1],
                 ['Downvoted'] * post_lengths[2]]

    type_flat = [item for sublist in type_list for item in sublist]
    output_df['Type'] = type_flat
    
    output_df.to_csv('user_info.csv', index = False)

def main():    
    results = get_data()
    output_data(results)

if __name__ == "__main__":
    main()
