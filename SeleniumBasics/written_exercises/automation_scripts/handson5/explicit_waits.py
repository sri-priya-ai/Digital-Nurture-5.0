import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

PLAYGROUND_URL = "https://www.lambdatest.com/selenium-playground/"


def success_alert_with_explicit_wait(browser):
    browser.get(PLAYGROUND_URL + "bootstrap-alert-messages/")
    success_btn = browser.find_element(By.XPATH, "//button[text()='Success Message']")
    success_btn.click()

    alert_box = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    assert "successfully" in alert_box.text.lower()
    print("Alert text found ->", alert_box.text)


def compare_sleep_vs_explicit_wait(browser):
    browser.get(PLAYGROUND_URL + "bootstrap-alert-messages/")

    start_sleep = time.time()
    browser.find_element(By.XPATH, "//button[text()='Success Message']").click()
    time.sleep(3)
    _ = browser.find_element(By.CSS_SELECTOR, ".alert-success")
    sleep_duration = time.time() - start_sleep

    browser.get(PLAYGROUND_URL + "bootstrap-alert-messages/")

    start_wait = time.time()
    browser.find_element(By.XPATH, "//button[text()='Success Message']").click()
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
    )
    wait_duration = time.time() - start_wait

    print(f"time.sleep(3) approach took {sleep_duration:.2f}s")
    print(f"explicit wait approach took {wait_duration:.2f}s")


def click_when_clickable(browser):
    browser.get(PLAYGROUND_URL + "bootstrap-alert-messages/")
    clickable_btn = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Success Message']"))
    )
    clickable_btn.click()


def fluent_wait_demo(browser):
    from selenium.webdriver.support.wait import WebDriverWait as FluentWDWait

    browser.get(PLAYGROUND_URL + "table-sort-search-highlight/")

    fluent = FluentWDWait(
        browser,
        timeout=10,
        poll_frequency=0.5,
        ignored_exceptions=[NoSuchElementException],
    )
    first_row = fluent.until(lambda d: d.find_element(By.CSS_SELECTOR, "table tbody tr"))
    print("First table row text:", first_row.text)


if __name__ == "__main__":
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service)
    try:
        success_alert_with_explicit_wait(drv)
        compare_sleep_vs_explicit_wait(drv)
        click_when_clickable(drv)
        fluent_wait_demo(drv)
    finally:
        drv.quit()
