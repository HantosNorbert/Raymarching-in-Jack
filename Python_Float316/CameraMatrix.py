from Float316 import Float316
from Vec3 import Vec3
from UtilsVec import UtilsVec
from Constants import Constants
from Parameters import Parameters

# A class to build the camera matrix from the camera parameters.
class CameraMatrix:
    # Variables for temporal computations
    CAMERA_forward = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    CAMERA_right = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    CAMERA_up = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))

	# Create a camera matrix from the camera position
	# and the the look at point parameters.
	# v1, v2 and v3 are the row vectors of the matrix.
    @staticmethod
    def create(v1: Vec3, v2: Vec3, v3: Vec3):
        # FORWARD
        Vec3.sub(CameraMatrix.CAMERA_forward, Parameters.PARAM_cameraPos, Parameters.PARAM_cameraLookAt)
        UtilsVec.normalize(CameraMatrix.CAMERA_forward, CameraMatrix.CAMERA_forward)

        # RIGHT
        UtilsVec.cross(CameraMatrix.CAMERA_right, Constants.CONST_UP, CameraMatrix.CAMERA_forward)
        UtilsVec.normalize(CameraMatrix.CAMERA_right, CameraMatrix.CAMERA_right)

        # UP
        UtilsVec.cross(CameraMatrix.CAMERA_up, CameraMatrix.CAMERA_forward, CameraMatrix.CAMERA_right)

        # copy
        v1.x = CameraMatrix.CAMERA_right.x
        v1.y = CameraMatrix.CAMERA_up.x
        v1.z = CameraMatrix.CAMERA_forward.x
        v2.x = CameraMatrix.CAMERA_right.y
        v2.y = CameraMatrix.CAMERA_up.y
        v2.z = CameraMatrix.CAMERA_forward.y
        v3.x = CameraMatrix.CAMERA_right.z
        v3.y = CameraMatrix.CAMERA_up.z
        v3.z = CameraMatrix.CAMERA_forward.z
