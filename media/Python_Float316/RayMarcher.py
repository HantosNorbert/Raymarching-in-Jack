from Float316 import Float316
from Vec3 import Vec3
from Surface import Surface
from UtilsVec import UtilsVec
from Scene import Scene
from Parameters import Parameters

# A raymarcher and some related funtions: how to calculate the normal
# at a given point of the scene, and what is the light intensity.
class RayMarcher:
    # Variables for temporal computations
    RAYMATCH_depth = Float316(0, 0, 0)
    RAYMATCH_p = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))

    CNORMAL_pExyy = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    CNORMAL_pEyyx = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    CNORMAL_pEyxy = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    CNORMAL_pExxx = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    CNORMAL_sd1 = Float316(0, 0, 0)
    CNORMAL_sd2 = Float316(0, 0, 0)
    CNORMAL_sd3 = Float316(0, 0, 0)
    CNORMAL_sd4 = Float316(0, 0, 0)
    CNORMAL_exyyMulSd1 = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0,0))
    CNORMAL_eyyxMulSd2 = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0,0))
    CNORMAL_eyxyMulSd3 = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0,0))
    CNORMAL_exxxMulSd4 = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0,0))
    CNORMAL_sdScene = Surface(Float316(0, 0, 0), Float316(0, 0, 0))    

    LIGHT_lightDir = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    LIGHT_camDir = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    LIGHT_reflectDir = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    LIGHT_angle = Float316(0, 0, 0)

    # The heart and soul of our program: a simple raymarching algorithm.
    # Cast a ray from ray origin ro towards ray direction rd until
	# we are close enough to a surface.
    @staticmethod
    def rayMarch(res: Surface, ro: Vec3, rd: Vec3, maxStep: int):
        # depth = minDist initialization (minDist here is 0.0)
        RayMarcher.RAYMATCH_depth.s = 0
        RayMarcher.RAYMATCH_depth.e = 0
        RayMarcher.RAYMATCH_depth.m = 0

        for i in range(maxStep):
            # p = ro + (rd * depth)
            Vec3.cmul(RayMarcher.RAYMATCH_p, rd, RayMarcher.RAYMATCH_depth)
            Vec3.add(RayMarcher.RAYMATCH_p, ro, RayMarcher.RAYMATCH_p)

            # get the closest surface
            Scene.sdScene(res, RayMarcher.RAYMATCH_p)
            
            # we can increase the depth by the signed distance
            # depth += res.sd
            Float316.add(RayMarcher.RAYMATCH_depth, RayMarcher.RAYMATCH_depth, res.sd)

            # if the ray hit a surface or reached the maximum distance, break
            if Parameters.PARAM_precision.gt(res.sd) or RayMarcher.RAYMATCH_depth.gt(Parameters.PARAM_maxDist):
                break

        res.sd.s = RayMarcher.RAYMATCH_depth.s
        res.sd.e = RayMarcher.RAYMATCH_depth.e
        res.sd.m = RayMarcher.RAYMATCH_depth.m


    # Calculate the normal vector at point p based on the scene.
    # This uses a trick called "Tetrahedron technique", see link for more:
    # https://iquilezles.org/articles/normalsSDF/
    @staticmethod
    def calcNormal(res: Vec3, p: Vec3):
        # sd1 = sdScene(p + exyy).sd
        Vec3.add(RayMarcher.CNORMAL_pExyy, p, Parameters.PARAM_exyy)
        Scene.sdScene(RayMarcher.CNORMAL_sdScene, RayMarcher.CNORMAL_pExyy)
        RayMarcher.CNORMAL_sd1.s = RayMarcher.CNORMAL_sdScene.sd.s
        RayMarcher.CNORMAL_sd1.e = RayMarcher.CNORMAL_sdScene.sd.e
        RayMarcher.CNORMAL_sd1.m = RayMarcher.CNORMAL_sdScene.sd.m
        
        # sd2 = sdScene(p + eyyx).sd
        Vec3.add(RayMarcher.CNORMAL_pEyyx, p, Parameters.PARAM_eyyx)
        Scene.sdScene(RayMarcher.CNORMAL_sdScene, RayMarcher.CNORMAL_pEyyx)
        RayMarcher.CNORMAL_sd2.s = RayMarcher.CNORMAL_sdScene.sd.s
        RayMarcher.CNORMAL_sd2.e = RayMarcher.CNORMAL_sdScene.sd.e
        RayMarcher.CNORMAL_sd2.m = RayMarcher.CNORMAL_sdScene.sd.m

        # sd3 = sdScene(p + eyxy).sd
        Vec3.add(RayMarcher.CNORMAL_pEyxy, p, Parameters.PARAM_eyxy)
        Scene.sdScene(RayMarcher.CNORMAL_sdScene, RayMarcher.CNORMAL_pEyxy)
        RayMarcher.CNORMAL_sd3.s = RayMarcher.CNORMAL_sdScene.sd.s
        RayMarcher.CNORMAL_sd3.e = RayMarcher.CNORMAL_sdScene.sd.e
        RayMarcher.CNORMAL_sd3.m = RayMarcher.CNORMAL_sdScene.sd.m

        # sd4 = sdScene(p + exxx).sd
        Vec3.add(RayMarcher.CNORMAL_pExxx, p, Parameters.PARAM_exxx)
        Scene.sdScene(RayMarcher.CNORMAL_sdScene, RayMarcher.CNORMAL_pExxx)
        RayMarcher.CNORMAL_sd4.s = RayMarcher.CNORMAL_sdScene.sd.s
        RayMarcher.CNORMAL_sd4.e = RayMarcher.CNORMAL_sdScene.sd.e
        RayMarcher.CNORMAL_sd4.m = RayMarcher.CNORMAL_sdScene.sd.m

        # res = normalize(exyy * sd1 + eyyx * sd2 + eyxy * sd3 + exxx * sd4)
        Vec3.cmul(RayMarcher.CNORMAL_exyyMulSd1, Parameters.PARAM_exyy, RayMarcher.CNORMAL_sd1)
        Vec3.cmul(RayMarcher.CNORMAL_eyyxMulSd2, Parameters.PARAM_eyyx, RayMarcher.CNORMAL_sd2)
        Vec3.cmul(RayMarcher.CNORMAL_eyxyMulSd3, Parameters.PARAM_eyxy, RayMarcher.CNORMAL_sd3)
        Vec3.cmul(RayMarcher.CNORMAL_exxxMulSd4, Parameters.PARAM_exxx, RayMarcher.CNORMAL_sd4)

        Vec3.add(res, RayMarcher.CNORMAL_exyyMulSd1, RayMarcher.CNORMAL_eyyxMulSd2)
        Vec3.add(res, res, RayMarcher.CNORMAL_eyxyMulSd3)
        Vec3.add(res, res, RayMarcher.CNORMAL_exxxMulSd4)

        UtilsVec.normalize(res, res)


	# Calculate the light intensity at point p with normal vector
	# norm and light position lightPos. It uses the Phong reflection
	# model with ambient, diffuse and specular components
    @staticmethod
    def lightIntensity(res: Float316, p: Vec3, norm: Vec3):
        # lightDir = normalize(lightPos - p)
        Vec3.sub(RayMarcher.LIGHT_lightDir, Parameters.PARAM_lightPos, p)
        UtilsVec.normalize(RayMarcher.LIGHT_lightDir, RayMarcher.LIGHT_lightDir)

        # camDir = normalize(camPos - p)
        Vec3.sub(RayMarcher.LIGHT_camDir, Parameters.PARAM_cameraPos, p)
        UtilsVec.normalize(RayMarcher.LIGHT_camDir, RayMarcher.LIGHT_camDir)

        # reflectDir = 2.0 * angle(lightDir, norm) * norm - lightDir
        UtilsVec.angle(RayMarcher.LIGHT_angle, RayMarcher.LIGHT_lightDir, norm)
        RayMarcher.LIGHT_angle.e = RayMarcher.LIGHT_angle.e + 1
        Vec3.cmul(RayMarcher.LIGHT_reflectDir, norm, RayMarcher.LIGHT_angle)
        Vec3.sub(RayMarcher.LIGHT_reflectDir, RayMarcher.LIGHT_reflectDir, RayMarcher.LIGHT_lightDir)

        # diffuseLight = kd * angle(lightDir, norm) * id
        UtilsVec.angle(RayMarcher.LIGHT_angle, RayMarcher.LIGHT_lightDir, norm)
        Float316.mul(res, Parameters.PARAM_kd_id, RayMarcher.LIGHT_angle)

        # specularLight = ks * math.pow(angle(reflectDir, camDir), a) * iss
        UtilsVec.angle(RayMarcher.LIGHT_angle, RayMarcher.LIGHT_reflectDir, RayMarcher.LIGHT_camDir)
        Float316.mul(RayMarcher.LIGHT_angle, RayMarcher.LIGHT_angle, RayMarcher.LIGHT_angle)
        Float316.mul(RayMarcher.LIGHT_angle, RayMarcher.LIGHT_angle, RayMarcher.LIGHT_angle)
        Float316.mul(RayMarcher.LIGHT_angle, RayMarcher.LIGHT_angle, Parameters.PARAM_ks_is)

        Float316.add(res, res, RayMarcher.LIGHT_angle)
