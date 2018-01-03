import time
import select
import serial
import logging
import logging.handlers

class RflinkInterface:

    def __init__(self, device: object = "/dev/ttyACM0", speed: object = 57600, callback: object = None)  -> object:
        self.gotsignal = callback
        self.serial = serial.Serial( device , speed , timeout=0 )
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()
        self.epoll = select.epoll()
        self.epoll.register(self.serial.fileno(), select.EPOLLOUT)
        self.buf = ""

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

    def __emptySerialBuffer(self):
        res = []
        while True:
            data = self.serial.read( 1000 )
            if not data:
                break
            try:
                unicodeString = data.decode()
                res.append(unicodeString)
            except UnicodeDecodeError:
                self.logger.info("UnicodeDecodeError {0}".format(repr(data)))
                return ""

        return "".join(res)

    def __readline(self, data):
        self.logger.info("datas<{}>".format(data))
        self.buf += data
        lines = self.buf.splitlines()

        if not lines:
            return "", []

        if data[-1] == "\n":
            return "", lines

        return lines[-1], lines[:-1]

    def __read(self):
        res = self.__emptySerialBuffer()
        self.buf, lines = self.__readline(res)
        return lines

    def __iter__(self):
        return self

    def __next__(self):
        modify = select.EPOLLIN
        self.epoll.modify(self.serial.fileno(), modify)
        for event in self.epoll.poll(0.1) :
            fd, event = event
            if event & select.EPOLLIN:
                self.logger.debug("select.EPOLLIN")
                for r in self.__read() :
                    return r

        raise StopIteration



