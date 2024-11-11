import math
import struct

class Quaternion():
    def __init__(self,comp:int) -> None:
        self._quaternion = self.quatdecompress(comp)
        self._x = self._quaternion[0]
        self._y = self._quaternion[1]
        self._z = self._quaternion[2]
        self._w = self._quaternion[3]

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def z(self):
        return self._z
    
    @property
    def w(self):
        return self._w
    
    @property
    def quaternion(self):
        return self._quaternion

    def quatdecompress(self,comp):
        q = [0,0,0,0]
        mask = (1 << 9) - 1
        i_largest = comp >> 30
        sum_squares = 0
        for i in range(3, -1, -1):
            if i != i_largest:
                mag = comp & mask
                negbit = (comp >> 9) & 0x1
                comp = comp >> 10
                q[i] = mag / mask / math.sqrt(2)
                if negbit == 1:
                    q[i] = -q[i]
                sum_squares += q[i] * q[i]
        q[i_largest] = math.sqrt(1.0 - sum_squares)
        return q 