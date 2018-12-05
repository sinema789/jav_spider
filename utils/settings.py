import os

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"

URL = "https://www.seedmm.cc/"

MAX_WORKERS = 100

MAX_PAGE = 100

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_PATH = os.path.join(BASE_DIR, "logs/log_file_")

SAVE_PATH = os.path.join(BASE_DIR, "save/")

PIC_PATH = os.path.join(SAVE_PATH, "pictures/")

EXCEL_PATH = os.path.join(SAVE_PATH, "movie_info.xls")