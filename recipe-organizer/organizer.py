import requests
import pandas as pd
import json

# gets API key from separate file for privacy
key_get = open('keys/telegram_key.txt', 'r')
API_KEY = key_get.read()

# Read telegram IDs
user_ids = pd.read_csv('keys/id.csv', sep=',')

all_recipes = {
               'jeff': {},
               'lauren': {}
              }


# ============== TESTING ============
# with open("test.json") as f:
#     data = json.load(f)
# print('http' in data['result'][2]['message']['text'].split())
# print(data['result'][2]['message']['text'].split()[-1])
# recipes = all_recipes['jeff']
# print(recipes)
# for recipe in recipes:
#     if 'tilapia' in recipes[recipe]['tags']:
#         print(recipes[recipe]['link'])


# for recipe in all_recipes:
#     if tag_search in recipe['tags']:
#         matching_links.append(recipe['link'])


# ===================================


# TODO: simplify logic
def tag_searcher(tag_search, user):
    print(tag_search)
    print(user)
    print(all_recipes)
    matching_links = []
    recipes = all_recipes[user]

    for recipe in recipes:
        if tag_search in recipes[recipe]['tags']:
            matching_links.append(recipes[recipe]['link'])

    return matching_links

# TODO: see if it is possible to self delete bot responses
# def clear_output():
# # for message in all messages
#     # if message is from bot
#         # add id to list 

# # for id in list
#     # post delete request

#     for message in all_messages:
#         if message['']


# TODO: add handling so that only the last get request is processed
def send_recipe(message):
    message_parse = message['message']['text'].split()
    tag_search = message_parse[1]
    user = message_parse[2]
    links = tag_searcher(tag_search, user)

    user_id = user_ids.loc[user_ids['user'] == user, 'id'][0]

    # delete previous messages to prevent spamming
    # clear_output()

    for link in links:
        SEND_MESSAGE = ('https://api.telegram.org/bot' + API_KEY
                        + '/sendmessage?chat_id=' + str(user_id)
                        + '&text=' + link)

    requests.get(SEND_MESSAGE)


def shortcut_validation(shortcut):
    try:
        int(shortcut)
        return True
    except ValueError:
        return False


def add_recipe(message, index, all_messages):
    link = message['message']['text'].split()[-1]
    user = all_messages[index+1]['message']['text']
    shortcut = all_messages[index+2]['message']['text']
    tags = all_messages[index+3]['message']['text']

    print(link)
    print(user)
    print(shortcut)
    print(tags)

    # TODO: simplify logic
    # TODO add check for tags
    if user != 'jeff' and user != 'lauren':
        if not shortcut_validation(shortcut):
            pass
        pass
    else:
        sub_dict = {shortcut: {'link': link, 'tags': tags}}
        all_recipes[user].update(sub_dict)


# edit previous recipe
# TODO: add functionality
# def edit_recipe(message):

# TODO: add validation logic (valid link, command, user etc.)
# def validate_input(message):
#     while True:

# TODO: make this work
# def delete_message(message, index, all_messages):
#     delete_id = all_messages[index-1]['update_id']
#     # DELETE_MESSAGE = ('https://api.telegram.org/bot' + API_KEY + '/deleteMessage')
#     DELETE_MESSAGE = ('https://api.telegram.org/bot' + API_KEY 
#                       + '/getUpdates?offset=' + str(delete_id-1))
    
#     requests.get(DELETE_MESSAGE)

# TODO: write logic to save requests (telegram will delete after too many)
# def save_recipes():
#     recipes = pd.DataFrame()
#     recipes.to_csv('data/recipes.csv')


def message_handler(all_messages):
    for index, message in enumerate(all_messages):
        # validate_input(message)
        message_parse = message['message']['text'].lower().split()
        command = message_parse[0]
        if command == 'get':
            send_recipe(message)
        elif 'http' in message_parse[-1]:
            add_recipe(message, index, all_messages)
        # elif command == 'edit':
        #     edit_recipe(message)
        # elif command == 'delete':
            # delete_message(message, index, all_messages)
        else:
            print('N/A text. Message index: ' + str(index))


def receive_message():
    GET_UPDATES = ('https://api.telegram.org/bot' + API_KEY + '/getUpdates')
    message_response = requests.get(GET_UPDATES)
    all_messages = message_response.json()

    return all_messages['result']


def main():
    print(all_recipes)
    all_messages = receive_message()
    message_handler(all_messages)
    print(all_recipes)


if __name__ == "__main__":
    main()
