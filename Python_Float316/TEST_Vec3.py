from Float316 import Float316
from Vec3 import Vec3

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
    cvalue = -6.6
    a = Vec3(Float316.create(ax), Float316.create(ay), Float316.create(az))
    b = Vec3(Float316.create(bx), Float316.create(by), Float316.create(bz))
    c = Float316.create(cvalue)
    res = Vec3(Float316.create(0), Float316.create(0), Float316.create(0))

    EPS = 0.001
    Vec3.add(res, a, b)
    assert math.fabs(res.x.getValue() - (ax + bx)) < EPS, f"Vec3_AddError_x, a={a}, b={b}, a+b={res}"
    assert math.fabs(res.y.getValue() - (ay + by)) < EPS, f"Vec3_AddError_y, a={a}, b={b}, a+b={res}"
    assert math.fabs(res.z.getValue() - (az + bz)) < EPS, f"Vec3_AddError_z, a={a}, b={b}, a+b={res}"

    EPS = 0.001
    Vec3.sub(res, a, b)
    assert math.fabs(res.x.getValue() - (ax - bx)) < EPS, f"Vec3_SubError_x, a={a}, b={b}, a-b={res}"
    assert math.fabs(res.y.getValue() - (ay - by)) < EPS, f"Vec3_SubError_y, a={a}, b={b}, a-b={res}"
    assert math.fabs(res.z.getValue() - (az - bz)) < EPS, f"Vec3_SubError_z, a={a}, b={b}, a-b={res}"

    EPS = 0.01
    Vec3.cmul(res, b, c)
    assert math.fabs(res.x.getValue() - (bx*cvalue)) < EPS, f"Vec3_MulError_x, b={b}, b*c={res}"
    assert math.fabs(res.y.getValue() - (by*cvalue)) < EPS, f"Vec3_MulError_y, b={b}, b*c={res}"
    assert math.fabs(res.z.getValue() - (bz*cvalue)) < EPS, f"Vec3_MulError_z, b={b}, b*c={res}"

    end_time = time.time()
    print("VEC3 TEST OK.", end_time - start_time, "sec")
