import boto3
import logging
from datetime import datetime
import config


class CloudWatchLogHandler(logging.Handler):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self,):
        super().__init__()
        self.log_group_name = config.CLOUDWATCH_GROUP
        self.log_stream_name = config.CLOUDWATCH_STREAM
        self.max_batch_size = 256000
        self.cloudwatch_logs = boto3.client('logs', aws_access_key_id=config.CLOUDWATCH_ACCESS_KEY,
                                            aws_secret_access_key=config.CLOUDWATCH_SECRET_KEY,
                                            region_name=config.AWS_REGION_NAME)
        if not self._log_stream_exists():
            self._create_log_stream()

    def _log_stream_exists(self):
        response = self.cloudwatch_logs.describe_log_streams(
            logGroupName=self.log_group_name,
            logStreamNamePrefix=self.log_stream_name
        )
        return any(stream['logStreamName'] == self.log_stream_name for stream in response['logStreams'])

    def _create_log_stream(self):
        self.cloudwatch_logs.create_log_stream(
            logGroupName=self.log_group_name,
            logStreamName=self.log_stream_name
        )

    def emit(self, record):
        log_message = self.format(record)
        timestamp = int(datetime.now().timestamp() * 1000)
        if len(log_message.encode('utf-8')) > self.max_batch_size:
            split_log_message = log_message[0:self.max_batch_size]
            log_message = log_message[self.max_batch_size:-1]
            self.cloudwatch_logs.put_log_events(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name,
                logEvents=[{
                    'timestamp': timestamp,
                    'message': split_log_message
                }]
            )
        self.cloudwatch_logs.put_log_events(
            logGroupName=self.log_group_name,
            logStreamName=self.log_stream_name,
            logEvents=[{
                'timestamp': timestamp,
                'message': log_message
            }]
        )
