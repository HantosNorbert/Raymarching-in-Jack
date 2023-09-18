import numpy as np
import cv2
from dataclasses import dataclass
import math
import time

MIN_DIST = 0.0
MAX_DIST = 12.0
MAX_MARCHING_STEPS = 64
MAX_MARCHING_STEPS_SHADOW = 32
PRECISION = 0.01
EPSILON = 0.005

ditherMatrix = ( 0., 48., 12., 60.,  3., 51., 15., 63.,
                32., 16., 44., 28., 35., 19., 47., 31.,
                 8., 56.,  4., 52., 11., 59.,  7., 55.,
                40., 24., 36., 20., 43., 27., 39., 23.,
                 2., 50., 14., 62.,  1., 49., 13., 61.,
                34., 18., 46., 30., 33., 17., 45., 29.,
                10., 58.,  6., 54.,  9., 57.,  5., 53.,
                42., 26., 38., 22., 41., 25., 37., 21.)


class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, v):
        return Vec3(self.x + v.x, self.y + v.y, self.z + v.z)
    
    def __sub__(self, v):
        return Vec3(self.x - v.x, self.y - v.y, self.z - v.z)
    
    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)
    
    def __mul__(self, c: float):
        return Vec3(self.x * c, self.y * c, self.z * c)

    def __rmul__(self, c):
        return Vec3(self.x * c, self.y * c, self.z * c)


class Mat3:
    def __init__(self, v1x: float, v1y: float, v1z: float, v2x: float, v2y: float, v2z: float, v3x: float, v3y: float, v3z: float):
        # row vectors
        self.v1 = Vec3(v1x, v1y, v1z)
        self.v2 = Vec3(v2x, v2y, v2z)
        self.v3 = Vec3(v3x, v3y, v3z)

    def __mul__(self, v: Vec3):
        return Vec3(dot(self.v1, v), dot(self.v2, v), dot(self.v3, v))


def length(v: Vec3) -> float:
    return math.sqrt(v.x*v.x + v.y*v.y + v.z*v.z)


def length2(f1: float, f2: float):
    return math.sqrt(f1*f1 + f2*f2)


def normalize(p: Vec3) -> Vec3:
    l = length(p)
    return Vec3(p.x/l, p.y/l, p.z/l)


def cross(v1: Vec3, v2: Vec3) -> Vec3:
    return Vec3(v1.y * v2.z - v2.y * v1.z,
                v1.z * v2.x - v2.z * v1.x,
                v1.x * v2.y - v2.x * v1.y)


def dot(v1: Vec3, v2: Vec3) -> float:
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z


@dataclass
class Surface:
    sd: float
    col: float


def sdSphere(p: Vec3, r: float, offset: Vec3, col: float) -> Surface:
    p = p - offset
    d = length(p)-r
    return Surface(d, col)


def sdTorus(p: Vec3, r1: float, r2: float, offset: Vec3, col: float) -> Surface:
  p = p - offset
  d1 = length2(p.x, p.z) - r1
  d2 = length2(d1, p.y) - r2
  return Surface(d2, col)


def sdFloor(p: Vec3, col: float) -> Surface:
  d = p.y + 1.0
  return Surface(d, col)


def unionSDF(obj1: Surface, obj2: Surface) -> Surface:
    if obj1.sd < obj2.sd:
        return obj1
    return obj2


def sdScene(p: Vec3) -> Surface:
    floorColor = 1. + 0.7*((math.floor(p.x) + math.floor(p.z)) % 2)
    floor = sdFloor(p, floorColor)
    sphere = sdSphere(p, 1., Vec3(-1.5, 0., 0.), 0.7)
    torus = sdTorus(p, 1.0, 0.25, Vec3(1.5, 0., 0.), 0.7)
    co = unionSDF(sphere, torus)
    co = unionSDF(co, floor)
    return co


def rayMarch(ro: Vec3, rd: Vec3, maxMarchingSteps: int) -> Surface:
    depth = MIN_DIST
    for i in range(maxMarchingSteps):
        p = ro + depth * rd
        co = sdScene(p)
        depth += co.sd
        if co.sd < PRECISION or depth > MAX_DIST:
            break

    co.sd = depth
    return co


