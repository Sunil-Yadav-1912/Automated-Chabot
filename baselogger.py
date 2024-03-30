import logging
from cloudwatch_handler import CloudWatchLogHandler
# logger = loggings
# logger.basicConfig(filename='record.log', level=logging.DEBUG)
log = logging
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = log.getLogger()
logger.setLevel(log.INFO)
formatter = log.Formatter(log_format, "%Y-%m-%d %H:%M:%S")

# File logging

file_handler = log.FileHandler('record.log', mode='a')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Cloudwatch logging

cloudwatch_handler = CloudWatchLogHandler()
cloudwatch_handler.setFormatter(formatter)
logger.addHandler(cloudwatch_handler)
