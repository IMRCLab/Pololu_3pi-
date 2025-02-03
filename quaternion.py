import math
import struct

class Quaternion():
    def __init__(self,comp:int) -> None:
        self._x, self._y, self._z, self._w = self.quatdecompress(comp)
        self._roll = None
        self._pitch = None
        self._yaw = math.atan2(2*(self._w*self._z+self._x*self._y),1-2*(self._y**2+self._z**2))
    
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
    def roll(self):
        if self.roll == None:
            self._roll = math.atan2(2*(self._w*self._x+self._y*self._z),1-2*(self._x**2+self._y**2))
        return self._roll

    @property
    def pitch(self):
        if self.pitch == None:
            self._pitch = -math.pi/2 +math.atan2(math.sqrt(1+2*(self._w*self._y-self._x*self._z)),math.sqrt(1-2*(self._w*self._y-self._x*self._z)))
        return self._pitch

    @property
    def yaw(self):
        return self._yaw
    

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
    
    def calc_rotational_matrix(self)-> list:
        x = self._x
        y = self._y
        z = self._z
        w = self._w
        # for the quaternion q = w +xi +yj +zk
        return [
        [1 - 2*y**2 - 2*z**2, 2*x*y - 2*w*z, 2*x*z + 2*w*y],
        [2*x*y + 2*w*z, 1 - 2*x**2 - 2*z**2, 2*y*z - 2*w*x],
        [2*x*z - 2*w*y, 2*y*z + 2*w*x, 1 - 2*x**2 - 2*y**2]
        ]