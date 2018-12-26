from selenium import webdriver
from selenium.webdriver.common.keys import Keys



def test():
    driver = webdriver.Chrome(executable_path=r'E:\tmp\chromedriver_win32\chromedriver.exe')
    driver.get("http://www.python.org")
    assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("pycon")
    elem.send_keys(Keys.RETURN)
    assert "No results found." not in driver.page_source
    # driver.close()


if __name__ == "__main__":
    test()