def calcNormal(p: Vec3) -> Vec3:
    exyy = Vec3( EPSILON, -EPSILON, -EPSILON)
    eyyx = Vec3(-EPSILON, -EPSILON,  EPSILON)
    eyxy = Vec3(-EPSILON,  EPSILON, -EPSILON)
    exxx = Vec3( EPSILON,  EPSILON,  EPSILON)
    sd1 = sdScene(p + exyy).sd
    sd2 = sdScene(p + eyyx).sd
    sd3 = sdScene(p + eyxy).sd
    sd4 = sdScene(p + exxx).sd
    return normalize(exyy * sd1 + eyyx * sd2 + eyxy * sd3 + exxx * sd4)


def camera(cameraPos: Vec3, lookAtPoint: Vec3) -> Mat3:
    forward = normalize(cameraPos - lookAtPoint)
    right = normalize(cross(Vec3(0., 1., 0.), forward))
    # up is reversed since the screen Y coordinate is flipped
    up = cross(forward, right)
    return Mat3(right.x, up.x, forward.x,
                right.y, up.y, forward.y,
                right.z, up.z, forward.z)


def angle(v1: Vec3, v2: Vec3) -> float:
    a = dot(v1, v2)
    if a < 0.0:
        return 0.0
    if a > 1.0:
        return 1.0
    return a


def lightIntensity(p: Vec3, norm: Vec3, camPos: Vec3, lightPos: Vec3) -> float:
    kd = 0.9
    ks = 0.7
    id = 0.7
    iss = 0.5
    a = 4.0

    lightDir = normalize(lightPos - p)
    camDir = normalize(camPos - p)

    reflectDir = 2.0 * angle(lightDir, norm) * norm - lightDir
    diffuseLight = kd * angle(lightDir, norm) * id
    specularLight = ks * math.pow(angle(reflectDir, camDir), a) * iss

    return diffuseLight + specularLight


def mainImage(u, v, camMatrix, camPos, backgroundColor, lightPos) -> float:
    rd = camMatrix * normalize(Vec3(u, v, -1.0))
    co = rayMarch(camPos, rd, MAX_MARCHING_STEPS)

    if co.sd > MAX_DIST:
        col = backgroundColor
    else:
        p = camPos + rd * co.sd
        normal = calcNormal(p)

        col = co.col * lightIntensity(p, normal, camPos, lightPos) + 0.2*backgroundColor

        # shadow
        lightDir = normalize(lightPos - p)
        newRayOrigin = p + normal * PRECISION * 2.
        shadowRayLength = rayMarch(newRayOrigin, lightDir, MAX_MARCHING_STEPS_SHADOW).sd
        if shadowRayLength < length(lightPos - newRayOrigin):
            col *= 0.25

    return col


def main():
    screen = np.zeros((256, 512), dtype=np.float32)
    backgroundColor = 0.835
    camPos = Vec3(0., 1.5, 4.)
    lookAt = Vec3(0., 0., 0.)
    lightPos = Vec3(2., 5., -1.)

    camMatrix = camera(camPos, lookAt)

    start_time = time.time()

    for y in range(256):
        for x in range(512):
            u = (x - 0.5*512) / 256
            v = -(y - 0.5*256) / 256

            value = mainImage(u, v, camMatrix, camPos, backgroundColor, lightPos)
            
            if value < 0.0:
                value = 0.0
            elif value > 1.0:
                value = 1.0

            # Ordered dithering
            value = value + ditherMatrix[8 * (y%8) + x%8] / 64.0 - 0.5
            screen[y][x] = 1.0 if value > 0.5 else 0.0

        cv2.imshow("screen", screen)
        if cv2.waitKey(1) == ord('q'):
            exit()

    print(f"Render time: {time.time() - start_time} seconds.")
    cv2.imshow("screen", screen)
    # cv2.imwrite("RayTracer_float.png", screen*255)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()
