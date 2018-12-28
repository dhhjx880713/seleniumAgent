from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def open_google_and_search():
    driver = webdriver.Chrome(executable_path=r'E:\tmp\chromedriver_win32\chromedriver.exe')
    driver.get("https://www.youtube.com/watch?v=qXqrEKWPgTI")
    # elem = driver.find_element_by_name("q")
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    time.sleep(10)
    driver.close()
    time.sleep(10)

def open_url():
    driver = webdriver.Chrome(executable_path=r'E:\tmp\chromedriver_win32\chromedriver.exe')
    # driver.get(r"E:\tmp\Welcome to Python.org.html")
    driver.switch_to.frame("test")
    driver.get("http://www.python.org")
    # print(driver.title)
    # assert "Python" in driver.title
    # elem = driver.find_element_by_name("q")
    # elem.clear()
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # assert "No results found." not in driver.page_source
    # driver.close()




# def remoteWebDriver():
#     from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#
#     driver = webdriver.Remote(
#         command_executor='http://127.0.0.1:4444/wd/hub',
#         desired_capabilities=DesiredCapabilities.CHROME)
#
#     # driver = webdriver.Remote(
#     #     command_executor='http://127.0.0.1:4444/wd/hub',
#     #     desired_capabilities={'browserName': 'chrome',
#     #                           'version': '2',
#     #                           'javascriptEnabled': True})

if __name__ == "__main__":
    # open_url()
    open_google_and_search()