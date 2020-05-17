import copy
import pickle
import logging

class TLVError(Exception):
    pass


class TLV:
    def __init__(self, t_len=2, l_len=2):
        self.buffer = bytearray()
        self.t_len = t_len
        self.l_len = l_len
        self.l_len = l_len

    def _int(self, i, len):
        try:
            return  i.to_bytes(len, byteorder='big')
        except OverflowError as e:
            logging.error('OverflowError!:type or length to_buffer failed.')

    def add(self, t, v):
        self.buffer += self._int(t,self.t_len)
        l = len(v)
        self.buffer += self._int(l,self.l_len)
        # logging.debug("TLV object added value: {}".format(v))
        self.buffer += v

    def add_obj(self, t, v):
        new_buf = pickle.dumps(v)
        self.buffer += self._int(t,self.t_len)
        l = len(new_buf)
        self.buffer += self._int(l,self.l_len)
        # logging.debug("TLV object added value: {},{}".format(t,v))
        self.buffer += new_buf

    def pop_buf(self):
        buf = copy.deepcopy(self.buffer)
        self.buffer = bytearray()
        return buf

    def __str__(self):
        return self.buffer

    def __repr__(self):
        return self.buffer



class TLVParser:
    def __init__(self, buffer=bytearray(), t_len=2, l_len=2, socket=0):
        self.buffer =bytearray()
        self.t_len = t_len
        self.l_len = l_len
        self.offset = 0
        self.socket = socket


    def _get_i(self, len):
        try:
            o_offset = self.offset
            self.offset += len
            i = int.from_bytes(self.buffer[o_offset:self.offset],byteorder='big')
            return i
        except Exception as e:
            logging.error('_get_i: get type or length failed!')


    def _get_tlv(self):
        off = self.offset
        t = self._get_i(self.t_len)
        logging.debug("try get tlv!:t:{}".format(t))
        l = self._get_i(self.l_len)
        logging.debug("try get tlv!:l:{}".format(l))
        if self.offset + l > len(self.buffer):
            self.offset = off
            raise TLVError("Buffer not long enough to encompass TLV")
        v = self.buffer[self.offset:self.offset+l]
        self.offset += l
        return (t, l, v)


    def parse(self):
        while self.offset < len(self.buffer):
            try:
                t, l, v = self._get_tlv()
                yield {
                "t": t,
                "l": l,
                "v": v,
                }
            except TLVError:
                self.add_buf(self.socket.recv(1024))
                logging.info("Incomplete buffer, recv(1024) again.")
            # yield is similar to return
            # the different thing is that yield is not "static"
            # after yield a value the function do not quit
            # instead it remain its status and waiting for the next call

    def parse_obj(self):
        logging.debug("parse_obj!")
        while self.offset < len(self.buffer):
            try:
                logging.debug("try get tlv!")
                t, l, v = self._get_tlv()
                logging.debug("try get tlv!:t:{}".format(t))
                obj = pickle.loads(v)
                yield {
                "t": t,
                "v": obj
                }
            except TLVError:
                self.add_buf(self.socket.recv(1024))
                logging.info("Incomplete buffer, recv(1024) again.")
            # yield is similar to return
            # the different thing is that yield is not "static"
            # after yield a value the function do not quit
            # instead it remain its status and waiting for the next call


    def set_socket(self,socket):
        self.socket = socket

    def add_buf(self,buf):
        self.buffer+=buf