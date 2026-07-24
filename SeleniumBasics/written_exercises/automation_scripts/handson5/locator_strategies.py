from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

PLAYGROUND_URL = "https://www.lambdatest.com/selenium-playground/"


def locate_message_box_all_ways(browser):
    browser.get(PLAYGROUND_URL + "simple-form-demo/")

    by_id = browser.find_element(By.ID, "user-message")
    by_name = browser.find_element(By.NAME, "message")
    by_class = browser.find_element(By.CLASS_NAME, "form-control")
    by_tag = browser.find_element(By.TAG_NAME, "input")

    by_xpath_abs = browser.find_element(
        By.XPATH, "/html/body/div[3]/div/div/div[3]/div[1]/form/div[1]/input"
    )
    by_xpath_rel = browser.find_element(By.XPATH, "//input[@id='user-message']")

    found = [by_id, by_name, by_class, by_tag, by_xpath_abs, by_xpath_rel]
    print("All 6 locators pointed to the same element:",
          all(el.get_attribute("id") == "user-message" for el in found))

    css_by_id = browser.find_element(By.CSS_SELECTOR, "#user-message")
    css_by_attr = browser.find_element(By.CSS_SELECTOR, "[name='message']")
    css_by_parent = browser.find_element(By.CSS_SELECTOR, "div.form-group > input")
    print("CSS selectors also matched:",
          css_by_id.get_attribute("id") == css_by_attr.get_attribute("id") == css_by_parent.get_attribute("id"))


def locate_checkbox_labels(browser):
    browser.get(PLAYGROUND_URL + "checkbox-demo/")

    exact_match = browser.find_elements(By.XPATH, "//label[text()='Option 1']")
    contains_match = browser.find_elements(By.XPATH, "//label[contains(text(),'Option')]")

    print("Exact text() match count:", len(exact_match))
    print("contains() match count:", len(contains_match))


if __name__ == "__main__":
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service)
    try:
        locate_message_box_all_ways(drv)
        locate_checkbox_labels(drv)
    finally:
        drv.quit()
