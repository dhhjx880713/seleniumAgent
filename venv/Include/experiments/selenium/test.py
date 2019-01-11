import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import threading
import time
from selenium.webdriver.common.by import By
import datetime
import time

import pyautogui


def skip_ads():
    driver = webdriver.Chrome(executable_path=r'E:\tmp\chromedriver_win32\chromedriver.exe')
    url = "https://www.youtube.com/watch?v=ghr4MkSuxqw&start_radio=1&list=RDghr4MkSuxqw"
    # url = "http://www.google.com"
    driver.get(url)
    # driver.manage().window().maximize()
    # driver.set_window_size(1920, 1200)
    driver.maximize_window()
    # player_status = driver.execute_script("return document.getElementById('movie_player').getPlayerState()")
    # print(player_status)
    movie_player = driver.find_element_by_id('movie_player')
    print(movie_player)
    time.sleep(5)
    movie_player.click()
    # youtube_search = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/form/div/input")
    # clickButton = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/form/button")

    # clickButton.click()
    # elem = driver.find_element_by_name("q")
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # skipAd = driver.find_element_by_xpath(
    #     "xpath for next /html/body/div[2]/div[4]/div/div[4]/div[2]/div[2]/div/div[4]/div/div/div[5]/button"
    # videoAdUiPreSkipButton = driver.find_element(By.XPATH, '//div[@class="videoAdUiPreSkipButton"]')
    # skipAdFunction(skipAd)
    # elem1 = driver.find_element_by_id('search')
    # elem1.send_keys("python")
    # elem1.send_keys(Keys.RETURN)
    #
    time.sleep(10)


def skipAdFunction(skipAd):
    threading.Timer(3,skipAdFunction).start()
    if(skipAd.is_enabled() or skipAd.is_displayed()):
        skipAd.click()


def test():
    while True:
        print(datetime.datetime.now())
        try:
            # Firefox ain't got no Flash
            browser = webdriver.Chrome(executable_path=r'E:\tmp\chromedriver_win32\chromedriver.exe')
            browser.maximize_window()
            # drop the pleasantries, just open the Flash object
            browser.get('https://www.youtube.com/watch?v=ghr4MkSuxqw&start_radio=1&list=RDghr4MkSuxqw')
            # wait for the page to load
            # time.sleep(10)
            # make sure the browser is in focus
            browser.maximize_window()
            time.sleep(10)
            # click the start test button
            pyautogui.moveTo(165, 783)
            pyautogui.click()
            print("the video is stop!")
            # wait for the test to finish
            time.sleep(10)
            pyautogui.moveTo(165, 783)
            pyautogui.click()
            print("continue to play!")
            time.sleep(60)
            # browser.save_screenshot(datetime.datetime.now().strftime('rds__%Y-%m-%d__%H.%M.png'))
            browser.close()
            # time.sleep(5 * 60)
        except Exception as e:
            # print(e.message)
            pass

if __name__ == "__main__":
    skip_ads()
    # test()