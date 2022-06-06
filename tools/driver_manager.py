from selenium import webdriver
import time


class DriverManager:
    def __init__(self, user_login: str, user_password: str) -> None:
        # user settings
        self.user_login = user_login
        self.user_password = user_password

        self.driver = self.__initial_driver()

        # urls 
        self.__bitrix24_auth_url = "https://auth2.bitrix24.net/oauth/authorize/"

    def __initial_driver(self) -> webdriver.Firefox:

        # options for web driver
        options = webdriver.FirefoxOptions()

        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0")

        driver = webdriver.Firefox(options=options, 
            executable_path="tools/geckodriver.exe")

        return driver

    def auth_bitrix24(self) -> None:
        self.driver.get(self.__bitrix24_auth_url)
        time.sleep(3)

        input_login = self.driver.find_element_by_id("login")
        input_login.clear()
        input_login.send_keys(self.user_login)
        time.sleep(2)

        next_button = self.driver.find_element_by_class_name("b24-network-auth-form-btn").click()
        time.sleep(3)

    
    def finish(self):
        self.driver.close()
        self.driver.quit()
