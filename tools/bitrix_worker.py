import json, requests, datetime
from .xls_manager import XlsWriter
from .settings import BITRIX_DOMEN, BITRIX_KEY


class BitrixWorker:
    """
    Сlass for managing requests and generating data for writing to xls file.
    Tt uses rest-api bitrix24 to receive data. For write to xls file uses another class - XlsWriter.
    """

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

        data = self.__get_json_data()

        self.__xls_writer = XlsWriter(format_date=self.__format_date, data=data)

        self.__xls_writer.run_xls_writer()

    def __get_json_data(self):
        tasks_data = self.__get_json_tasks_data()
        elapsed_times_data = self.__get_elapsed_times_data()

        data_for_write = self.__build_data_for_write(tasks_data=tasks_data, elapsed_times_data=elapsed_times_data)

        return data_for_write


    def __get_json_tasks_data(self) -> list[dict, ...]:
        url = self.__url_tasks_api_template.format(BITRIX_DOMEN, BITRIX_KEY)
        response = requests.get(url=url).json()
        return response["result"]

    def __get_elapsed_times_data(self) -> list[dict, ...]:
        url = self.__url_elapsed_time_template.format(BITRIX_DOMEN, BITRIX_KEY)
        response = requests.get(url=url).json()
        return response["result"]
    
    def __build_data_for_write(self, 
                tasks_data: list[dict, ...], 
                elapsed_times_data: list[dict, ...]
            ) -> list[dict, ...]:
        data_for_write = list()
       
        for elapsed_time_data in elapsed_times_data:
            task = self.__get_task_by_id(tasks_data, elapsed_time_data["TASK_ID"])
            user = self.__get_user_by_id(elapsed_time_data["USER_ID"])

            data_for_write.append(
                {
                    "Название задачи": task["TITLE"],
                    "Описание задачи":task["DESCRIPTION"],
                    "Коментарий к выполнению":elapsed_time_data["COMMENT_TEXT"],
                    "Имя сотрудника":" ".join([user['NAME'], user['LAST_NAME']]),
                    "Почта сотрудника":user["EMAIL"],
                    "Время выполнения":elapsed_time_data["MINUTES"],
                    "Дата начала выполнения":self.__get_format_date(elapsed_time_data["DATE_START"]),
                    "Дата окончания выполнения":self.__get_format_date(elapsed_time_data["DATE_STOP"]),
                    "":"",
                    "Контрагент":"",
                    "Постановщик":' '.join([task["CREATED_BY_NAME"], task["CREATED_BY_LAST_NAME"]]),
                    "Дата постановки":self.__get_format_date(task["CREATED_DATE"]),
                    "Общее время затраченное на задачу":task["DURATION_FACT"]
                }
            )
        return data_for_write


    def __get_task_by_id(self, tasks_data: list[dict, ...], task_id: str) -> dict:
        tasks_filter = list(filter(lambda task: task["ID"] == task_id, tasks_data))
        return tasks_filter[0]

    def __get_user_by_id(self, user_id: str):
        url = f"https://{BITRIX_DOMEN}.bitrix24.ru/rest/1/{BITRIX_KEY}/user.get.json?ID={user_id}"
        response = requests.get(url=url).json()
        return response["result"][0]

    def __get_format_date(self, date: str):
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
        return date_obj.strftime("%Y-%m-%d %H:%M")