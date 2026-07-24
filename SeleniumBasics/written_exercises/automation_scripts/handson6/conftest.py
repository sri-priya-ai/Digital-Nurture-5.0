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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        node_fixtures = item.funcargs
        chrome_driver = node_fixtures.get("driver")
        if chrome_driver is not None:
            safe_name = item.name.replace("[", "_").replace("]", "")
            chrome_driver.save_screenshot(f"{safe_name}_failure.png")
