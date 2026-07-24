import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def base_url():
    return "https://www.lambdatest.com/selenium-playground/"


@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    chrome_driver = webdriver.Chrome(service=service)
    chrome_driver.maximize_window()
    yield chrome_driver
    chrome_driver.quit()
