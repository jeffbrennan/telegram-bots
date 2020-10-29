import os 
import time 
import glob
import random
import zipfile
import requests
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def build_selenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")     # run in background
    chrome_options.add_argument("--disable-gpu")  # laptop has no dedicated gpu
    chrome_options.add_argument('--log-level=3')  # suppress all console logs

    # enable headless downloading
    chrome_options.add_experimental_option("prefs", {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False   
    })

    driver = webdriver.Chrome(executable_path=r"C:\Program Files\chromedriver.exe", options=chrome_options)
    return driver


def scrape_data(driver): 
    site_url = 'https://data.typeracer.com/pit/login?continueURL=https%3A%2F%2Fdata.typeracer.com%2Fpit%2Fexport_data'

    driver.get(site_url)

    wait = WebDriverWait(driver, 3)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='username']"))).click()
    user_field = driver.find_element_by_xpath("//input[@name='username']")
    time.sleep(round(random.uniform(0,1), 2))

    user_field.send_keys(auth['typeracer_user'])
    time.sleep(round(random.uniform(0,1), 2))

    pw_field = driver.find_element_by_xpath("//input[@name='password']")
    pw_field.send_keys(auth['typeracer_pw'])
    time.sleep(round(random.uniform(0,1), 2))

    pw_field.send_keys(Keys.ENTER)
    time.sleep(round(random.uniform(0,1), 2))
    
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Continue']"))).click()


def plot_data():
  # TODO: update hue & group to Week after 2 weeks
  wpm_df = pd.read_csv(f'{download_dir}\\race_data.csv')
  wpm_df.columns = ['Race', 'WPM', 'Accuracy', 'Rank', 'Racers', 'Text', 'Date']
  wpm_df.Date = pd.to_datetime(wpm_df.Date)
  wpm_df['Day'] = wpm_df['Date'].dt.strftime('%a')
  wpm_df['Week'] = wpm_df['Date'].dt.week
  wpm_df['Day_Unique'] = wpm_df['Week'].astype(str) + ' - ' + wpm_df['Day']
  wpm_df['Race_Day'] = wpm_df.groupby(['Day_Unique']).cumcount()+1


  # update to include more data points after 1 week
  wpm_avg = round(wpm_df.groupby('Day', as_index = False).mean()['WPM'], 2).tolist()


  progress = sns.lmplot(x="Race_Day", y="WPM", hue="Day", data=wpm_df,
                        order=2, scatter_kws={"s": 30})
  progress.set(xlim = (0, wpm_df.Race_Day.max() * 1.1))
  progress.set(xlabel='Daily Races')
  progress.fig.suptitle(f'Start Average: {wpm_avg[0]} WPM\nCurrent Average: {wpm_avg[-1]} WPM',
                        ha = 'left', x = 0.1, y = 1.05)
  progress.savefig('viz/wpm_progress.png')
  plt.clf()


def process_zip(zip_path):
  with zipfile.ZipFile(zip_path, 'r') as zip_ref:
      zip_ref.extractall(download_dir)


def check_dir(): 
  start_time = time.time()
  wpm_raw = glob.glob(f'{download_dir}\*')
  day_seconds = 60 * 60 * 24

  old_files = [f for f in wpm_raw if ((start_time - os.path.getctime(f)) > day_seconds*0.5)]

  if old_files:
    [os.remove(f) for f in old_files]
    scrape_data(build_selenium())
  
  return ''.join([f for f in glob.glob(f'{download_dir}\*') if f.endswith('.zip')])
    

def send_photo(bot_key, chat_id, image):
  files = {'photo': open(image, 'rb')}
  message = (f"https://api.telegram.org/bot{bot_key}/sendPhoto?chat_id={chat_id}")
  requests.post(message, files = files)


auth = pd.read_csv('auth/auth.csv')
download_dir = r'C:\Users\jeffb\Desktop\Life\personal-projects\wpm\data'

new_data = check_dir()
process_zip(new_data)
plot_data()
send_photo(auth['telegram_key'][0], auth['telegram_id'][0], 'viz/wpm_progress.png')