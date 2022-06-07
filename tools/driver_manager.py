from selenium import webdriver
import time, os


class DriverManager:
    def __init__(self, user_login: str, user_password: str, bitrix_name="") -> None:
        # user settings
        self.__user_login = user_login
        self.__user_password = user_password
        self.__user_bitrix24_name = bitrix_name.lower()

        # work names
        self.driver = self.__initial_driver()
        
        self.__bitrix24_account_now = "" # account you are logged into
        self.tasks_count = 0

        # urls 
        self.__bitrix24_auth_url = "https://auth2.bitrix24.net/oauth/authorize/?user_lang=ru&client_id=site.53889571c72cf8.19427820&redirect_uri=https://www.bitrix24.ru/auth/?auth_service_id=Bitrix24Net&scope=auth,client&response_type=code&mode=page&state=site_id=ru&backurl=%2Fauth%2F%3Fcheck_key%3D0ded0e0219d61d967de2c356ece3e943&mode=page"
    
    def __initial_driver(self) -> webdriver.Firefox:

        # options for web driver
        options = webdriver.FirefoxOptions()

        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0")

        driver = webdriver.Firefox(options=options, 
            executable_path="tools/geckodriver.exe")

        return driver

    def auth_bitrix24(self) -> None:
        # get link auth
        self.driver.get(self.__bitrix24_auth_url)
        time.sleep(3)
        
        #
        input_login = self.driver.find_element_by_id("login")
        input_login.clear()
        input_login.send_keys(self.__user_login)
        time.sleep(2)

        self.driver.find_element_by_class_name("b24-network-auth-form-btn").click()
        time.sleep(3)

        input_password = self.driver.find_element_by_id("password")
        input_password.clear()
        input_password.send_keys(self.__user_password)
        time.sleep(2)

        self.driver.find_element_by_class_name("b24-network-auth-form-btn").click()
        time.sleep(7)
        self.driver.find_element_by_class_name("portal-auth-bitrix24__message").click()
        time.sleep(7)
        self.driver.find_element_by_class_name("bx-ui-button_primary").click()
        time.sleep(10)
        self.driver.find_element_by_class_name("portal-auth-bitrix24__user").click()
        time.sleep(2)

        bitrix24_account_links = self.driver.find_elements_by_class_name("portal-auth-bitrix24-window__link")[:-1]
        time.sleep(3)

        self.__click_account_in_auth(bitrix24_account_links=bitrix24_account_links)

    def __click_account_in_auth(self, bitrix24_account_links: list) -> None:
        if self.__user_bitrix24_name != "":
            accounts = {account.text.lower(): account for account in bitrix24_account_links}
            if accounts.get(self.__user_bitrix24_name) is None:
                self.__bitrix24_account_now = bitrix24_account_links[0].text
                bitrix24_account_links[0].click()
            else:
                self.__bitrix24_account_now = self.__user_bitrix24_name
                accounts[self.__user_bitrix24_name].click()
        else:
            self.__bitrix24_account_now = bitrix24_account_links[0].text
            bitrix24_account_links[0].click()
        time.sleep(3)

    def __get_tasks_links(self, tasks_count: int) -> list:
        url = "https://b24-tq78e8.bitrix24.ru/company/personal/user/1/tasks/task/view/{}/"
        links = [url.format(i) for i in range(2, tasks_count * 2 + 1, 2)]
        print(links)
        

    def parse_bitrix24_usertasks(self) -> None:
        self.driver.get(f"https://{self.__bitrix24_account_now.lower()}/company/personal/user/1/tasks/")
        time.sleep(3)
        self.driver.find_element_by_id("tasks_grid_role_id_4096_0_advanced_n_row_count").click()
        time.sleep(1)
        tasks_count = int(self.driver.find_element_by_id("tasks_grid_role_id_4096_0_advanced_n_row_count_wrapper").text.split(": ")[-1])
        self.__get_tasks_links(tasks_count=tasks_count)


    def finish(self):
        # self.driver.close()
        # self.driver.quit()
        # os.remove("geckodriver.log")
        pass