# import logging

# import config
# from cloudwatch_handler import CloudWatchLogHandler


# class GlobalLogger:
#     def __init__(self, ):
#         self.logger = logging.getLogger()
#         log_level = logging.DEBUG if config.LEVEL == 'INFO' else logging.INFO
#         self.logger.setLevel(log_level)
#         log_format = '%(asctime)s - %(levelname)s - %(message)s'
#         formatter = logging.Formatter(log_format, "%Y-%m-%d %H:%M:%S")
#         if config.LOG_HANDLER == 'cloudwatch':
#             cloudwatch_handler = CloudWatchLogHandler()
#             cloudwatch_handler.setFormatter(formatter)
#             self.logger.addHandler(cloudwatch_handler)
#         if config.LOG_HANDLER == 'file':
#             file_handler = logging.FileHandler('logger.log', mode='a')
#             file_handler.setFormatter(formatter)
#             self.logger.addHandler(file_handler)
#         else:
#             console_handler = logging.StreamHandler()
#             console_handler.setFormatter(formatter)
#             self.logger.addHandler(console_handler)
