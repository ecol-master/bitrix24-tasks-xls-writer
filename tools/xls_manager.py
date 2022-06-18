import xlsxwriter
from .settings import XLS_FOLDER

class XlsWriter:
    """"""

    def __init__(self, format_date: str, data: list[dict, ...]) -> None:
        # date for files names xls & json
        self.__format_date = format_date
        
        # writable data
        self.__data = data
        
        self.__filename = "{}report_{}.xls".format(XLS_FOLDER, self.__format_date)

        self.__workbook = xlsxwriter.Workbook(self.__filename)
        self.__worksheet = self.__workbook.add_worksheet()
        
    def run_xls_writer(self):
        self.__write_headers_file()

        for col, header in enumerate(self.__data[0].keys()):
            self.__write_one_col_file(col=col, key=header)

        self.__workbook.close()
    
    def __write_headers_file(self):
        headers_list = self.__data[0].keys()

        for index, header in enumerate(headers_list):
            self.__worksheet.write(0, index, header)

    def __write_one_col_file(self, col: int, key: str):
        info = [obj[key] for obj in self.__data]
        for index, item in enumerate(info):
            self.__worksheet.write(index + 1, col, item)