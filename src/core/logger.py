import logging
import threading
import os

logPath = 'log/app.log'
if not os.path.exists(os.path.dirname(logPath)):
    os.makedirs(os.path.dirname(logPath))
    with open(logPath, 'w') as f:
        pass

# class Logger:
#     _instance_lock = threading.Lock()

#     def __init__(self, name):
        
#         self.logger = logging.getLogger(name)
#         self.logger.setLevel(logging.DEBUG)

#         # 创建一个handler，用于写入日志文件
#         file_handler = logging.FileHandler(logPath)
#         file_handler.setLevel(logging.DEBUG)

#         # 创建一个handler，用于将日志输出到控制台
#         console_handler = logging.StreamHandler()
#         console_handler.setLevel(logging.DEBUG)

#         # 定义handler的输出格式
#         formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#         file_handler.setFormatter(formatter)
#         console_handler.setFormatter(formatter)

#         # 给logger添加handler
#         self.logger.addHandler(file_handler)
#         self.logger.addHandler(console_handler)
#         print("logger init")

#     def __new__(cls, *args, **kwargs):
#         if not hasattr(Logger, "_instance"):
#             with Logger._instance_lock:
#                 if not hasattr(Logger, "_instance"):
#                     Logger._instance = object.__new__(cls)  
#         print("logger new")
#         return Logger._instance

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(logPath)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)