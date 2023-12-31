# Appendix B - Gallery

![grayscale](grayscale_normal_size.png)

The grayscale prototype image created with Python, with built-in `float` numbers.

&nbsp;

&nbsp;

![dither threshold](dither_threshold.png)

The simplest dither algorithm: threshold. Every pixel that has a grayscale value of $0.5$ or higher is white, the rest is black. This is why we need proper dithering.

&nbsp;

&nbsp;

![dither random](dither_random.png)

Random dithering: instead of painting a pixel white if its grayscale value is high, we paint it white only *with certain probability*. Since the grayscale value is already between $0$ and $1$, that can be the probability value itself. So a white-ish (but not completely white) area will still contain some black pixels. A gray area should have white and black pixels in equal amount. The result is still far from satisfying - but it's a good effort.

&nbsp;

&nbsp;

![dither floyd](dither_floyd.png)

[Floyd-Steinberg dithering](https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering). For each pixel we apply a simple threshold, but then we push the difference (called *residual quantization error*) to its neighbours. A white-ish area will contain a lot of white pixels, until the error grows too large and a black pixel appear. The resulted image is very nice, but the algorithm requires to keep a lot of error values in memory, which I wanted to avoid in Jack/Hack. Alex Quach used this algorithm in his [Jack raytracer](https://blog.alexqua.ch/posts/from-nand-to-raytracer/).

&nbsp;

&nbsp;

![result](result.png)

The final image we produce, with an $8 \times 8$ ordered dithering.

&nbsp;

&nbsp;

![result_4x4](dither_4x4.png)

The same image but with a $4 \times 4$ ordered dithering.

&nbsp;

&nbsp;

![result_2x2](dither_2x2.png)

A $2 \times 2$ ordered dithering is only slightly better than a simple threshold.

&nbsp;

&nbsp;

![ordered dither big](ordered_dither_big.png)

The same image with an $8 \times 8$ ordered dithering, but with a resolution of $1920 \times 1080$. Open the image separately to see in its full glory!

&nbsp;

&nbsp;

![result camera change](result_cam_change.png)

Changing the camera position from $(0, 1.5, 4)$ to $(4, 3, 4)$ changes our view on the world. In the Python code, it means we swap the line

`PARAM_cameraPos = Vec3(Float316(0, 0, 0), Float316(0, 127, 12288), Float316(0, 129, 8192))`

with

`PARAM_cameraPos = Vec3(Float316(0, 129, 8192), Float316(0, 128, 12288), Float316(0, 129, 8192))`

in the `Parameters.py` file.

&nbsp;

&nbsp;

![result position change](result_pos_change.png)

We can even change the position of the objects. The sphere was moved from $(-1.5, 0, 0)$ to $(0, 0, 0)$, and the torus from $(1.5, 0, 0)$ to $(0, -0.25, 0)$. In the Python code, we changed the lines

`PARAM_spherePos = Vec3(Float316(1, 127, 12288), Float316(0, 0, 0), Float316(0, 0, 0))`

`PARAM_torusPos =  Vec3(Float316(0, 127, 12288), Float316(0, 0, 0), Float316(0, 0, 0))`

to

`PARAM_spherePos = Vec3(Float316(0, 0, 0), Float316(0, 0, 0), Float316(0, 0, 0))`

`PARAM_torusPos =  Vec3(Float316(0, 0, 0), Float316(1, 125, 8192), Float316(0, 0, 0))`

in the `Parameters.py` file.

&nbsp;

&nbsp;

![result sd change](result_sd_change.png)

"How many toruses do you want?"  "YES."

This happens when we apply the infinite repetition trick on the $\text{SDF}$, see [here](https://iquilezles.org/articles/distfunctions/). The floor, the sphere, and shadow rays are turned off.

&nbsp;

&nbsp;

![colorful](colorful.png)

A step towards reality: colors, texture and [displacement mapping](https://en.wikipedia.org/wiki/Displacement_mapping) on the sphere, reflective surface on the torus, soft shadows, fog effect. Too bad it's above the Hack machine's paygrade! See https://www.shadertoy.com/view/csVyz1 in animation.

&nbsp;

&nbsp;

![shadertoy](shadertoy.png)

Animated version created by Shadertoy. Go to https://www.shadertoy.com/view/dtSyDz to see it in real time!
