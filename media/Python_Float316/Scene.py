from Float316 import Float316
from Vec3 import Vec3
from UtilsFloat import UtilsFloat
from UtilsVec import UtilsVec
from Surface import Surface
from Constants import Constants
from Parameters import Parameters

# A class containing functions to define the signed distance function
# that describes the entire scene.
class Scene:
    # Variables for temporal computations
    SPHERE_p = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    SPHERE_length = Float316(0, 0, 0)
    SPHERE_sd = Float316(0, 0, 0)

    TORUS_p = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    TORUS_p1_2 = Float316(0, 0, 0)
    TORUS_p2_2 = Float316(0, 0, 0)
    TORUS_d1 = Float316(0, 0, 0)
    TORUS_d2 = Float316(0, 0, 0)

    FLOOR_sd = Float316(0, 0, 0)

    SCENE_floorPx = Float316(0, 0, 0)
    SCENE_floorPz = Float316(0, 0, 0)
    SCENE_floorColor = Float316(0, 0, 0)
    SCENE_floor = Surface(Float316(0, 0, 0), Float316(0, 0, 0))
    SCENE_sphere = Surface(Float316(0, 0, 0), Float316(0, 0, 0))
    SCENE_TORUS = Surface(Float316(0, 0, 0), Float316(0, 0, 0))
    SCENE_res = Surface(Float316(0, 0, 0), Float316(0, 0, 0))

    # Define a Surface res, where
    #   res.col = col
    #   res.sd = the signed distance of p and a sphere defined
    #   at offset point offset with radius r
    # See https://iquilezles.org/articles/distfunctions/
    @staticmethod
    def sdSphere(res: Surface, p: Vec3, r: Float316, offset: Vec3, col: Float316):
        # p = p - offset
        Vec3.sub(Scene.SPHERE_p, p, offset)

        # sd = length(p) - r
        UtilsVec.length(Scene.SPHERE_length, Scene.SPHERE_p)
        Float316.sub(Scene.SPHERE_sd, Scene.SPHERE_length, r)

        # res = Surface(sd, col)
        # deepcopy
        res.sd.s = Scene.SPHERE_sd.s
        res.sd.e = Scene.SPHERE_sd.e
        res.sd.m = Scene.SPHERE_sd.m
        res.col.s = col.s
        res.col.e = col.e
        res.col.m = col.m
    
    # Define a Surface res, where
    #   res.col = col
    #   res.sd = the signed distance of p and a torus defined at
    #   offset point offset with outer radius r1 and cross radius r2
    # See https://iquilezles.org/articles/distfunctions/
    @staticmethod
    def sdTorus(res: Surface, p: Vec3, r1: Float316, r2: Float316, offset: Vec3, col: Float316):
        # p = p - offset
        Vec3.sub(Scene.TORUS_p, p, offset)

        # d1 = length(p.x, p.z) - r1
        Float316.mul(Scene.TORUS_p1_2, Scene.TORUS_p.x, Scene.TORUS_p.x)
        Float316.mul(Scene.TORUS_p2_2, Scene.TORUS_p.z, Scene.TORUS_p.z)
        Float316.add(Scene.TORUS_d1, Scene.TORUS_p1_2, Scene.TORUS_p2_2)
        UtilsFloat.sqrt(Scene.TORUS_d1, Scene.TORUS_d1)
        Float316.sub(Scene.TORUS_d1, Scene.TORUS_d1, r1)

        # d2 = length(d1, p.y) - r2
        Float316.mul(Scene.TORUS_p1_2, Scene.TORUS_d1, Scene.TORUS_d1)
        Float316.mul(Scene.TORUS_p2_2, Scene.TORUS_p.y, Scene.TORUS_p.y)
        Float316.add(Scene.TORUS_d2, Scene.TORUS_p1_2, Scene.TORUS_p2_2)

        UtilsFloat.sqrt(Scene.TORUS_d2, Scene.TORUS_d2)
        Float316.sub(Scene.TORUS_d2, Scene.TORUS_d2, r2)

        # res = Surface(sd, col)
        # deepcopy
        res.sd.s = Scene.TORUS_d2.s
        res.sd.e = Scene.TORUS_d2.e
        res.sd.m = Scene.TORUS_d2.m
        res.col.s = col.s
        res.col.e = col.e
        res.col.m = col.m

    # Define a Surface res, where
    #   res.col = col
    #   res.sd = the signed distance of p and a plane (floor) defined at y = -1
    @staticmethod
    def sdFloor(res: Surface, p: Vec3, col: Float316):
        # sd = p.y + 1.0
        Float316.add(Scene.FLOOR_sd, p.y, Constants.CONST_ONE)
        # res = Surface(sd, col)
        res.sd.s = Scene.FLOOR_sd.s
        res.sd.e = Scene.FLOOR_sd.e
        res.sd.m = Scene.FLOOR_sd.m
        res.col.s = col.s
        res.col.e = col.e
        res.col.m = col.m
    
    # union of two surfaces: a min function
    @staticmethod
    def unionSDF(obj1: Surface, obj2: Surface) -> Surface:
        if obj2.sd.gt(obj1.sd):
            return obj1
        return obj2


    # Put together a scene (Surface), containing a floor with checkerboard
    # pattern and two identical spheres at different positions.
    @staticmethod
    def sdScene(res: Surface, p: Vec3):
        # floorColor is a checkerboard pattern:
        # floorColor = 1. + 0.7*((floor(p.x) + math.floor(p.z)) % 2)
        UtilsFloat.floor(Scene.SCENE_floorPx, p.x)
        UtilsFloat.floor(Scene.SCENE_floorPz, p.z)
        Float316.add( Scene.SCENE_floorColor, Scene.SCENE_floorPx, Scene.SCENE_floorPz)
        Float316.mod2(Scene.SCENE_floorColor, Scene.SCENE_floorColor)
        Float316.mul( Scene.SCENE_floorColor, Scene.SCENE_floorColor, Parameters.PARAM_objectColor)
        Float316.add( Scene.SCENE_floorColor, Scene.SCENE_floorColor, Constants.CONST_ONE)

        # define the scene: a floor, a sphere and a torus
        Scene.sdFloor(Scene.SCENE_floor, p, Scene.SCENE_floorColor)
        Scene.sdSphere(Scene.SCENE_sphere, p, Parameters.PARAM_sphereRad, Parameters.PARAM_spherePos, Parameters.PARAM_objectColor)
        Scene.sdTorus(Scene.SCENE_TORUS, p, Parameters.PARAM_torusOuterRad, Parameters.PARAM_torusInnerRad, Parameters.PARAM_torusPos, Parameters.PARAM_objectColor)

        # res = union(sphere1, sphere2, floor)
        Scene.SCENE_res = Scene.unionSDF(Scene.SCENE_sphere, Scene.SCENE_TORUS)
        Scene.SCENE_res = Scene.unionSDF(Scene.SCENE_res, Scene.SCENE_floor)
        # deepcopy
        res.sd.s =  Scene.SCENE_res.sd.s
        res.sd.e =  Scene.SCENE_res.sd.e
        res.sd.m =  Scene.SCENE_res.sd.m
        res.col.s = Scene.SCENE_res.col.s
        res.col.e = Scene.SCENE_res.col.e
        res.col.m = Scene.SCENE_res.col.m
