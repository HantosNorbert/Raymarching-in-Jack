from Float316 import Float316

# A class for vectors. Not much else to say.
class Vec3:
    def __init__(self, x: Float316, y: Float316, z: Float316):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def add(res, v1, v2):
        Float316.add(res.x, v1.x, v2.x)
        Float316.add(res.y, v1.y, v2.y)
        Float316.add(res.z, v1.z, v2.z)
    
    @staticmethod
    def sub(res, v1, v2):
        Float316.sub(res.x, v1.x, v2.x)
        Float316.sub(res.y, v1.y, v2.y)
        Float316.sub(res.z, v1.z, v2.z)
        
    @staticmethod
    def cmul(res, v, f):
        Float316.mul(res.x, v.x, f)
        Float316.mul(res.y, v.y, f)
        Float316.mul(res.z, v.z, f)
    
    #####################################################################################
    # THESE ARE ONLY FOR TESTING
    #####################################################################################
    # print a representation
    def __str__(self):
        return f"({self.x.getValue()}, {self.y.getValue()}, {self.z.getValue()})"
    