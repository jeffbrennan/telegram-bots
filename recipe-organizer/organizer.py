import requests
import pandas as pd
# import json

# Get api key
key_get = open('recipe-organizer/keys/telegram_key.txt', 'r')
API_KEY = key_get.read()

# Get telegram unique ids
user_ids = pd.read_csv('recipe-organizer/keys/id.csv', sep=',')

all_recipes = {'jeff': {},
               'lauren': {}}

# ============== TESTING ============
# with open("recipe-organizer/test.json") as f:
#     data = json.load(f)

# results = data['result']
# ===================================


def tag_searcher(tag_search, user):
    matching_links = []
    recipes = all_recipes[user]

    for recipe in recipes:
        if tag_search in recipes[recipe]['tags']:
            matching_links.append(recipes[recipe]['link'])

    return matching_links


# TODO: add handling so that only the last get request is processed
def send_recipe(result, message_parse):
    # message_parse = message['message']['text'].split()
    tag_search = message_parse[1]
    user = message_parse[2]
    links = tag_searcher(tag_search, user)

    user_id = user_ids.loc[user_ids['user'] == user, 'id'][0]

    for link in links:
        SEND_MESSAGE = ('https://api.telegram.org/bot' + API_KEY
                        + '/sendmessage?chat_id=' + str(user_id)
                        + '&text=' + link)
        requests.get(SEND_MESSAGE)

    
def validate_recipe(user, shortcut):
    if user == 'jeff' or user == 'lauren':
        try:
            int(shortcut)
            return True
        except ValueError:
            return False
    else:
        return False


def add_recipe(result, message_parse, index, all_results):
    link = message_parse[-1]
    user = all_results[index + 1]['message']['text']
    shortcut = all_results[index + 2]['message']['text']
    tags = all_results[index + 3]['message']['text']

    print(link)
    print(user)
    print(shortcut)
    print(tags)

    if not validate_recipe(user, shortcut):
        pass
    else:
        sub_dict = {shortcut: {'link': link, 'tags': tags}}
        all_recipes[user].update(sub_dict)


# edit previous recipe
# TODO: add functionality
# def edit_recipe(message):

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


def get_logger(all_results):
    get_ids = []

    for result in all_results:
        if 'get' in result['message']['text'].split():
            get_ids.append(result['update_id'])
    return get_ids


def result_handler(all_results):
    get_ids = get_logger(all_results)

    for index, result in enumerate(all_results):
        # validate_input(result)
        update_id = result['update_id']

        message_parse = result['message']['text'].lower().split()
        print(message_parse)
        # command = message_parse[0]

        if update_id == get_ids[-1]:
            send_recipe(result, message_parse)
            print('Successful push. Result index: ' + str(index))
        elif 'http' in message_parse[-1]:
            add_recipe(result, message_parse, index, all_results)
            print('Successful add. Result index: ' + str(index))
        # elif command == 'edit':
        #     edit_recipe(message)
        # elif command == 'delete':
            # delete_message(message, index, all_messages)
        else:
            print('N/A text. Result index: ' + str(index))


def receive_updates():
    GET_UPDATES = ('https://api.telegram.org/bot' + API_KEY + '/getUpdates')
    response = requests.get(GET_UPDATES)
    all_results = response.json()

    return all_results['result']


def main():
    print(all_recipes)
    all_results = receive_updates()
    result_handler(all_results)
    print(all_recipes)


if __name__ == "__main__":
    main()
