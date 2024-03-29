from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import sys
from os import path, environ
from time import sleep
from dotenv import load_dotenv

try:
    # System path helper
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = path.dirname(__file__)
        return path.join(base_path, relative_path)

    # Loading values from .env
    load_dotenv()
    refreshTimer = int(environ.get('REFRESH_TIMER', '3'))
    firefoxPath = environ.get('FIREFOX_PATH', '')
    email = environ.get('EMAIL', '')
    password = environ.get('PASSWORD', '')
    title_selector = 'title'
    artist_selector = 'creatives'
    # Initial setup
    currentSong = ''
    binary = FirefoxBinary(firefoxPath)
    driver = webdriver.Firefox(firefox_binary=binary, executable_path=resource_path('.\driver\geckodriver.exe'))

    # Open login page
    driver.get("https://www.epidemicsound.com/login/")
    if email != '' and password != '':
        driver.find_element_by_css_selector("input#username").send_keys(email)
        driver.find_element_by_css_selector("input#password").send_keys(password)
        try:
            driver.find_element_by_css_selector('input#kc-login').click()
        except:
            pass

    # Main loop for fetching song name
    while True:
        try:
            songName = driver.find_element_by_css_selector(f'a[class^="src-mainapp-player-components-___TrackInfo__{title_selector}"]')
            artistName = driver.find_element_by_css_selector(f'div[class^="src-mainapp-player-components-___TrackInfo__{artist_selector}"]')
            if songName.text != None and artistName.text != None:
                musicData = f'{artistName.text} - {songName.text}'
                if currentSong != musicData:
                    currentSong = musicData
                    print(f'Playing: {musicData}')
                    with open('music_info.txt', 'w') as f:
                        f.write(musicData)
        except:
            pass
        sleep(refreshTimer)
except:
    log = sys.exc_info()[0]
    print("Unexpected error:", log)
    with open('log.txt', 'w') as f:
        f.write(str(log))
