from scapy.all import *
import copy
class TLVError(Exception):
    pass


class TLV:
    def __init__(self, tl_in_l=False, t_ext=0, l_ext=0):
        self.buffer = ""
        self.tl_in_l = tl_in_l
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

        holdstr = chr(holder | extend) + holdstr
        return holdstr

    def _t(self, t):
        if self.t_ext == 0 and t > 256:
            raise TLVError("type > 256 and no extension bit set")
        return self._int(t, self.t_ext)


    def _l(self, l):
        if self.l_ext == 0 and l > 256:
            raise TLVError("length > 256 and no extension bit set")
        return self._int(l, self.l_ext)


    def add(self, t, v, l=None):
        deal_v = msg_dic[t][0]


        self.buffer += self._t(t)
        length = 0 if l is None else l

        if self.tl_in_l:
            length += t

        if l is None:
            length += len(v)

        self.buffer += self._l(length)
        self.buffer += v

    def pop_buf(self):
        buf = copy.deepcopy(self.buffer)
        self.buffer = ""
        return buf


    def __str__(self):
        return self.buffer

    def __repr__(self):
        return self.buffer



class TLVParser:
    def __init__(self, buffer, tl_in_l=False, t_ext=0, l_ext=0, socket=0):
        self.buffer = buffer
        self.tl_in_l = tl_in_l
        self.t_ext = t_ext
        self.l_ext = l_ext
        self.offset = 0
        self.socket = socket


    def _get_i(self, i_ext):
        try:
            byte = ord(self.buffer[self.offset])
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
                byte = ord(self.buffer[self.offset])
            except IndexError:
                raise TLVError("Not enough data")
        i += byte
        self.offset += 1
        return i


    def _get_tlv(self):
        off = self.offset
        t = self._get_i(self.t_ext)
        l = self._get_i(self.l_ext)
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
                "type": t,
                "length": l,
                "value": v,
                }
            except TLVError:
                self.add_buf(self.socket.recv(1024))
                print('----recv again---')
            # yield is similar to return
            # the different thing is that yield is not "static"
            # after yield a value the function do not quit
            # instead it remain its status and waiting for the next call

    def set_socket(self,socket):
        self.socket = socket

    def add_buf(self,buf):
        self.buffer+=buf

# # Test/example program for building TLVs and parsing the TLVs
# if __name__ == "__main__":
#     tlv = TLV(t_ext = conf.T_EXT, l_ext= conf.L_EXT)
#     tlv.add(10, "Foobar")
#     tlv.add(16, "Bladibla")


#     fhead = struct.pack('128sl',os.path.basename(conf.FILEPATH),
#                             os.stat(conf.FILEPATH).st_size)
#     tlv.add(3,fhead)





#     # hexdump(tlv)
#     tlvp = TLVParser(tlv.buffer, t_ext = conf.T_EXT, l_ext= conf.L_EXT)
#     for avp in tlvp.parse():
#         if avp["type"] == 3:
#             filename,filesize = struct.unpack('128sl',avp["value"])
#             filename = filename.strip('\00')
#             print ("%d(%d): %s,%ld" % (avp["type"], avp["length"], filename,filesize))
#         else:
#             print ("%d(%d): %s" % (avp["type"], avp["length"], avp["value"]))