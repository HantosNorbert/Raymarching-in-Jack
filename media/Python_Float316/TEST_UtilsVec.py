from Float316 import Float316
from Vec3 import Vec3
from UtilsVec import UtilsVec

import time
import math

if __name__ == "__main__":
    start_time = time.time()

    ax = 3.5
    ay = -3.3
    az = 4.7
    bx = 2.4
    by = 0.8
    bz = -1.2
    a = Vec3(Float316.create(ax), Float316.create(ay), Float316.create(az))
    b = Vec3(Float316.create(bx), Float316.create(by), Float316.create(bz))
    resFloat = Float316(0, 0, 0)
    resVec = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))
    
    EPS = 0.001
    UtilsVec.length(resFloat, a)
    l = math.sqrt(sum(i**2 for i in [ax, ay, az]))
    assert math.fabs(resFloat.getValue() - l) < EPS, f"UtilsVec_LengthError, a={a}, length={l}, res={resFloat}"

    EPS = 0.005
    UtilsVec.normalize(resVec, a)
    l = math.sqrt(sum(i**2 for i in [ax, ay, az]))
    nx = ax / l
    ny = ay / l
    nz = az / l
    assert math.fabs(resVec.x.getValue() - nx) < EPS, f"UtilsVec_NormError_x, a={a}, nx={nx}, ny={ny}, nz={nz}, res={resVec}"
    assert math.fabs(resVec.y.getValue() - ny) < EPS, f"UtilsVec_NormError_y, a={a}, nx={nx}, ny={ny}, nz={nz}, res={resVec}"
    assert math.fabs(resVec.z.getValue() - nz) < EPS, f"UtilsVec_NormError_z, a={a}, nx={nx}, ny={ny}, nz={nz}, res={resVec}"

    EPS = 0.01
    UtilsVec.dot(resFloat, a, b)
    d = ax*bx + ay*by + az*bz
    assert math.fabs(resFloat.getValue() - d) < EPS, f"UtilsVec_DotError, a={a}, b={b}, d={d}, res={resFloat}"

    EPS = 0.01
    UtilsVec.cross(resVec, a, b)
    cx = ay*bz - az*by
    cy = az*bx - ax*bz
    cz = ax*by - ay*bx
    assert math.fabs(resVec.x.getValue() - cx) < EPS, f"UtilsVec_CrossError_x, a={a}, b={b}, cx={cx}, cy={cy}, cz={cz}, res={resVec}"
    assert math.fabs(resVec.y.getValue() - cy) < EPS, f"UtilsVec_CrossError_y, a={a}, b={b}, cx={cx}, cy={cy}, cz={cz}, res={resVec}"
    assert math.fabs(resVec.z.getValue() - cz) < EPS, f"UtilsVec_CrossError_z, a={a}, b={b}, cx={cx}, cy={cy}, cz={cz}, res={resVec}"

    EPS = 0.01
    UtilsVec.angle(resFloat, a, b)
    d = ax*bx + ay*by + az*bz
    assert math.fabs(resFloat.getValue() - d) < EPS, f"UtilsVec_AngleError, a={a}, b={b}, d={d}, res={resFloat}"

    end_time = time.time()
    print("UTILS_VEC TEST OK.", end_time - start_time, "sec")
