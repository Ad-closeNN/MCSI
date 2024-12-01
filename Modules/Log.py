"""日志服务"""

import datetime
import os

def info(message):
    if not os.path.exists("Logs"):
        os.mkdir("Logs")
    with open("Logs/log.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S]')} [INFO] {message}\n")

def error(message):
    if not os.path.exists("Logs"):
        os.mkdir("Logs")
    with open("Logs/log.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S]')} [ERROR] {message}\n")
        
def warning(message):
    if not os.path.exists("Logs"):
        os.mkdir("Logs")
    with open("Logs/log.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S]')} [WARNING] {message}\n")

def debug(message):
    if not os.path.exists("Logs"):
        os.mkdir("Logs")
    with open("Logs/log.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now().strftime('[%Y/%m/%d %H:%M:%S]')} [DEBUG] {message}\n")