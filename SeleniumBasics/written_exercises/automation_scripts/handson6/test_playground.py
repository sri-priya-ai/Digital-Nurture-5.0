import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def test_checkbox_demo(driver, base_url):
    driver.get(base_url + "checkbox-demo/")

    first_checkbox = driver.find_element(By.ID, "isAgeSelected")
    first_checkbox.click()
    assert first_checkbox.is_selected() is True

    first_checkbox.click()
    assert first_checkbox.is_selected() is False


def test_dropdown_selection(driver, base_url):
    driver.get(base_url + "select-dropdown-list/")

    day_dropdown = Select(driver.find_element(By.ID, "select-demo"))
    day_dropdown.select_by_visible_text("Wednesday")

    chosen = day_dropdown.first_selected_option
    assert chosen.text == "Wednesday"


@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission(driver, base_url, message):
    driver.get(base_url + "simple-form-demo/")

    input_box = driver.find_element(By.ID, "user-message")
    input_box.send_keys(message)
    driver.find_element(By.CSS_SELECTOR, "#single-input button").click()

    result = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message"))
    )
    assert result.text == message
