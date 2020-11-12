import logging

FILENAME = 'pychai-debug.log'
DATE_FMT = '%Y-%m-%d %H:%M:%S'
MSG_FMT = '%(asctime)s|%(levelname)s|%(module)s - %(message)s'

class BinaryDictFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        msg = record.msg
        if isinstance(msg, dict):
            record.msg = '{'
            output = super().format(record) + '\n'
            for k,v in msg.items():
                binaryStr = bin(k)[2:]
                record.msg = f'{binaryStr:>20s} : {v.name:<4s} {k}'
                output += super().format(record) + '\n'
            record.msg = '}'
            output += super().format(record)
            record.msg = msg
            return output
        return super().format(record)

chaiLogger = logging.getLogger('binaryDictLogger')
bdHandler = logging.FileHandler(FILENAME, encoding='utf-8')
bdHandler.setLevel(logging.DEBUG)
bdHandler.setFormatter(BinaryDictFormatter(MSG_FMT, DATE_FMT))
chaiLogger.addHandler(bdHandler)
