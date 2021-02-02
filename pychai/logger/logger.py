from logging import Formatter, LogRecord

class BinaryDictFormatter(Formatter):
    def format(self, record: LogRecord):
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
