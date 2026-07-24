from selenium.webdriver.common.by import By
from .base_page import BasePage


class InputFormPage(BasePage):
    NAME_FIELD = (By.NAME, "name")
    EMAIL_FIELD = (By.NAME, "email")
    PHONE_FIELD = (By.CSS_SELECTOR, "input[type='tel']")
    ADDRESS_FIELD = (By.NAME, "Address")
    SUBMIT_BTN = (By.CSS_SELECTOR, "input[type='submit']")
    SUCCESS_BANNER = (By.CSS_SELECTOR, ".alert-success")

    def fill_form(self, name, email, phone, address):
        self.wait_for_element(self.NAME_FIELD).send_keys(name)
        self.driver.find_element(*self.EMAIL_FIELD).send_keys(email)
        self.driver.find_element(*self.PHONE_FIELD).send_keys(phone)
        self.driver.find_element(*self.ADDRESS_FIELD).send_keys(address)

    def submit_form(self):
        self.driver.find_element(*self.SUBMIT_BTN).click()

    def get_success_message(self):
        return self.wait_for_element(self.SUCCESS_BANNER).text
