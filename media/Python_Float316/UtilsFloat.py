from Float316 import Float316
from Constants import Constants

# A couple of functions that use Float316 variables
# for internal computations.
class UtilsFloat:
    # Variables for temporal computations
    SQRT_tmpRes = Float316(0, 0, 0)
    SQRT_xDivTmp = Float316(0, 0, 0)

    ISQRT_x2 = Float316(0, 0, 0)
    ISQRT_y = Float316(0, 0, 0)
    ISQRT_tmpRes = Float316(0, 0, 0)

    # res = floor(f), where both res and f are Float316 numbers.
    # floor(f) is always the biggest integer such that floor(f) <= f
    # Examples:
    #   floor(3.0) = 3.0
    #   floor(3.2) = 3.0
    #   floor(3.9) = 3.0
    #   floor(-3.0) = -3.0
    #   floor(-3.2) = -4.0
    #   floor(0.0) = 0.0
    @staticmethod
    def floor(res: Float316, f: Float316):
        exponent = f.e
        # if number is smaller than 1
        if exponent < 127:
            # if positive, return 0
            if f.s == 0:
                res.s = 0
                res.e = 0
                res.m = 0
                return
            # else, return -1
            res.s = 1
            res.e = 127
            res.m = 8192
            return

        # The actual rounding is just cropping the tail of the mantissa.
        # The length of the cropping depends on the exponent.
        i = f.e - 127
        mask = 65535 - (2**(13-i) - 1)
        mantissa = f.m & mask

        # The pseudo-result
        res.s = f.s
        res.e = exponent
        res.m = mantissa

        # But this is a floor on the absolute value.
        # If f is a negative number and it was not already a whole number,
        # we have to substract 1.
        if f.s == 1 and f.m != mantissa:
            Float316.add(res, res, Constants.CONST_MINUS_ONE)

    # res = sqrt(x)
    @staticmethod
    def sqrt(res: Float316, x: Float316):
        if x.s > 0:
            raise Exception("SQRT of a negative!")
        
        # sqrt(0) is 0
        if x.e == 0 and x.m == 0:
            res.e = 0
            res.m = 0
            return
        
        # initial guess: just half the exponent
        UtilsFloat.SQRT_tmpRes.s = 0
        # UtilsFloat.SQRT_TMP_RES.e = (x.e - 127) // 2 + 127
        if x.e & 1 > 0:
            UtilsFloat.SQRT_tmpRes.e = x.e // 2 + 64
        else:
            UtilsFloat.SQRT_tmpRes.e = x.e // 2 + 63
        UtilsFloat.SQRT_tmpRes.m = x.m

        # Newton-Raphson method with some iterations
        # res = 0.5 * (res + x/res)
        Float316.div(UtilsFloat.SQRT_xDivTmp, x, UtilsFloat.SQRT_tmpRes)
        Float316.add(UtilsFloat.SQRT_tmpRes, UtilsFloat.SQRT_tmpRes, UtilsFloat.SQRT_xDivTmp)
        UtilsFloat.SQRT_tmpRes.e = UtilsFloat.SQRT_tmpRes.e - 1

        # res = 0.5 * (res + x/res)
        Float316.div(UtilsFloat.SQRT_xDivTmp, x, UtilsFloat.SQRT_tmpRes)
        Float316.add(UtilsFloat.SQRT_tmpRes, UtilsFloat.SQRT_tmpRes, UtilsFloat.SQRT_xDivTmp)
        UtilsFloat.SQRT_tmpRes.e = UtilsFloat.SQRT_tmpRes.e - 1

        res.s = 0
        res.e = UtilsFloat.SQRT_tmpRes.e
        res.m = UtilsFloat.SQRT_tmpRes.m
    
    # res = 1.0 / sqrt(x)
    # Uses a simplified version of the "Fast Inverse Square Root" trick, see
    # https://en.wikipedia.org/wiki/Fast_inverse_square_root
    # and:
    # https://githubharald.github.io/fast_inv_sqrt.html
    @staticmethod
    def invSqrt(res: Float316, x: Float316):
        if x.s > 0:
            raise Exception("SQRT of a negative!")
        
        # precompute x half
        UtilsFloat.ISQRT_x2.s = 0
        UtilsFloat.ISQRT_x2.e = x.e - 1
        UtilsFloat.ISQRT_x2.m = x.m

        # initial guess: just modify the exponent
        UtilsFloat.ISQRT_y.s = 0
        UtilsFloat.ISQRT_y.e = 190 - (x.e // 2)
        UtilsFloat.ISQRT_y.m = 8192

        # Newton-Raphson method
        # y  = y * ( threehalfs - ( x2 * y * y ) );
        Float316.mul(UtilsFloat.ISQRT_tmpRes, UtilsFloat.ISQRT_x2, UtilsFloat.ISQRT_y)
        Float316.mul(UtilsFloat.ISQRT_tmpRes, UtilsFloat.ISQRT_tmpRes, UtilsFloat.ISQRT_y)
        Float316.sub(UtilsFloat.ISQRT_tmpRes, Constants.CONST_THREE_HALFS, UtilsFloat.ISQRT_tmpRes)
        Float316.mul(UtilsFloat.ISQRT_y, UtilsFloat.ISQRT_y, UtilsFloat.ISQRT_tmpRes)

        # y  = y * ( threehalfs - ( x2 * y * y ) );
        Float316.mul(UtilsFloat.ISQRT_tmpRes, UtilsFloat.ISQRT_x2, UtilsFloat.ISQRT_y)
        Float316.mul(UtilsFloat.ISQRT_tmpRes, UtilsFloat.ISQRT_tmpRes, UtilsFloat.ISQRT_y)
        Float316.sub(UtilsFloat.ISQRT_tmpRes, Constants.CONST_THREE_HALFS, UtilsFloat.ISQRT_tmpRes)
        Float316.mul(UtilsFloat.ISQRT_y, UtilsFloat.ISQRT_y, UtilsFloat.ISQRT_tmpRes)

        res.s = 0
        res.e = UtilsFloat.ISQRT_y.e
        res.m = UtilsFloat.ISQRT_y.m
