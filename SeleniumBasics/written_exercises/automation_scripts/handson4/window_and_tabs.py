import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

PLAYGROUND_URL = "https://www.lambdatest.com/selenium-playground/"


def run():
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)

    browser.get(PLAYGROUND_URL)
    form_link = browser.find_element("link text", "Simple Form Demo")
    form_link.click()

    time.sleep(1)
    current_url = browser.current_url
    assert "simple-form-demo" in current_url, f"Unexpected url: {current_url}"
    print("URL check passed ->", current_url)

    browser.back()

    browser.execute_script("window.open('https://www.google.com');")
    all_tabs = browser.window_handles
    print("Number of open tabs:", len(all_tabs))

    browser.switch_to.window(all_tabs[1])
    print("Second tab title:", browser.title)

    browser.switch_to.window(all_tabs[0])
    screenshot_ok = browser.save_screenshot("playground_screenshot.png")
    print("Screenshot saved:", screenshot_ok)

    size_before = browser.get_window_size()
    print("Window size before:", size_before)
    browser.set_window_size(1280, 800)
    size_after = browser.get_window_size()
    print("Window size after:", size_after)

    browser.quit()


if __name__ == "__main__":
    run()
