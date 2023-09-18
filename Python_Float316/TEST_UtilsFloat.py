from Float316 import Float316
from UtilsFloat import UtilsFloat
import numpy as np
import time


def relErr(actual, expected):
    return np.fabs((actual - expected) / expected)


def test_sqrt():
    start_time = time.time()
    res = Float316(0, 0, 0)

    EPS = 0.05
    for x in np.arange(0.001, 1.0, 0.001):
        f = Float316.create(x)
        UtilsFloat.sqrt(res, f)
        fval = res.getValue()
        relErrValue = relErr(np.sqrt(x), fval)
        assert relErrValue < EPS, f"SqrtTest-1, x={x}, sqrt(x)={np.sqrt(x)}, sqrt(v)={fval}, relErr={relErrValue}"

    EPS = 0.05
    for x in np.arange(1.0, 10.0, 0.01):
        f = Float316.create(x)
        UtilsFloat.sqrt(res, f)
        fval = res.getValue()
        relErrValue = relErr(np.sqrt(x), fval)
        assert relErrValue < EPS, f"SqrtTest-2, x={x}, sqrt(x)={np.sqrt(x)}, sqrt(v)={fval}, relErr={relErrValue}"

    EPS = 0.05
    for x in np.arange(10.0, 100.0, 0.1):
        f = Float316.create(x)
        UtilsFloat.sqrt(res, f)
        fval = res.getValue()
        relErrValue = relErr(np.sqrt(x), fval)
        assert relErrValue < EPS, f"SqrtTest-3, x={x}, sqrt(x)={np.sqrt(x)}, sqrt(v)={fval}, relErr={relErrValue}"

    EPS = 0.05
    for x in np.arange(100.0, 1000.0, 1.0):
        f = Float316.create(x)
        UtilsFloat.sqrt(res, f)
        fval = res.getValue()
        relErrValue = relErr(np.sqrt(x), fval)
        assert relErrValue < EPS, f"SqrtTest-4, x={x}, sqrt(x)={np.sqrt(x)}, sqrt(v)={fval}, relErr={relErrValue}"

    end_time = time.time()
    print("SQRT TEST OK.", end_time - start_time, "sec")


def test_invSqrt():
    start_time = time.time()
    res = Float316(0, 0, 0)

    EPS = 0.15
    for x in np.arange(0.1, 1.0, 0.01):
        f = Float316.create(x)
        UtilsFloat.invSqrt(res, f)
        fval = res.getValue()
        relErrValue = relErr(1.0 / np.sqrt(x), fval)
        assert relErrValue < EPS, f"InvSqrtTest-1, x={x}, invSqrt(x)={1.0 / np.sqrt(x)}, invSqrt(v)={fval}, relErr={relErrValue}"

    EPS = 0.15
    for x in np.arange(1.0, 10.0, 0.01):
        f = Float316.create(x)
        UtilsFloat.invSqrt(res, f)
        fval = res.getValue()
        relErrValue = relErr(1.0 / np.sqrt(x), fval)
        assert relErrValue < EPS, f"InvSqrtTest-2, x={x}, invSqrt(x)={1.0 / np.sqrt(x)}, invSqrt(v)={fval}, relErr={relErrValue}"

    EPS = 0.15
    for x in np.arange(10.0, 100.0, 0.1):
        f = Float316.create(x)
        UtilsFloat.invSqrt(res, f)
        fval = res.getValue()
        relErrValue = relErr(1.0 / np.sqrt(x), fval)
        assert relErrValue < EPS, f"InvSqrtTest-3, x={x}, invSqrt(x)={1.0 / np.sqrt(x)}, invSqrt(v)={fval}, relErr={relErrValue}"

    end_time = time.time()
    print("INV SQRT TEST OK.", end_time - start_time, "sec")


def test_floor():
    start_time = time.time()
    res = Float316(0, 0, 0)
    MINUS_ONE = Float316.create(-1.0)

    EPS = 0.001
    for x in np.arange(-100.0, 100.0, 0.1):
        f = Float316.create(x)
        UtilsFloat.floor(res, f)
        fval = res.getValue()
        assert np.abs(np.floor(f.getValue()) - fval) < EPS, f"FloorTest-1, x={np.floor(f.getValue())}, floor(x)={np.floor(x)}, floor(f)={fval}"

    end_time = time.time()
    print("FLOOR TEST OK.", end_time - start_time, "sec")


if __name__ == "__main__":
    test_sqrt()
    test_invSqrt()
    test_floor()
