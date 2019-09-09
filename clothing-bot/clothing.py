import requests
import pandas as pd
from pyowm import OWM

# reads ids as a list (series)
all_IDs = pd.read_csv('id.csv', sep=',', squeeze=True)

# gets API key from separate file for privacy
telegram_key = open('telegram_key.txt', 'r')
TELEGRAM_API_KEY = telegram_key.read()

owm_key = open('owm_key.txt', 'r')
OWM_API_KEY = owm_key.read()

# sets people and their ids
jeff = all_IDs[0]
lauren = all_IDs[1]

# emoji to unicode converter with custom labels
emojis = {'Rain': '%E2%98%94', 'Sunny': '%F0%9F%8C%9E', 'top': '%F0%9F%91%95',
          'bottom': '%F0%9F%91%96'}


# sends message using telegram api
def sendMessage(message, person):
    api_call = ('https://api.telegram.org/bot' + TELEGRAM_API_KEY +
                '/sendmessage?chat_id=' + str(person) + '&text=' + message)

    requests.get(api_call)


def temp_decider(temp_min, temp_max):
    if temp_min > 80:
        top = 'Shirt'
        bottom = 'Shorts'
    elif temp_min > 60 and temp_max < 80:
        top = 'Long sleeve shirt or light jacket'
        bottom = 'Pants'
    elif temp_min > 40 and temp_max < 60:
        top = 'Long sleeve shirt and heavier jacket'
        bottom = 'Pants'
    elif temp_max < 40:
        top = 'Layered clothes with insulated jacket'
        bottom = 'Pants'

    return top, bottom


def weather_report(results):
    # rain decisions
    rain = results['rain']

    if rain:
        umbrella = 'Bring an umbrella'
        condition_emoji = emojis['Rain']
    else:
        umbrella = 'No umbrella'
        condition_emoji = emojis['Sunny']

    # temperature decisions
    temp_max = results['temp']['temp_max']
    temp_min = results['temp']['temp_min']

    temp_avg = (temp_max + temp_min) // 2
    top, bottom = temp_decider(temp_min, temp_max)
    temp_format = ('Low: ' + str(temp_min) + ' | High: ' + str(temp_max) + ' | Avg: ' + str(temp_avg))

    # reporting
    report = ('Temperature today: ' + temp_format + '\n'
              + 'Expected condition: ' + results['condition'] + '\n'
              + 'UV exposure risk: ' + results['risk'] + '\n'
              + emojis['top'] + ': ' + top + '\n'
              + emojis['bottom'] + ': ' + bottom + '\n'
              + condition_emoji + ': ' + umbrella)

    return report


def weather_get():
    # setup
    owm = OWM(OWM_API_KEY)
    obs = owm.weather_at_coords(29.700389, -95.402497) 
    htown_weather = obs.get_weather()

    # weather
    temp_results = htown_weather.get_temperature('fahrenheit')
    rain = htown_weather.get_rain()
    wind = htown_weather.get_wind()['speed']
    condition = htown_weather.get_detailed_status()

    # UV
    uvi = owm.uvindex_around_coords(29.700389, -95.402497)
    risk = uvi.get_exposure_risk()

    output = {'temp': temp_results, 'rain': rain, 'wind': wind, 'condition': condition,
              'risk': risk}

    return output


results = weather_get()
message = weather_report(results)
print(message)
# sendMessage(message, jeff)
