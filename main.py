from tools import DriverManager, ExelManager
import config, os

def main():
    
    # create managers driver & exel
    driver_manager = DriverManager(user_login=config.USER_LOGIN, user_password=config.USER_PASSWORD, 
                    bitrix_name=config.USER_BITRIX_NAME)
    exel_manager = ExelManager(dir_json=config.DIR_JSON, dir_exel=config.DIR_EXEL)
    
    try:
        # authtarizate in bitrix24
        driver_manager.auth_bitrix24()

        # parse usertasks from profile in bitrix24
        driver_manager.parse_bitrix24_usertasks()

        # write to json file usertasks info
        driver_manager.write_to_file_time_table_blocks_data()
        
        # close driver manager
        driver_manager.finish()
        
        # write data to exel file from json file
        exel_manager.write_exel_data()

    except Exception as error:
        print(f"{error=}")

if __name__ == "__main__":
    main()



