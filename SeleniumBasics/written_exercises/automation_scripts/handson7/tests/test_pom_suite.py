import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage


def test_simple_form_submission(driver, base_url):
    form_page = SimpleFormPage(driver)
    form_page.navigate_to(base_url + "simple-form-demo/")
    form_page.enter_message("Hello Selenium")
    form_page.click_submit()

    assert form_page.get_displayed_message() == "Hello Selenium"


def test_checkbox_demo(driver, base_url):
    checkbox_page = CheckboxPage(driver)
    checkbox_page.navigate_to(base_url + "checkbox-demo/")

    checkbox_page.check_option(1)
    assert checkbox_page.is_option_checked(1) is True

    checkbox_page.uncheck_option(1)
    assert checkbox_page.is_option_checked(1) is False


def test_dropdown_selection(driver, base_url):
    dropdown_page = DropdownPage(driver)
    dropdown_page.navigate_to(base_url + "select-dropdown-list/")

    dropdown_page.select_day("Wednesday")
    assert dropdown_page.get_selected_day() == "Wednesday"


def test_input_form_submit(driver, base_url):
    input_page = InputFormPage(driver)
    input_page.navigate_to(base_url + "input-form-demo/")

    input_page.fill_form(
        name="Ravi Kumar",
        email="ravi.kumar@example.com",
        phone="9876543210",
        address="12 MG Road, Bengaluru",
    )
    input_page.submit_form()

    assert "Successfully" in input_page.get_success_message()
