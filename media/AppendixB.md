# Appendix B - Gallery

![grayscale](grayscale.png)

*The grayscale prototype image created with Shadertoy*

![dither threshold](dither_threshold.png)

*The simplest dither algorithm: threshold. Every pixel shade below* $0.5$ *is black, the rest is white*

![dither random](dither_random.png)

*Random dithering: every pixel with a grayscale value of* $p$ *has a probability of* $p$ *to be white*

![dither floyd](dither_floyd.png)

*[Floyd-Steinberg dithering](https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering). It pushes he residual quantization error of a pixel onto its neighboring pixels. Very nice result, but requires a lot of memory to keep the list of error values*

TODO: shadertoy animation, dithered big resolution, python-real, different dithering
