# Bitrix24 Tasks Xls Writer

## Description of the project. 
The developed script allows the Bitrix24 user to collect and sort information about their tasks. Developed with the Python programming language. The basis of the code is classes for working with WebDriver (FireFox) and Xls files

---

## Libraries used in the project:

* selenium (for the script to work correctly, you need to [install]("https://github.com/mozilla/geckodriver/releases/") geckodriver for FireFox and, after unzipping, move the geckfriver.exe file to the tools directory.

![After installation, this structure should be obtained.](/additions/tools.png)
* xlsxwriter
* json
s* datetime
* asyncio
* time
---
## Code Examples

### Initial WebDriver Object

```py
# options for web driver
options = webdriver.FirefoxOptions()

options.add_argument("user-agent=USER_AGENT")

driver = webdriver.Firefox(options=options, 
    executable_path="tools/geckodriver.exe")
```
---
### Part Of The Authorization Function
```py
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
    ...
```
---
### Write Data To Xls File
```py
def write_exel_data(self) -> None:
    filename = self.__get_exel_filename()
        
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    data_write = self.__get_json_data()

    self.__write_headers_exel(worksheet, data_write)
        try:
            for index, key in enumerate(list(data_write[0].keys())):
                self.__write_one_row_to_file(worksheet, index ,key, data_write)
            
            workbook.close()

        except TypeError as type_error:
            print("Проверьте правильность данных для exel_manager")
```

