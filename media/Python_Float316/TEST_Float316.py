from Float316 import Float316
import numpy as np
import time

def approxEqual(a, b, relEps):
    # Symmetric relative error check without division.
    diff = np.abs(a - b)
    return diff <= relEps * max(abs(a), abs(b))


def test_repr():
    start_time = time.time()

    EPS = 0.0001
    for x in np.arange(-1.0, 1.0, 0.001):
        res = Float316.create(x).getValue()
        assert np.abs(x - res) < EPS, f"RepTest-1, x={x}, res={res}"

    EPS = 0.001
    for x in np.arange(-10.0, 10.0, 0.01):
        res = Float316.create(x).getValue()
        assert np.abs(x - res) < EPS, f"RepTest-2, x={x}, res={res}"

    EPS = 0.01
    for x in np.arange(-100.0, 100.0, 0.1):
        res = Float316.create(x).getValue()
        assert np.abs(x - res) < EPS, f"RepTest-3, x={x}, res={res}"

    for x in np.arange(-1000.0, 1000.0, 1.0):
        res = Float316.create(x).getValue()
        assert x == res, f"RepTest-4, x={x}, v={res}"

    end_time = time.time()
    print("REPR TEST OK.", end_time - start_time, "sec")


def test_mult():
    start_time = time.time()
    res = Float316(0, 0, 0)

    EPS = 0.001
    for x in np.arange(-1.0, 1.0, 0.01):
        for y in np.arange(-1.0, 1.0, 0.01):
            f1 = Float316.create(x)
            f2 = Float316.create(y)
            Float316.mul(res, f1, f2)
            assert np.abs(x*y - res.getValue()) < EPS, f"MulTest-1, x={x}, y={y}, xy={x*y}, res={res}"
            assert approxEqual(x*y, res.getValue(), 0.001), f"MulTest-1, x={x}, y={y}, xy={x*y}, res={res}"

    EPS = 0.1
    for x in np.arange(-10.0, 10.0, 0.1):
        for y in np.arange(-10.0, 10.0, 0.1):
            f1 = Float316.create(x)
            f2 = Float316.create(y)
            Float316.mul(res, f1, f2)
            assert np.abs(x*y - res.getValue()) < EPS, f"MulTest-2, x={x}, y={y}, xy={x*y}, res={res}"
            assert approxEqual(x*y, res.getValue(), 0.001), f"MulTest-2, x={x}, y={y}, xy={x*y}, res={res}"

    end_time = time.time()
    print("MULT TEST OK.", end_time - start_time, "sec")


def test_greater():
    start_time = time.time()

    for x in np.arange(-1.0, 1.0, 0.01):
        for y in np.arange(-1.0, 1.0, 0.01):
            f1 = Float316.create(x)
            f2 = Float316.create(y)
            if x > y:
                assert f1.gt(f2), f"GrTest-1, x={x}, y={y}, f1={f1}, f2={f2}"
            else:
                assert not f1.gt(f2), f"GrTest-1, x={x}, y={y}, f1={f1}, f2={f2}"


    for x in np.arange(-10.0, 10.0, 0.1):
        for y in np.arange(-10.0, 10.0, 0.1):
            f1 = Float316.create(x)
            f2 = Float316.create(y)
            if x > y:
                assert f1.gt(f2), f"GrTest-2, x={x}, y={y}, f1={f1}, f2={f2}"
            else:
                assert not f1.gt(f2), f"GrTest-2, x={x}, y={y}, f1={f1}, f2={f2}"

    end_time = time.time()
    print("GR TEST OK.", end_time - start_time, "sec")


def test_add():
    start_time = time.time()
    res = Float316(0, 0, 0)

    EPS = 0.001
    for x in np.arange(-1.0, 1.0, 0.01):
        for y in np.arange(-1.0, 1.0, 0.01):
            f1 = Float316.create(x)
            f2 = Float316.create(y)
            Float316.add(res, f1, f2)
            assert np.abs(x+y - res.getValue()) < EPS, f"AddTest-1, x={x}, y={y}, x+y={x+y}, res={res}"

    EPS = 0.01
    for x in np.arange(-10.0, 10.0, 0.1):
        for y in np.arange(-10.0, 10.0, 0.1):
            f1 = Float316.create(x)
            f2 = Float316.create(y)
            Float316.add(res, f1, f2)
            assert np.abs(x+y - res.getValue()) < EPS, f"AddTest-2, x={x}, y={y}, x+y={x+y}, res={res}"

    end_time = time.time()
    print("ADD TEST OK.", end_time - start_time, "sec")


def test_sub():
    start_time = time.time()
    res = Float316(0, 0, 0)

    EPS = 0.001
    for x in np.arange(-1.0, 1.0, 0.01):
        for y in np.arange(-1.0, 1.0, 0.01):
            f1 = Float316.create(x)
            f2 = Float316.create(y)
            Float316.sub(res, f1, f2)
            assert np.abs(x-y - res.getValue()) < EPS, f"SubTest-1, x={x}, y={y}, x-y={x-y}, res={res}"

    EPS = 0.01
    for x in np.arange(-10.0, 10.0, 0.1):
        for y in np.arange(-10.0, 10.0, 0.1):
            f1 = Float316.create(x)
            f2 = Float316.create(y)
            Float316.sub(res, f1, f2)
            assert np.abs(x-y - res.getValue()) < EPS, f"SubTest-2, x={x}, y={y}, x-y={x-y}, res={res}"

    end_time = time.time()
    print("SUB TEST OK.", end_time - start_time, "sec")


def test_div():
    start_time = time.time()
    res = Float316(0, 0, 0)

    EPS = 0.001
    for x in np.arange(-1.0, 1.0, 0.01):
        for y in np.arange(-1.0, 1.0, 0.01):
            if y == 0.0:
                continue
            f1 = Float316.create(x)
            f2 = Float316.create(y)
            Float316.div(res, f1, f2)
            assert approxEqual(x/y, res.getValue(), EPS), f"DivTest-1, x={x}, y={y}, x/y={x/y}, res={res}"

    EPS = 0.001
    for x in np.arange(-10.0, 10.0, 0.1):
        for y in np.arange(-10.0, 10.0, 0.1):
            if y == 0.0:
                continue
            f1 = Float316.create(x)
            f2 = Float316.create(y)
            Float316.div(res, f1, f2)
            assert approxEqual(x/y, res.getValue(), EPS), f"DivTest-2, x={x}, y={y}, x/y={x/y}, res={res}"

    end_time = time.time()
    print("DIV TEST OK.", end_time - start_time, "sec")


def test_mod2():
    start_time = time.time()
    res = Float316(0, 0, 0)

    for x in np.arange(-100.0, 100.0, 1.0):
        f = Float316.create(x)
        Float316.mod2(res, f)
        fval = res.getValue()
        assert np.mod(x, 2.0) == fval, f"ModTest-1, x={x}, mod2(x)={np.mod(x, 2.0)}, mod2(v)={fval}"

    end_time = time.time()
    print("MOD TEST OK.", end_time - start_time, "sec")


if __name__ == "__main__":
    test_repr()
    test_mult()
    test_greater()
    test_add()
    test_sub()
    test_div()
    test_mod2()
