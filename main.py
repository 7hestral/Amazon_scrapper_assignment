import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import random
import sys
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

from element_finder.order_elements import Order_elements_retriver
from element_finder.signin_elements import Signin_elements_retriver
from google_profile import Google_profile
from parser.vanilla_parser import VanillaCAParser
def rand_sleep(min_seconds=2, max_seconds=5):
    """
    Wait a little while so we don't spam Amazon.
    """
    seconds = random.randint(min_seconds, max_seconds)
    print("Sleeping for %s seconds..." % seconds, end="")
    sys.stdout.flush()
    time.sleep(seconds)
    print("done.")

class Agent:

    def __init__(self, google_profile=None):

        options = Options()
        options.headless = False
        options.add_argument("--disable-gpu")
        options.add_experimental_option("detach", True)

        if google_profile is not None:
            options.add_argument(f"user-data-dir={google_profile.profile_path}")
            options.add_argument(f"profile-directory={google_profile.profile_name}")

        service = ChromeService(ChromeDriverManager().install())
        service.command_line_args().append('--verbose')
        self.driver = webdriver.Chrome(service=service, options=options)

        url = "https://amazon.ca/"
        self.driver.maximize_window()
        rand_sleep()
        self.driver.get(url)
        rand_sleep()
        self.driver.set_page_load_timeout(10)

        self.signin_elements = Signin_elements_retriver(self.driver)
        self.order_elements = Order_elements_retriver(self.driver)
        self.parser = VanillaCAParser()
    def login(self, email, password):
        rand_sleep(1, 2)
        try:
            self.signin_elements.get_signin_button().click()
        except NoSuchElementException:
            print("Already logged in")
            return
        rand_sleep()
        email_text_box = self.signin_elements.get_email_text_box()
        email_text_box.clear()
        email_text_box.send_keys(email)
        # Sometimes there is a Continue button after entering your email;
        # sometimes there isn't.
        try:
            continue_button = self.signin_elements.get_continue_button()
            continue_button.click()
            rand_sleep()
        except NoSuchElementException:
            print("No continue button found; ignoring...")
        
        password_text_box = self.signin_elements.get_password_text_box()
        password_text_box.clear()
        password_text_box.send_keys(password)

        submit_button = self.signin_elements.get_submit_button()
        submit_button.click()
        print("Credential submitted")
    
    def navigate_to_order_page(self, retry=5):
        while retry > 0:
            try:
                order_button = self.order_elements.get_order_list_button()
                order_button.click()
                return
            except Exception as e:
                print(e)
            retry -= 1

    def _scroll_and_click(self, button):
        self.driver.execute_script("arguments[0].scrollIntoView();", button)
        self.driver.execute_script("arguments[0].click();", button)

    def navigate_dropdown(self, option_text_lst):
        driver = self.driver
        dropdown_trigger = self.order_elements.get_dropdown_trigger()
        
        self._scroll_and_click(dropdown_trigger)
        rand_sleep(1, 2)

        dropdown_items = self.order_elements.get_dropdown_items()
        num_items = len(dropdown_items)
        for i in range(num_items):
            item = dropdown_items[i]
            data_value = item.get_attribute("data-value")

            # Only year and archived are required, other items have duplication
            # option_text_lst = ['year', 'archived']
            selected = False
            for text in option_text_lst:
                if text in data_value:
                    selected = True
                    break

            if selected:
                print(data_value)
                driver.execute_script("arguments[0].click();", item)
                rand_sleep(1, 3)
                self.navigate_order_details()
                try:
                    dropdown_trigger = self.order_elements.get_dropdown_trigger()
                    self._scroll_and_click(dropdown_trigger)
                    dropdown_items = self.order_elements.get_dropdown_items()
                except NoSuchElementException:
                    print("No such element: Can't find the dropdown trigger element or dropdown list")
                    return
                except TimeoutException:
                    print("Timeout: Can't find the dropdown trigger element. Reason: reached archived order")
                    return
            else:
                continue


    def navigate_order_details(self):
        # find out all the clickable ones
        driver = self.driver
        page_index = 0
        base_url = driver.current_url
        while True:
            start_index_str = f'{page_index}0'
            new_url = f"{base_url}&startIndex={start_index_str}"
            driver.get(new_url)
            page_index += 1 

            try:
                order_details_items = self.order_elements.get_order_detail_link()
            except NoSuchElementException:
                print("No such element: No order details button found at this page")
                return
            except TimeoutException:
                print("Timeout: No order details button found at this page")
                return 
            num_items = len(order_details_items)
            # iterate over them using indexing
            for i in range(num_items):
                
                item = order_details_items[i]
                self._scroll_and_click(item)
                self.order_elements.wait_for_page_load()
                rand_sleep(1,3)
                self.save_html()
                driver.back()

                self.order_elements.wait_for_page_load()
                rand_sleep(1,3)
                # refresh them each time go back
                order_details_items = self.order_elements.get_order_detail_link()
            
            
    
    def save_html(self):
        try:
            order_date = self.parser.parse_order_date_text(self.order_elements.get_order_date().text)
            order_number = self.parser.parse_order_number_text(self.order_elements.get_order_number().text)
            print(order_date)
            print(order_number)
        except NoSuchElementException:
            print("No such element: No order date or order number")
            return
        except TimeoutException:
            print("Timeout: No order date or order number")
            return 
        
        result_path = os.path.join('.', 'result_html')
        if not os.path.exists(result_path):
            os.mkdir(result_path)

        with open(os.path.join(result_path, f'{order_date}_{order_number}.html'), "w", encoding="utf-8") as file:
            file.write(self.driver.page_source)

    def clean_up(self):
        self.driver.quit()

if __name__ == '__main__':
    import config
    # can not use the default path to the chrome user data, need to be cp to a new directory
    # see https://stackoverflow.com/questions/70825917/selenium-common-exceptions-webdriverexception-message-unknown-error-devtoolsa for explanation
    profile_path = config.profile_path
    proifle_name = config.proifle_name
    email = config.email
    password = config.password

    dropdown_options = ["year", "archived"]


    my_profile = Google_profile(profile_path, proifle_name)
    try:
        agent = Agent(google_profile=my_profile)
        agent.login(email, password)
        agent.navigate_to_order_page()
        agent.navigate_dropdown(dropdown_options)
        

    except Exception as e:
        print(e)
    finally:
        agent.clean_up()
    
