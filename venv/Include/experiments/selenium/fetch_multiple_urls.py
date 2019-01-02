import threading
from multiprocessing.pool import ThreadPool
from selenium import webdriver
from selenium.webdriver.phantomjs.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
import time


def fetch_url(url):
    # start = time.time()
    driver = webdriver.Chrome(executable_path=r'E:\tmp\chromedriver_win32\chromedriver.exe')
    # driver.switch_to.window("new window")
    driver.get(url)
    # time.sleep(60) ## play time
    # html = driver.page_source
    # print(html)
    # print("'%s\' fetched in %ss" % (url, (time.time() - start)))


def thread_task(lock,url):
    lock.acquire()
    fetch_url(url)
    lock.release()


if __name__ == "__main__":
    start = time.time()
    dataset =[
                    "https://www.youtube.com/watch?v=qXqrEKWPgTI",
                    "https://www.youtube.com/watch?v=_Sai8fN1FhU",
                    "https://www.youtube.com/watch?v=U-4d9qAKT9c",
                    "https://www.youtube.com/watch?v=yBr_8JCsQVE",
                    "https://www.youtube.com/watch?v=Ks0VhM_gFG8",
                ]

    with ThreadPool(5) as pool:
        pool.map(fetch_url, dataset, chunksize=1)
    print("Elapsed Time: %s" % (time.time() - start))
