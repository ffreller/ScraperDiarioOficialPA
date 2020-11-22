from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def open_driver():
    opcoes = Options()
    opcoes.add_argument('--headless')
    chrmdrvr = 'chrmdrvr/chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chrmdrvr, options=opcoes)
    return driver