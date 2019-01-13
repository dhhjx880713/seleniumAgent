from selenium import webdriver
from utils.tools import load_json_file
from selenium.common.exceptions import NoSuchElementException
import time
IGNORED_EXCEPTIONS = (NoSuchElementException,)



class SelenuimOP(object):

    def __init__(self, driver_type='Firefox', config_file='./config', debug=False):
        self.driver_type = driver_type
        self.config = load_json_file(config_file)
        self.debug = debug

    def youtube_click(self, task, shutdown_flag):
        ## driver can be created from task
        if self.driver_type == 'Firefox':
            driver = webdriver.Firefox(executable_path=self.config["driver_setting"]["firefox"])
        elif self.driver_type == 'Chrome':
            driver = webdriver.Chrome(executable_path=self.config["driver_setting"]["chrome"])
        else:
            raise  NotImplementedError

        try:
            end_time = time.time() + task['watchingtime'] * 60  ## minutes to seconds
            driver.get(task['url'])
            time_clip = 0.5
            while not shutdown_flag.is_set() and time.time() < end_time:
                try:
                    player = driver.find_element_by_id("movie_player")
                    if player:  ## if this is a youtube video
                        player_state = driver.execute_script(
                            "return document.getElementById('movie_player').getPlayerState()")
                        '''
                        youtube player_state
                        Player_state = 0 means end
                        Player_state = 1 means playing
                        Player_state = -1 means advertise
                        '''
                        if player_state == -1:
                            if self.debug:
                                print("ad is playing")
                            try:
                                skip_button = driver.find_element_by_class_name('ytp-ad-skip-button')
                                if skip_button:
                                    print("find skip button, prepare click in 5 seconds")
                                    time.sleep(task['ad_watchingtime'])
                                    while True:
                                        try:
                                            skip_button.click()
                                            break
                                        except:
                                            time.sleep(0.1)
                            except NoSuchElementException:
                                print('no skip button!')
                        elif player_state > 0:  ### normal playing state

                            time.sleep(time_clip)  ### continue to play
                        elif player_state == 0:  ## for a very short video
                            break
                        else:
                            pass
                    else:
                        time.sleep(time_clip)
                except IGNORED_EXCEPTIONS:
                    if self.debug:
                        print('This is not a yoube video')
                    time.sleep(time_clip)
        except IGNORED_EXCEPTIONS:
            print("selenium open url failed")
        driver.quit()


