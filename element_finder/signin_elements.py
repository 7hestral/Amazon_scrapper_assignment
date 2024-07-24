
from selenium.webdriver.common.by import By


class Signin_elements_retriver:
    def __init__(self, driver) -> None:
        self.driver = driver

    def get_signin_button(self):
        return self.driver.find_element(By.XPATH, '//*[@id="nav-signin-tooltip"]/a/span')
    def get_email_text_box(self):
        return self.driver.find_element(By.XPATH, '//*[@id="ap_email"]')
    def get_password_text_box(self):
        return self.driver.find_element(By.XPATH, '//*[@id="ap_password"]')
    def get_continue_button(self):
        return self.driver.find_element(By.XPATH, '//*[@id="continue"]')
    def get_submit_button(self):
        return self.driver.find_element(By.XPATH, '//*[@id="signInSubmit"]')

    