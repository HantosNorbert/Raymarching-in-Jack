# Appendix B - Gallery

![grayscale](grayscale.png)

The grayscale prototype image created with Shadertoy.

![dither threshold](dither_threshold.png)

The simplest dither algorithm: threshold. Every pixel shade below $0.5$ is black, the rest is white.

![dither random](dither_random.png)

Random dithering: every pixel with a grayscale value of $p$ has a probability of $p$ to be white.

![dither floyd](dither_floyd.png)

[Floyd-Steinberg dithering](https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering). It pushes he residual quantization error of a pixel onto its neighboring pixels. Very nice result, but requires a lot of memory to keep the list of error values.

![result](result.png)

The final image Jack produces with $8 \times 8$ ordered dithering.

![ordered dither big](ordered_dither_big.png)

The same image with ordered dithering but with a resolution of $1920 \times 1080$. Open the image separately to see in its full glory!

![result camera change](result_cam_change.png)

Changing the camera position from $(0, 1.5, 4)$ to $(4, 3, 4)$ changes the scenery a lot.

![shadertoy](shadertoy.png)

Animated version created by Shadertoy. Go to https://www.shadertoy.com/view/dtSyDz to see it in real time!
