from Float316 import Float316
from Vec3 import Vec3
from UtilsFloat import UtilsFloat
from Constants import Constants

# A couple of functions that use Float316 variables
# for internal computations.
class UtilsVec:
    # Variables for temporal computations
    UTILS_vx2 = Float316(0, 0, 0)
    UTILS_vy2 = Float316(0, 0, 0)
    UTILS_vz2 = Float316(0, 0, 0)

    NORMALIZE_coeff = Float316(0, 0, 0)

    CROSS_v1y_mul_V2z = Float316(0, 0, 0)
    CROSS_v2y_mul_v1z = Float316(0, 0, 0)
    CROSS_v1z_mul_v2x = Float316(0, 0, 0)
    CROSS_v2z_mul_v1x = Float316(0, 0, 0)
    CROSS_v1x_mul_v2y = Float316(0, 0, 0)
    CROSS_v2x_mul_v1y = Float316(0, 0, 0)

    # res = length(v)
    @staticmethod
    def length(res: Float316, v: Vec3):
        # collect the squares of x, y, and z values
        Float316.mul(UtilsVec.UTILS_vx2, v.x, v.x)
        Float316.mul(UtilsVec.UTILS_vy2, v.y, v.y)
        Float316.mul(UtilsVec.UTILS_vz2, v.z, v.z)

        # res = v.x^2 + v.y^2 + v.y^2
        Float316.add(res, UtilsVec.UTILS_vx2, UtilsVec.UTILS_vy2)
        Float316.add(res, res, UtilsVec.UTILS_vz2)

        # res = sqrt(res)
        UtilsFloat.sqrt(res, res)

    # res = normalize(v)
    @staticmethod
    def normalize(res: Vec3, v: Vec3):
        # collect the squares of x, y, and z values
        Float316.mul(UtilsVec.UTILS_vx2, v.x, v.x)
        Float316.mul(UtilsVec.UTILS_vy2, v.y, v.y)
        Float316.mul(UtilsVec.UTILS_vz2, v.z, v.z)

        # coeff = 1.0 / (v.x^2 + v.y^2 + v.y^2)
        Float316.add(UtilsVec.NORMALIZE_coeff, UtilsVec.UTILS_vx2, UtilsVec.UTILS_vy2)
        Float316.add(UtilsVec.NORMALIZE_coeff, UtilsVec.NORMALIZE_coeff, UtilsVec.UTILS_vz2)
        UtilsFloat.invSqrt(UtilsVec.NORMALIZE_coeff, UtilsVec.NORMALIZE_coeff)

        Vec3.cmul(res, v, UtilsVec.NORMALIZE_coeff)

    # res = dotProduct(v1, v2)
    @staticmethod
    def dot(res: Float316, v1: Vec3, v2: Vec3):
        # res = (v1.x * v2.x) + (v1.y * v2.y) + (v1.z * v2.z)
        Float316.mul(UtilsVec.UTILS_vx2, v1.x, v2.x)
        Float316.mul(UtilsVec.UTILS_vy2, v1.y, v2.y)
        Float316.mul(UtilsVec.UTILS_vz2, v1.z, v2.z)
        
        Float316.add(res, UtilsVec.UTILS_vx2, UtilsVec.UTILS_vy2)
        Float316.add(res, res, UtilsVec.UTILS_vz2)
    
    # The angle between v1 and v2.
    # res = clamp(dot(v1, v2), 0, 1)
    @staticmethod
    def angle(res: Float316, v1: Vec3, v2: Vec3):
        UtilsVec.dot(res, v1, v2)
        # if the result is negative, return with 0.0
        if res.s == 1:
            res.s = 0
            res.e = 0
            res.m = 0
            return
        # if the result is > 1.0, return with 1.0
        if Float316.gt(res, Constants.CONST_ONE):
            res.s = 0
            res.e = 127
            res.m = 8192

    @staticmethod
    def cross(res: Vec3, v1: Vec3, v2: Vec3):
        # res.x = v1.y * v2.z - v2.y * v1.z
        Float316.mul(UtilsVec.CROSS_v1y_mul_V2z, v1.y, v2.z)
        Float316.mul(UtilsVec.CROSS_v2y_mul_v1z, v2.y, v1.z)
        Float316.sub(res.x, UtilsVec.CROSS_v1y_mul_V2z, UtilsVec.CROSS_v2y_mul_v1z)

        # res.y = v1.z * v2.x - v2.z * v1.x
        Float316.mul(UtilsVec.CROSS_v1z_mul_v2x, v1.z, v2.x)
        Float316.mul(UtilsVec.CROSS_v2z_mul_v1x, v2.z, v1.x)
        Float316.sub(res.y, UtilsVec.CROSS_v1z_mul_v2x, UtilsVec.CROSS_v2z_mul_v1x)

        # res.z = v1.x * v2.y - v2.x * v1.y
        Float316.mul(UtilsVec.CROSS_v1x_mul_v2y, v1.x, v2.y)
        Float316.mul(UtilsVec.CROSS_v2x_mul_v1y, v2.x, v1.y)
        Float316.sub(res.z, UtilsVec.CROSS_v1x_mul_v2y, UtilsVec.CROSS_v2x_mul_v1y)     
