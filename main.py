from tools import DriverManager
import config

def main():
    driver_manager = DriverManager(user_login=config.USER_LOGIN, user_password=config.USER_PASSWORD)
    # , bitrix_name="b24-xx803c.bitrix24.ru"
    try:
        driver_manager.auth_bitrix24()

        driver_manager.parse_bitrix24_usertasks()
    except Exception as error:
        print(f"{error=}")
    finally:
        driver_manager.finish()

if __name__ == "__main__":
    main()



