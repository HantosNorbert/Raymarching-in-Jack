from Float316 import Float316
from Constants import Constants
from CalcPixel import CalcPixel

# The main attraction.
class ImageRenderer:
    # The main function: iterate through all the pixels, calculate their
    # intensity value, apply dithering, and finally draw that pixel
    @staticmethod
    def render():
        import numpy as np
        import cv2
        import time

        start_time = time.time()

        screen = np.ones((256, 512), dtype=np.float32)

        pixelValue = Float316(0, 0, 0)

        u = Float316(0, 0, 0)
        v = Float316(0, 0, 0)
        x = Float316(0, 0, 0)
        y = Float316(0, 0, 0)
        xInt = 0
        yInt = 0

        xIntMod8 = 0
        yIntMod8 = 0

        # For every row
        while Constants.CONST_IMG_HEIGHT.gt(y):
            x.s = 0
            x.e = 0
            x.m = 0
            xInt = 0
            # For every column
            while Constants.CONST_IMG_WIDTH.gt(x):
                # (u,v) normalized coordinates from (x,y)
                # u = (x - 0.5*512) / 256
                Float316.sub(u, x, Constants.CONST_IMG_HALF_WIDTH)
                Float316.div(u, u, Constants.CONST_IMG_HEIGHT)

                # v = -(y - 0.5*256) / 256
                Float316.sub(v, y, Constants.CONST_IMG_HALF_HEIGHT)
                Float316.div(v, v, Constants.CONST_IMG_HEIGHT)
                Float316.swapSign(v)

                # let's do this...
                CalcPixel.calcPixelValue(pixelValue, u, v)

                # if value > 1.0, value = 1.0
                if pixelValue.gt(Constants.CONST_ONE):
                    pixelValue.s = 0
                    pixelValue.e = 127
                    pixelValue.m = 8192
                # if value < 0.0, value = 0.0
                elif pixelValue.s == 1:
                    pixelValue.s = 0
                    pixelValue.e = 0
                    pixelValue.m = 0

                # Ordered dithering
                Float316.add(pixelValue, pixelValue, Constants.CONST_DITHER[yIntMod8 * 8 + xIntMod8])

                # draw that pixel
                # screen[255-yInt][511-xInt] = value.getValue()
                if pixelValue.gt(Constants.CONST_HALF):
                    screen[yInt][xInt] = 1.0
                else:
                    screen[yInt][xInt] = 0.0

                # increment x related variables
                Float316.add(x, x, Constants.CONST_ONE)
                xInt = xInt + 1
                xIntMod8 = xIntMod8 + 1
                if xIntMod8 > 7:
                    xIntMod8 = 0

            # increment y related variables
            Float316.add(y, y, Constants.CONST_ONE)
            yInt = yInt + 1
            yIntMod8 = yIntMod8 + 1
            if yIntMod8 > 7:
                yIntMod8 = 0

            cv2.imshow("screen", screen)
            if cv2.waitKey(1) == ord('q'):
                exit()

        print(f"Render time: {time.time() - start_time} seconds.")
        # cv2.imwrite("RayTracer_float316.png", screen*255)
        cv2.waitKey(0)               
