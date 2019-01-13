import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import threading
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import time

import pyautogui


def wait_until_example():
    # driver = webdriver.Chrome(executable_path=r'../../chromedriver_win32\chromedriver.exe')
    driver = webdriver.Firefox(executable_path=r'../../geckodriver-v0.23.0-win64/geckodriver.exe')
    url = "https://www.youtube.com/watch?v=XYypsQOhQXE"
    # url = "https://www.youtube.com/watch?v=Dz4Vq7hZtqo"
    driver.get(url)
    timeout = 100
    wait = WebDriverWait(driver , timeout)
    # try:
    #     wait.until(driver.find_element_by_class_name('ytp-ad-skip-button'))
    # except TimeoutError:
    #     print("no advertisemetn")
    while True:
        end_time = time.time() + timeout
        player_status = driver.execute_script("return document.getElementById('movie_player').getPlayerState()")
        print("current play state: ", player_status)
        if player_status == -1:
            print("playing ads")
            try:
                value = driver.find_element_by_class_name('ytp-ad-skip-button')
                if value:
                    print("find skip button, prepare click in 5 seconds")
                    time.sleep(5)
                    value.click()
            except NoSuchElementException:
                print('skip button not ready!')
        elif player_status == 0:
            time.sleep(0.5)
        elif player_status == 0:
            driver.quit()
            break
        else:
            pass
        # try:
        #     player_status = driver.execute_script("return document.getElementById('movie_player').getPlayerState()")
        #     if player_status == -1:
        #         print("playing ads")
        #     value = driver.find_element_by_class_name('ytp-ad-skip-button')
        #     if value:
        #         print("find adviter")
        # except NoSuchElementException:
        #     print('no ads')
        # time.sleep(0.5)
        # if time.time() > end_time:
        #     break


def firxfox_test():
    driver = webdriver.Chrome(executable_path=r'../../chromedriver_win32\chromedriver.exe')
    # driver = webdriver.Firefox(executable_path=r'../../geckodriver-v0.23.0-win64/geckodriver.exe')
    # url = "https://www.youtube.com/watch?v=XYypsQOhQXE"
    url = "https://www.youtube.com/watch?v=Dz4Vq7hZtqo"
    # url = "http://www.google.com"
    watchtime = 180
    driver.get(url)
    wait = WebDriverWait(driver , 5)
    # while True:
    #     ad_elem = driver.find_element_by_class_name('ytp-ad-skip-button')
    #     print(ad_elem)
    #     time.sleep(1)

    ## get watch state: play or not play
    movie_player = driver.find_element_by_id('movie_player')
    player_status = driver.execute_script("return document.getElementById('movie_player').getPlayerState()")

    '''
    			Player_state = 0 means end
			Player_state = 1 means playing
			Player_state = -1 means advertise

    '''
    # player_status1 = movie_player.get_player_state()
    print("current play status: ", player_status)
    # print("current play status: ", player_status1)
    while True:
        try:
            ad_elem = driver.find_element_by_class_name('ytp-ad-skip-button')
            time.sleep(5)
            # print(ad_elem)
            ad_elem.click()
        except NoSuchElementException:
            print("button does not found.")
        time.sleep(1)


def skip_ads():
    # driver = webdriver.Chrome(executable_path=r'../../chromedriver_win32\chromedriver.exe')
    driver = webdriver.Firefox(executable_path=r'../../geckodriver-v0.23.0-win64/geckodriver.exe')
    url = "https://www.youtube.com/watch?time_continue=1&v=1KrMEsg7hr4"
    # url = "http://www.google.com"
    driver.get(url)
    # driver.manage().window().maximize()
    # driver.set_window_size(1920, 1200)
    driver.maximize_window()
    # player_status = driver.execute_script("return document.getElementById('movie_player').getPlayerState()")
    # print(player_status)
    # movie_player = driver.find_element_by_id('movie_player')
    # print(movie_player)
    try:
        ad_elem = driver.find_element_by_class_name('branding-img-container')
        # ad_elem1 =
        print(ad_elem)
        '''
        ad properties
        id = 
        ytp-ad-skip-button
        
        '''
        # player_status = driver.execute_script("return document.getElementById('branding-img-container').getPlayerState()")
        # print("play status: ", player_status)
        ad_elem.click()
    except:
        print("advertise cannot be clicked. ")
    time.sleep(5)
    # movie_player.click()

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
            # browser.set_window_size(1048, 786)
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
    # skip_ads()
    test()
    # firxfox_test()
    # wait_until_example()