from selenium.webdriver.common.by import By
from .base_page import BasePage


class SimpleFormPage(BasePage):
    MESSAGE_INPUT = (By.ID, "user-message")
    SUBMIT_BTN = (By.CSS_SELECTOR, "#single-input button")
    DISPLAYED_MESSAGE = (By.ID, "message")

    def enter_message(self, text):
        box = self.wait_for_element(self.MESSAGE_INPUT)
        box.clear()
        box.send_keys(text)

    def click_submit(self):
        btn = self.wait_for_clickable(self.SUBMIT_BTN)
        btn.click()

    def get_displayed_message(self):
        return self.wait_for_element(self.DISPLAYED_MESSAGE).text
