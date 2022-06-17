import xlsxwriter


class XlsWriter:
    def __init__(self, format_date: str, data: list[dict, ...]) -> None:
        # date for files names xls & json
        self.__format_date = format_date
        
        # writable data
        self.__data = data
        
        self.__workbook = xlsxwriter.Workbook(filename)
        self.__worksheet = workbook.add_worksheet()
    
    def run_xls_writer(self):
        return "hello"