from selenium.webdriver.common.by import By
from .base_page import BasePage


class CheckboxPage(BasePage):
    CHECKBOX_LIST = (By.CSS_SELECTOR, "#colorbox input[type='checkbox']")

    def _get_checkbox(self, index):
        boxes = self.driver.find_elements(*self.CHECKBOX_LIST)
        return boxes[index - 1]

    def check_option(self, index):
        box = self._get_checkbox(index)
        if not box.is_selected():
            box.click()

    def uncheck_option(self, index):
        box = self._get_checkbox(index)
        if box.is_selected():
            box.click()

    def is_option_checked(self, index):
        return self._get_checkbox(index).is_selected()
