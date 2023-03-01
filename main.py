from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os

TWITTER_USER = os.environ.get("TWITTER_USER")
TWITTER_PASS = os.environ.get("TWITTER_PASS")
PROMISED_DOWN = 400
PROMISED_UP = 10
CHROME_DRIVER_PATH = Service("/Users/briantapia/Documents/Development/chromedriver")

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

global complaint, up_speed, down_speed
complaint = ""
down_speed = 0
up_speed = 0

class InternetSpeedTwitterBot:
    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(service=CHROME_DRIVER_PATH, options=options)

    def get_internet_speed(self):
        global complaint, up_speed, down_speed
        self.driver.get("https://www.google.com/search?q=speed+test&rlz=1C5CHFA_enUS1011US1011&oq=speed+test&aqs=chrome..69i57j69i60.3144j0j7&sourceid=chrome&ie=UTF-8")
        run_test = self.driver.find_element(
            By.XPATH,
            '//*[@id="knowledge-verticals-internetspeedtest__test_button"]/div')
        run_test.click()
        time.sleep(30)
        down_speed = self.driver.find_element(
            By.XPATH,
            '//*[@id="knowledge-verticals-internetspeedtest__download"]/p[1]').text
        up_speed = self.driver.find_element(
            By.XPATH,
            '//*[@id="knowledge-verticals-internetspeedtest__upload"]/p[1]').text
        complaint = f"@xfinity Why are my download/upload speeds so bad? I'm promised 400mbps down and 10mbps up," \
                    f" I'm currently only getting {down_speed}mbps down and {up_speed}mbps up. What gives?!  "

    def tweet(self):
        global complaint, up_speed, down_speed
        self.driver.get("https://twitter.com/i/flow/login")
        time.sleep(2)
        enter_user = self.driver.find_element(
            By.XPATH,
            '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'
        )
        enter_user.send_keys(TWITTER_USER)
        next_button = self.driver.find_element(
            By.XPATH,
            '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div'
        )
        next_button.click()
        time.sleep(2)
        enter_pass = self.driver.find_element(
            By.XPATH,
            '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
        )
        enter_pass.send_keys(TWITTER_PASS)
        login = self.driver.find_element(
            By.XPATH,
            '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div'
        )
        login.click()
        time.sleep(6)
        draft = self.driver.find_element(By.CLASS_NAME, "public-DraftStyleDefault-block")
        draft.send_keys(complaint)
        send = self.driver.find_element(
            By.XPATH,
        '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/span/span')
        send.click()


bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH)
bot.get_internet_speed()
if PROMISED_UP > float(up_speed) or PROMISED_DOWN > float(down_speed):
    bot.tweet()



