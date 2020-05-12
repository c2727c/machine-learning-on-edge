from scapy.all import *
import copy
import pickle
import logging

class TLVError(Exception):
    pass


class TLV:
    def __init__(self, t_ext=0, l_ext=0):
        self.buffer = bytearray()
        self.t_ext = t_ext
        self.l_ext = l_ext

    def _int(self, i, ext):
        maxi = 1<<8
        if ext > 0:
            maxi = (1 << ext)
        holdstr = ""
        holder = i 
        extend = 0 
        count = 1 
        while holder >= maxi:
            count += 1
            newnum = (holder & (maxi - 1)) 
            holdstr = chr(newnum | extend) + holdstr
            extend = maxi
            holder /= maxi

        holdstr = chr(int(holder) | int(extend)) + holdstr
        # logging.debug("int():{}-->{}".format(i, holdstr))
        print(holdstr.encode())
        return holdstr.encode()

    def _t(self, t):
        if self.t_ext == 0 and t > 256:
            raise TLVError("type > 256 and no extension bit set")
        return self._int(t, self.t_ext)

    def _l(self, l):
        if self.l_ext == 0 and l > 256:
            raise TLVError("length > 256 and no extension bit set")
        return self._int(l, self.l_ext)

    def add(self, t, v, l=None):
        self.buffer += self._t(t)
        length = 0 if l is None else l
        if l is None:
            length += len(v)
        self.buffer += self._l(length)
        # logging.debug("TLV object added value: {}".format(v))
        self.buffer += v

    def add_obj(self, t, v, l=None):
        new_buf = pickle.dumps(v)
        # deal_v = msg_dic[t][0]
        self.buffer += self._t(t)
        length = 0 if l is None else l
        if l is None:
            length += len(new_buf)
        self.buffer += self._l(length)
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
    def __init__(self, buffer=bytearray(), t_ext=0, l_ext=0, socket=0):
        self.buffer =bytearray()
        self.t_ext = t_ext
        self.l_ext = l_ext
        self.offset = 0
        self.socket = socket


    def _get_i(self, i_ext):
        o_offset = self.offset
        try:
            byte = self.buffer[self.offset]
        except IndexError:
            # If the IndexError is raised when the offset>=len
            
            raise TLVError("Not enough data")
        # Otherwise,'byte' is the next byte of data now
        # if i_ext=7, ext =     1000 0000(last i_ext(7) bits are 0) 
        #           ext-1 =     0111 1111(last i_ext(7) bits are 1) 
        # Otherwise,  ext = (1) 0000 0000
        ext = 1 << (i_ext if i_ext > 0 else 8)
        i = 0
        # copying data of i_ext
        while byte & ext:
            i += (byte & (ext - 1))#take the last i_ext(7) bits of the cur_byte
            i <<= i_ext#left shift i_ext bits,got i_ext(7) bits empty in the end
            self.offset += 1#moves to next cur_byte
            try:
                byte = self.buffer[self.offset]
            except IndexError:
                raise TLVError("Not enough data")
        i += byte
        self.offset += 1
        bts = self.buffer[o_offset:self.offset]
        # logging.debug("get_i():{}-->{}".format(bts,i))
        return i


    def _get_tlv(self):
        off = self.offset
        t = self._get_i(self.t_ext)
        logging.debug("try get tlv!:t:{}".format(t))
        l = self._get_i(self.l_ext)
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