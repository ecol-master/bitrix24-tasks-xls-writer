import datetime
from tools import write_json_data_tasks, ExelWriter

def now_format_date() -> str:
    format_date = datetime.datetime.now().strftime("%d_%m_%Y__%H_%M")
    return format_date

def main():

    format_date = now_format_date()
    write_json_data_tasks(format_date=format_date)


    writer_xls = ExelWriter(format_date=format_date)

    writer_xls.write_all_data_to_xls()

   
if __name__ == "__main__":
    main()


