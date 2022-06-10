import json, xlsxwriter, datetime

class ExelManager:

    """Params:  
        keys_to_write - list with keys wich wiil be write to file
        sorted_by - here you can pass the keys to sort the record """
    def __init__(self,
            dir_json: str,
            dir_exel: str,
            keys_to_write : list = None, 
            sorted_by : list = None,  
        ) -> None:

        self.__keys_to_write = keys_to_write
        self.__keys_sorted = sorted_by 

        self.__DIR_JSON = dir_json
        self.__DIR_EXEL = dir_exel

    """write to exel file data tasks"""
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

    """function returns exel filename"""
    def __get_exel_filename(self) -> str:
        format_data = self.__get_now_format_data()
        filename_exel = "{}report_{}.xls".format(self.__DIR_EXEL, format_data)
        return filename_exel

    """function return json data to write"""
    def __get_json_data(self) -> list[dict, ...]:   
        json_filename = self.__get_json_filename()
        with open(file=json_filename, mode="r") as json_file:
            data = json.load(json_file)
            data_with_certain_keys = self._get_data_with_certain_keys(data=data)
            sorted_data = self.__get_sort_json_data(data=data_with_certain_keys)
            return sorted_data
    
    """function return json filename"""
    def __get_json_filename(self) -> str:
        format_data = self.__get_now_format_data()
        filename_json = "{}report_{}.json".format(self.__DIR_JSON, format_data)
        return filename_json
    
    """function ruturns format date to files (exel & json) """
    def __get_now_format_data(self) -> str:
        format_data = datetime.datetime.now().strftime("%d_%m_%Y")
        return format_data

    """"""
    def _get_data_with_certain_keys(self, data: list[dict, ...]) -> list[dict, ...]:
        if self.__keys_to_write is None:
            return data
        data_with_certain_keys = list(map(
                lambda data_block: self.__get_one_data_with_certain_keys(data), data
                    ))             
        return data_with_certain_keys
    
    """"""
    def __get_one_data_with_certain_keys(self, data: dict) -> dict:
        return {key: data[key] for key in self.__keys_to_write}

    """"""
    def __get_sort_json_data(self, data: list[dict, ...]) -> list[dict, ...]: 
        if self.__keys_sorted is None:
            return data
        sorted_data = sorted(data, key=lambda data_block: (data_block[key] for key in self.__keys_sorted))
        return sorted_data

    """"""
    def __write_headers_exel(self, worksheet, data: list[dict, ...]) -> None:
        for index, name_title in enumerate(list(data[0].keys())):
            worksheet.write(0, index, name_title)

    """"""
    def __write_one_row_to_file(self, worksheet, row: int, key: str, data: list[dict, ...]) -> None:
        params = [obj[key] for obj in data] 
        print(params)
        for index, title in enumerate(params):
            worksheet.write(index + 1, row, title)