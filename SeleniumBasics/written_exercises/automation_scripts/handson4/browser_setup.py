from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

PLAYGROUND_URL = "https://www.lambdatest.com/selenium-playground/"


def open_playground_and_print_title(headless=False):
    chrome_opts = Options()
    if headless:
        chrome_opts.add_argument("--headless=new")
        chrome_opts.add_argument("--window-size=1280,800")

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=chrome_opts)

    browser.implicitly_wait(10)

    browser.get(PLAYGROUND_URL)
    page_title = browser.title
    print("Page title is:", page_title)

    browser.quit()
    return page_title


if __name__ == "__main__":
    open_playground_and_print_title(headless=False)
    open_playground_and_print_title(headless=True)
