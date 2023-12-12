from pythonjsonlogger import jsonlogger

from datetime import datetime


class JsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(JsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['message'] = log_record['message'].replace('\x1b[m', '').replace('\x1b[0m', '')

        if not log_record.get('timestamp'):
            log_record['timestamp'] = datetime.utcnow().strftime('%H:%M:%S %d.%m.%Y')

        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

formatter = JsonFormatter('%(level)s %(name)s %(message)s')
# formatter = JsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')