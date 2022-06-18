import datetime
from tools import BitrixWorker

def now_format_date() -> str:
    format_date = datetime.datetime.now().strftime("%d_%m_%Y__%H_%M")
    return format_date

def main():
    format_date = now_format_date()
    worker = BitrixWorker(format_date)
    worker.run_worker()
   
if __name__ == "__main__":
    main()


