import json, requests
from .exel_manager import XlsWriter

from .settings import BITRIX_DOMEN, BITRIX_KEY

class BitrixWorker:
    def __init__(self, format_date: str) -> None:
        
        # date for files names xls & json
        self.__format_date = format_date

        # user settings
        self.__user_domen = BITRIX_DOMEN
        self.__user_key = BITRIX_KEY
        
        # urls
        self.__url_tasks_api_template = "https://{}.bitrix24.ru/rest/1/{}/task.item.list.json"
        self.__url_elapsed_time_template = "https://{}.bitrix24.ru/rest/1/{}/task.elapseditem.getlist.json"

        # XlsWriter object, start_value - None
        self.__xls_writer = None

    def run_worker(self):

        data = self.get_json_data()

        self.__xls_writer = XlsWriter(format_date=self.__format_date, data=data)

        self.__xls_writer.run_xls_writer()














def write_json_data_tasks(format_date: str) -> None:
    
    # запрос для получения данных от битрикса
    url =  f"https://{BITRIX_DOMEN}.bitrix24.ru/rest/1/{BITRIX_KEY}/task.item.list.json"
    response = requests.get(url=url).json()

    filename = "json_{}.json".format(format_date)
    with open(file=filename, mode="w") as jsonfile:
        json.dump(response, jsonfile, ensure_ascii=False)


def write_json_data_times():
    url =  f"https://{BITRIX_DOMEN}.bitrix24.ru/rest/1/{BITRIX_KEY}/task.elapseditem.getlist.json"
    response = requests.get(url=url).json()

    filename = "json_time{}.json"
    with open(file=filename, mode="w") as jsonfile:
        json.dump(response, jsonfile, ensure_ascii=False)

write_json_data_times()

