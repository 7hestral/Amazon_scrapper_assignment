

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Order_elements_retriver:
    def __init__(self, driver, timeout=10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def get_order_list_button(self):
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav-orders"]/span[2]')))
        return self.driver.find_element(By.XPATH, '//*[@id="nav-orders"]/span[2]')
    
    def get_dropdown_trigger(self):
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "a-dropdown-prompt")))
        return self.driver.find_element(By.CLASS_NAME, "a-dropdown-prompt")

    def get_dropdown_items(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'a-dropdown-item')]//a")))
        return self.driver.find_elements(By.XPATH, "//li[contains(@class, 'a-dropdown-item')]//a")

    def get_order_detail_link(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'order-details')]")))
        return self.driver.find_elements(By.XPATH, "//a[contains(@href, 'order-details')]")
    
    def wait_for_page_load(self):
        self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

    def get_order_date(self):
        self.wait_for_page_load()
        order_date_element = self.driver.find_element(By.XPATH, "//span[contains(@class, 'order-date-invoice-item')]")
        return order_date_element
    def get_order_number(self):
        self.wait_for_page_load()
        order_number_element = self.driver.find_element(By.XPATH, "//span[contains(@class, 'order-date-invoice-item')]//bdi")
        return order_number_element


