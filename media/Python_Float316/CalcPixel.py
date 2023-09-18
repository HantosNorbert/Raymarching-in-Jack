from Float316 import Float316
from Vec3 import Vec3
from UtilsVec import UtilsVec
from Surface import Surface
from RayMarcher import RayMarcher
from CameraMatrix import CameraMatrix
from Parameters import Parameters

# A class to calculate the float value of a single pixel.
class CalcPixel:
    # Variables for temporal computations
    PIXEL_cameraMatrix_v1 = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    PIXEL_cameraMatrix_v2 = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    PIXEL_cameraMatrix_v3 = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))

    PIXEL_normUV = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    PIXEL_rayDir = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    PIXEL_surface = Surface(Float316(0, 0, 0), Float316(0, 0, 0))
    PIXEL_p = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    PIXEL_normal = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    PIXEL_lightIntensity = Float316(0, 0, 0)

    PIXEL_lightPosMinusP = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    PIXEL_lightDir = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    PIXEL_newRayOrigin = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    PIXEL_shadowRayLength = Float316(0, 0, 0)
    PIXEL_lightPosMinusNewRayOrigin = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    PIXEL_lightDistance = Float316(0, 0, 0)

    @staticmethod
    def init():
        CameraMatrix.create(CalcPixel.PIXEL_cameraMatrix_v1, CalcPixel.PIXEL_cameraMatrix_v2, CalcPixel.PIXEL_cameraMatrix_v3)

    # based on (u,v) normalized pixel coordinates, get the intensity value
    # of that pixel
    @staticmethod
    def calcPixelValue(res: Float316, u: Float316, v: Float316):
        ###############################################################
        # RAY MARCHING
        ###############################################################

        # calculate the ray direction
        # rd = camMatrix * normalize(Vec3(u, v, -1.0))
        CalcPixel.PIXEL_normUV.x = u
        CalcPixel.PIXEL_normUV.y = v
        CalcPixel.PIXEL_normUV.z.s = 1
        CalcPixel.PIXEL_normUV.z.e = 127
        CalcPixel.PIXEL_normUV.z.m = 8192

        UtilsVec.normalize(CalcPixel.PIXEL_normUV, CalcPixel.PIXEL_normUV)

        UtilsVec.dot(CalcPixel.PIXEL_rayDir.x, CalcPixel.PIXEL_cameraMatrix_v1, CalcPixel.PIXEL_normUV)
        UtilsVec.dot(CalcPixel.PIXEL_rayDir.y, CalcPixel.PIXEL_cameraMatrix_v2, CalcPixel.PIXEL_normUV)
        UtilsVec.dot(CalcPixel.PIXEL_rayDir.z, CalcPixel.PIXEL_cameraMatrix_v3, CalcPixel.PIXEL_normUV)

        # ray marching: what surface did we hit
        # surface = rayMarch(camPos, rd)
        RayMarcher.rayMarch(CalcPixel.PIXEL_surface, Parameters.PARAM_cameraPos, CalcPixel.PIXEL_rayDir,
                            Parameters.PARAM_maxMarchingSteps)

        # if we didn't hit any surface: it's a background (no lighting)
        # if surface.sd > MAX_DIST:
        #   col = backgroundColor
        if CalcPixel.PIXEL_surface.sd.gt(Parameters.PARAM_maxDist):
            res.s = Parameters.PARAM_backgroundColor.s
            res.e = Parameters.PARAM_backgroundColor.e
            res.m = Parameters.PARAM_backgroundColor.m
            return

        ###############################################################
        # LIGHT INTENSITY
        ###############################################################

        # let's bring p to that surface
        # p = camPos + rd * co.sd
        Vec3.cmul(CalcPixel.PIXEL_p, CalcPixel.PIXEL_rayDir, CalcPixel.PIXEL_surface.sd)
        Vec3.add(CalcPixel.PIXEL_p, Parameters.PARAM_cameraPos, CalcPixel.PIXEL_p)

        # normal = calcNormal(p)
        RayMarcher.calcNormal(CalcPixel.PIXEL_normal, CalcPixel.PIXEL_p)

        # calculate the light intensity at p
        # col = co.col * lightIntensity(p, normal, camPos, lightPos, co.sd) +
        #       0.2*backgroundColor
        RayMarcher.lightIntensity(CalcPixel.PIXEL_lightIntensity, CalcPixel.PIXEL_p, CalcPixel.PIXEL_normal)
        Float316.mul(res, CalcPixel.PIXEL_surface.col, CalcPixel.PIXEL_lightIntensity)
        Float316.add(res, res, Parameters.PARAM_ambientBackgroundColor)

        ###############################################################
        # SHADOW CALCULATIONS
        ###############################################################

        # we need a light direction first
        # lightDir = normalize(lightPos - p)
        Vec3.sub(CalcPixel.PIXEL_lightPosMinusP, Parameters.PARAM_lightPos, CalcPixel.PIXEL_p)
        UtilsVec.normalize(CalcPixel.PIXEL_lightDir, CalcPixel.PIXEL_lightPosMinusP)
        
        # start a new raymarching from the surface we hit, but we need to
        # lift it up a little ("up" = towards its normal vector)
        # newRayOrigin = p + normal * PRECISION * 2.0
        Vec3.cmul(CalcPixel.PIXEL_newRayOrigin, CalcPixel.PIXEL_normal, Parameters.PARAM_precision2)
        Vec3.add(CalcPixel.PIXEL_newRayOrigin, CalcPixel.PIXEL_newRayOrigin, CalcPixel. PIXEL_p)

        # start a new ray march: we either hit a surface or don't
        # shadowRayLength = rayMarch(newRayOrigin, lightDir).sd
        RayMarcher.rayMarch(CalcPixel.PIXEL_surface, CalcPixel.PIXEL_newRayOrigin, CalcPixel.PIXEL_lightDir, Parameters.PARAM_maxMarchingStepsShadow)
        # deepcopy
        CalcPixel.PIXEL_shadowRayLength.s = CalcPixel.PIXEL_surface.sd.s
        CalcPixel.PIXEL_shadowRayLength.e = CalcPixel.PIXEL_surface.sd.e
        CalcPixel.PIXEL_shadowRayLength.m = CalcPixel.PIXEL_surface.sd.m

        # if we hit a surface: we are in a shadow -> reduce the final color
        # if shadowRayLength < length(lightPos - newRayOrigin):
        #     col *= 0.25
        Vec3.sub(CalcPixel.PIXEL_lightPosMinusNewRayOrigin, Parameters.PARAM_lightPos, CalcPixel.PIXEL_newRayOrigin)
        UtilsVec.length(CalcPixel.PIXEL_lightDistance, CalcPixel.PIXEL_lightPosMinusNewRayOrigin)
        if CalcPixel.PIXEL_lightDistance.gt(CalcPixel.PIXEL_shadowRayLength):
            res.e -= 2
