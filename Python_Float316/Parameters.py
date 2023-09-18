from Float316 import Float316
from Vec3 import Vec3

# A class that contains all the parameters that can be freely changed,
# such as the position, size and color of the objects; and some more.
class Parameters:
    ########################################################
    # SCENE DEFINITION
    ########################################################
    PARAM_spherePos = Vec3(Float316(1, 127, 12288), Float316(0, 0, 0), Float316(0, 0, 0))  # (-1.5, 0, 0)
    PARAM_sphereRad = Float316(0, 127, 8192)  # 1.0

    PARAM_torusPos =  Vec3(Float316(0, 127, 12288), Float316(0, 0, 0), Float316(0, 0, 0))  # ( 1.5, 0, 0)
    PARAM_torusOuterRad = Float316(0, 127, 8192)  # 1.0
    PARAM_torusInnerRad = Float316(0, 125, 8192)  # 0.25

    ########################################################
    # CAMERA
    ########################################################
    PARAM_cameraPos = Vec3(Float316(0, 0, 0), Float316(0, 127, 12288), Float316(0, 129, 8192))  # (0.0, 1.5, 4.0)
    PARAM_cameraLookAt = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))  # (0.0, 0.0, 0.0)

    ########################################################
    # COLORS AND LIGHTING
    ########################################################
    PARAM_lightPos = Vec3(Float316(0, 128, 8192), Float316(0, 129, 10240), Float316(1, 127, 8192))  # (2.0, 5.0, -1.0)

    PARAM_objectColor = Float316(0, 126, 11468)  # 0.7
    PARAM_backgroundColor = Float316(0, 126, 13680)  # 0.835
    PARAM_ambientBackgroundColor = Float316(0, 124, 10944)  # 0.2 * BACKGROUND_VALUE

    PARAM_kd_id = Float316(0, 126, 10321)  # kd * id, 0.9 * 0.7
    PARAM_ks_is = Float316(0, 125, 11468)  # ks * is, 0.7 * 0.5

    ########################################################
    # RAYMARCHING
    ########################################################
    PARAM_precision = Float316(0, 120, 10485)  # 0.01
    PARAM_precision2 = Float316(0, 121, 10485)  # 2.0 * PRECISION

    PARAM_maxDist = Float316(0, 130, 12288)  # 12.0

    PARAM_maxMarchingSteps = 64
    PARAM_maxMarchingStepsShadow = 32

    PARAM_exyy = Vec3(Float316(0, 119, 10485), Float316(1, 119, 10485), Float316(1, 119, 10485))  # ( 0.005, -0.005, -0.005)
    PARAM_eyyx = Vec3(Float316(1, 119, 10485), Float316(1, 119, 10485), Float316(0, 119, 10485))  # (-0.005, -0.005,  0.005)
    PARAM_eyxy = Vec3(Float316(1, 119, 10485), Float316(0, 119, 10485), Float316(1, 119, 10485))  # (-0.005,  0.005, -0.005)
    PARAM_exxx = Vec3(Float316(0, 119, 10485), Float316(0, 119, 10485), Float316(0, 119, 10485))  # ( 0.005,  0.005,  0.005)
