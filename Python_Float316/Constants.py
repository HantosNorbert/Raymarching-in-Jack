from Float316 import Float316
from Vec3 import Vec3

class Constants:
    CONST_MINUS_ONE = Float316(1, 127, 8192)  # -1.0
    CONST_QUARTER = Float316(0, 125, 8192)  # 0.25
    CONST_HALF = Float316(0, 126, 8192)  # 0.5
    CONST_ONE = Float316(0, 127, 8192)  # 1.0
    CONST_THREE_HALFS = Float316(0, 127, 12288)  # 1.5

    CONST_IMG_WIDTH = Float316(0, 136, 8192)  # 512.0
    CONST_IMG_HALF_WIDTH = Float316(0, 135, 8192)  # 256.0
    CONST_IMG_HEIGHT = Float316(0, 135, 8192)  # 256.0
    CONST_IMG_HALF_HEIGHT = Float316(0, 134, 8192)  # 128.0

    CONST_UP = Vec3(Float316(0, 0, 0), Float316(0, 127, 8192), Float316(0, 0, 0))  # (0.0, 1.0, 0.0)

    # Ordered dithering 8x8 threshold map values
    # See https://en.wikipedia.org/wiki/Ordered_dithering
    CONST_DITHER = [Float316(1, 126,  8192),  #  0/64 - 0.5
                    Float316(0, 125,  8192),  # 48/64 - 0.5
                    Float316(1, 125, 10240),  # 12/64 - 0.5
                    Float316(0, 125, 14336),  # 60/64 - 0.5
                    Float316(1, 125, 14848),  #  3/64 - 0.5
                    Float316(0, 125,  9728),  # 51/64 - 0.5
                    Float316(1, 125,  8704),  # 15/64 - 0.5
                    Float316(0, 125, 15872),  # 63/64 - 0.5

                    Float316(0,   0,     0),  # 32/64 - 0.5
                    Float316(1, 125,  8192),  # 16/64 - 0.5
                    Float316(0, 124, 12288),  # 44/64 - 0.5
                    Float316(1, 123,  8192),  # 28/64 - 0.5
                    Float316(0, 122, 12288),  # 35/64 - 0.5
                    Float316(1, 124, 13312),  # 19/64 - 0.5
                    Float316(0, 124, 15360),  # 47/64 - 0.5
                    Float316(1, 121,  8192),  # 31/64 - 0.5

                    Float316(1, 125, 12288),  #  8/64 - 0.5
                    Float316(0, 125, 12288),  # 56/64 - 0.5
                    Float316(1, 125, 14336),  #  4/64 - 0.5
                    Float316(0, 125, 10240),  # 52/64 - 0.5
                    Float316(1, 125, 10752),  # 11/64 - 0.5
                    Float316(0, 125, 13824),  # 59/64 - 0.5
                    Float316(1, 125, 12800),  #  7/64 - 0.5
                    Float316(0, 125, 11776),  # 55/64 - 0.5

                    Float316(0, 124,  8192),  # 40/64 - 0.5
                    Float316(1, 124,  8192),  # 24/64 - 0.5
                    Float316(0, 123,  8192),  # 36/64 - 0.5
                    Float316(1, 124, 12288),  # 20/64 - 0.5
                    Float316(0, 124, 11264),  # 43/64 - 0.5
                    Float316(1, 123, 10240),  # 27/64 - 0.5
                    Float316(0, 123, 14336),  # 39/64 - 0.5
                    Float316(1, 124,  9216),  # 23/64 - 0.5

                    Float316(1, 125, 15360),  #  2/64 - 0.5
                    Float316(0, 125,  9216),  # 50/64 - 0.5
                    Float316(1, 125,  9216),  # 14/64 - 0.5
                    Float316(0, 125, 15360),  # 62/64 - 0.5
                    Float316(1, 125, 15872),  #  1/64 - 0.5
                    Float316(0, 125,  8704),  # 49/64 - 0.5
                    Float316(1, 125,  9728),  # 13/64 - 0.5
                    Float316(0, 125, 14848),  # 61/64 - 0.5

                    Float316(0, 122,  8192),  # 34/64 - 0.5
                    Float316(1, 124, 14336),  # 18/64 - 0.5
                    Float316(0, 124, 14336),  # 46/64 - 0.5
                    Float316(1, 122,  8192),  # 30/64 - 0.5
                    Float316(0, 121,  8192),  # 33/64 - 0.5
                    Float316(1, 124, 15360),  # 17/64 - 0.5
                    Float316(0, 124, 13312),  # 45/64 - 0.5
                    Float316(1, 122, 12288),  # 29/64 - 0.5

                    Float316(1, 125, 11264),  # 10/64 - 0.5
                    Float316(0, 125, 13312),  # 58/64 - 0.5
                    Float316(1, 125, 13312),  #  6/64 - 0.5
                    Float316(0, 125, 11264),  # 54/64 - 0.5
                    Float316(1, 125, 11776),  #  9/64 - 0.5
                    Float316(0, 125, 12800),  # 57/64 - 0.5
                    Float316(1, 125, 13824),  #  5/64 - 0.5
                    Float316(0, 125, 10752),  # 53/64 - 0.5

                    Float316(0, 124, 10240),  # 42/64 - 0.5
                    Float316(1, 123, 12288),  # 26/64 - 0.5
                    Float316(0, 123, 12288),  # 38/64 - 0.5
                    Float316(1, 124, 10240),  # 22/64 - 0.5
                    Float316(0, 124,  9216),  # 41/64 - 0.5
                    Float316(1, 123, 14336),  # 25/64 - 0.5
                    Float316(0, 123, 10240),  # 37/64 - 0.5
                    Float316(1, 124, 11264)   # 21/64 - 0.5
                    ]
