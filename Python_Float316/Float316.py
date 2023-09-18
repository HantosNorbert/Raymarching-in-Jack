import math
import numpy as np
import struct


# Float316 is a floating point number stored in 3 16-bit registers:
# | sign | exponent | mantissa
#   where sign and exponent are like IEEE-754,
#   and mantissa is truncated to the first 13 bits, then padded by 001 on the left:
#   00 is for detecting overflow (required for some calculations),
#   1 is the hidden 1 not stored in IEEE-754.
#
# For example, 5.75 in IEEE-754 is:
# 0 | 10000001 | 01110000000000000000000
# In our case:
# 0 | 10000001 | 0010111000000000
# In decimal representation:
# 0 | 129 | 11776
# 
# The class supports signed zero.
# The class DOES NOT support borderline cases such as
#   infinities, NaNs, and subnormal numbers.
class Float316:
    def __init__(self, sign, exponent, mantissa):
        # convert to uint16 to make sure overflow happens as intended
        self.s = sign
        self.e = exponent
        self.m = mantissa
        # self.s = np.array(sign).astype(np.uint16)
        # self.e = np.array(exponent).astype(np.uint16)
        # self.m = np.array(mantissa).astype(np.uint16)

    def swapSign(self):
        self.s = 1 - self.s

    # an approximation of res = f1 * f2
    @staticmethod
    def mul(res, f1, f2):
        # sign = (s1 + s2) mod 2
        sign = (f1.s + f2.s) & 1

        # if either f1 or f2 is zero, the result is zero
        if (f1.e == 0 and f1.m == 0) or (f2.e == 0 and f2.m == 0):
            res.s = sign
            res.e = 0
            res.m = 0
            return
        
        # if one of the numbers are +1 or -1, return with the other
        if (f1.e == 127 and f1.m == 8192):
            res.s = sign
            res.e = f2.e
            res.m = f2.m
            return
        
        if (f2.e == 127 and f2.m == 8192):
            res.s = sign
            res.e = f1.e
            res.m = f1.m
            return
        
        # exponents are adding up, but correct it with the bias
		# exponent is shifted by 1 to correct the decimal point shift
		# in the mantissa multiplication
        exponent = f1.e + f2.e - 126

        # calculate the upper and lower 7 bits of the factors
        f1_m_high = f1.m // 128
        f1_m_low = f1.m & 127
        f2_m_high = f2.m // 128
        f2_m_low = f2.m & 127
        
        # multiply the matching pairs (ignoring res_low calculation
        # for gaining speed but losing minor accuracy)
        res_m_middle1 = f1_m_high * f2_m_low
        res_m_middle2 = f1_m_low * f2_m_high
        res_m_high = f1_m_high * f2_m_high

        # final mantissa
        mantissa = res_m_high + (res_m_middle1 + res_m_middle2) // 128

        # mantissa must start as 001; if not, shift the mantissa
        # and correct the exponent
        if mantissa != 0:
            while mantissa < 8192:
                mantissa = mantissa + mantissa
                exponent = exponent - 1
        
        res.s = sign
        res.e = exponent
        res.m = mantissa

    # True iff this > f
    def gt(self, f):
        # + > -
        if self.s != f.s:
            return f.s > self.s
        
        # exponent decides first, then mantissa
        # positive numbers
        if self.s == 0:
            if self.e != f.e:
                return self.e > f.e
            return self.m > f.m
        # negative numbers
        else:
            if self.e != f.e:
                return self.e < f.e
        
        return self.m < f.m
        
    # an approximation of res = f1 + f2
    @staticmethod
    def add(res, f1, f2):
        # instead of f1 + f2, we calculate bigger + smaller (in absolute terms)
        # so it's easier to handle negative numbers
        if f1.e < f2.e or (f1.e == f2.e and f1.m < f2.m):
            bigs = f2.s
            bige = f2.e
            bigm = f2.m
            smols = f1.s
            smole = f1.e
            smolm = f1.m
        else:
            bigs = f1.s
            bige = f1.e
            bigm = f1.m
            smols = f2.s
            smole = f2.e
            smolm = f2.m

        # special case of adding a zero
        if smole == 0 and smolm == 0:
            res.s = bigs
            res.e = bige
            res.m = bigm
            return

        # special case of a + -a = 0 (or -a + a = 0)
        if bigs != smols and bige == smole and bigm == smolm:
            res.s = 0
            res.e = 0
            res.m = 0
            return

        # adjust the exponent of the smaller number to match the bigger one
        exp_diff = bige - smole
        while exp_diff > 0:
            smolm = smolm // 2
            exp_diff = exp_diff - 1

        # the result will be stored in big
        # addition
        if bigs == smols:
            bigm = bigm + smolm
            # if there was an overflow, normalize (mantissa must start with 001)
            if bigm > 16383:  # 0011111...
                bigm = bigm // 2
                bige = bige + 1
        # substraction
        else:
            bigm = bigm - smolm
            # normalize (mantissa must start with 001)
            while bigm < 8192:  # 0010000...
                bigm = bigm + bigm
                bige = bige - 1

        res.s = bigs
        res.e = bige
        res.m = bigm

    # an approximation of res = f1 - f2
    @staticmethod
    def sub(res, f1, f2):
        f2.s = 1 - f2.s
        Float316.add(res, f1, f2)
        if f2 is not res:
            f2.s = 1 - f2.s

    # an approximation of res = f1 / f2
    @staticmethod
    def div(res, f1, f2):
        # sign = (s1 + s2) mod 2
        sign = (f1.s + f2.s) & 1

        # if f1 = 0, return 0
        if f1.e == 0 and f1.m == 0:
            res.s = sign
            res.e = 0
            res.m = 0
            return
        
        # if f2 = 0, trouble
        if f2.e == 0 and f2.m == 0:
            raise Exception("Null division!")
        
        # the new exponent is the difference, adjusted by the bias
        exponent = (f1.e + 127) - f2.e

        # mantissa division algorithm
        mantissa = 0
        m1 = f1.m
        m2 = f2.m
        i = 13
        while i > -1: 
            if m1 > m2:
                mantissa = mantissa + 2**i
                m1 = m1 - m2
            m2 = m2 // 2
            i = i - 1

        # normalize (mantissa must start with 001)
        while mantissa < 8192:
            mantissa = mantissa + mantissa
            exponent = exponent - 1

        res.s = sign
        res.e = exponent
        res.m = mantissa
    
    # res = x % 2, assuming f is a Float316 containing a rounded number
    # (for example, after a floor function was applied)
    @staticmethod
    def mod2(res, f):
        # We just have to peek at a specific position in the mantissa.
        # The position depends on the exponent.
        i = f.e - 127
        mask = 2**(13-i)

        # if the particular bit is 1, return with 1
        if f.m & mask > 0:
            res.s = 0
            res.e = 127
            res.m = 8192
            return
        # else, return with 0
        res.s = 0
        res.e = 0
        res.m = 0
    
    #####################################################################################
    # THESE ARE ONLY FOR TESTING
    #####################################################################################
    # print a representation
    def __str__(self):
        return f"{self.getValue()} | {self.s} | {bin(self.e)[2:].zfill(8)} | {bin(self.m)[2:].zfill(16)}"
    # def __str__(self):
    #     return f"{self.s}, {self.e}, {self.m}"

    # calculate the true float value
    def getValue(self):
        value = 0
        mantissa = bin(self.m)[2:].zfill(14)
        for i, bit in enumerate(mantissa):
            if bit == "1":
                value += 2**-i

        value = math.pow(-1, self.s) * value*math.pow(2.0, self.e - 127)
        return value

    # create a new Float316 from a given float number
    @staticmethod
    def create(value):
        value = np.array(value).astype(np.float32)
        binValue = ''.join(format(c, '08b') for c in struct.pack('!f', value))
        sign = int(binValue[0])
        exponent = int(binValue[1:9], 2)

        mantissa = binValue[9:]
        if exponent == 0 and int(mantissa, 2) == 0:
            return Float316(sign, 0, 0)

        mantissa_modified = "001" + mantissa[:13]
        final_mantissa = int(mantissa_modified, 2)
        return Float316(sign, exponent, final_mantissa)
