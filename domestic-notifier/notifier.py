import requests
import pandas as pd

# reads ids as a list (series)
all_IDs = pd.read_csv('id.csv', sep=',', squeeze=True)

# gets API key from separate file for privacy
keyGet = open('key.txt', 'r')
API_KEY = keyGet.read()

# sets people and their ids
jeff = all_IDs[0]
lauren = all_IDs[1]

# emoji to unicode converter with custom labels
emojis = {'poop': '%F0%9F%92%A9', 'pee': '%F0%9F%92%A6', 'meds': '%F0%9F%92%89',
          'fun': '%F0%9F%8E%BE', 'dishes': '%F0%9F%9A%B0', 'food': '%F0%9F%8D%97',
          'school': '%F0%9F%93%94', 'laundry': '%F0%9F%91%95'}

# lists of possible message components
poop = ['I did not poop.', 'I pooped a little bit.', 'I pooped a lot.']
pee = ['I did not pee.', 'I peed a little bit.', 'I peed a lot.']
meds = ['Dad did not put medication on me.', 'Dad put medication on me.']
fun = ['Dad did not play with me.', 'Dad played rope with me.', 'Dad threw the ball for me.']
dishes = ['Dad did not do the dishes.', 'Dad did the dishes.']
food = ['Dad has not eaten today.', 'Dad ate breakfast.', 'Dad ate lunch.', 'Dad ate breakfast and lunch.']
school = ['Dad did not go to class today.', 'Dad went to class today.']
laundry = ['Dad did not do the laundry.', 'Dad did the laundry.']

message = (emojis['poop'] + ': ' + poop[0] + '\n' +
           emojis['pee'] + ': ' + pee[2] + '\n' +
           emojis['meds'] + ': ' + meds[1] + '\n' +
           emojis['fun'] + ': ' + fun[0] + '\n' +
           emojis['dishes'] + ': ' + dishes[0] + '\n' +
           emojis['food'] + ': ' + food[1] + '\n' +
           emojis['school'] + ': ' + school[1] + '\n' +
           emojis['laundry'] + ': ' + laundry[0])


# sends message using telegram api
def send_message(message, person):
    api_call = ('https://api.telegram.org/bot' + API_KEY +
                '/sendmessage?chat_id=' + str(person) + '&text=' + message)

    requests.get(api_call)


send_message(message, lauren)
