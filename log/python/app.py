import logging
import requests
import json

class LokiHandler(logging.Handler):
    def __init__(self, loki_url):
        super().__init__()
        self.loki_url = loki_url

    def emit(self, record):
        log_entry = self.format(record)
        headers = {
            'Content-type': 'application/json',
        }
        data = {
            "streams": [
                {
                    "stream": {
                        "logger": record.name,
                        "level": record.levelname
                    },
                    "values": [
                        [str(int(record.created * 1e9)), log_entry]
                    ]
                }
            ]
        }
        response = requests.post(self.loki_url, headers=headers, data=json.dumps(data))
        if response.status_code != 204:
            print(f"Failed to send log to Loki: {response.content}")

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('example')
loki_handler = LokiHandler("http://localhost:3100/loki/api/v1/push")
logger.addHandler(loki_handler)

# Example log messages
logger.debug('This message should go to the log file')
logger.info('So should this')
logger.warning('And this, too')
logger.error('And non-ASCII stuff, too, like Øresund and Malmö')