import csv
import io
import logging
from datetime import datetime


class CsvFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        self.output = io.StringIO()
        self.writer = csv.writer(self.output, quoting=csv.QUOTE_ALL)

    def format(self, record):
        timestamp = datetime.utcfromtimestamp(record.created).isoformat()
        self.writer.writerow([timestamp] + list(record.args))

        data = self.output.getvalue()
        self.output.truncate(0)
        self.output.seek(0)
        return data.strip()
