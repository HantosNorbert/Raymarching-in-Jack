## Float316 Functions in Detail

### Normalization of Float316 Numbers

Ignoring the sign for a moment, our `Float316` number's real form is $m\cdot2^e$ (since we store the explicit 1 in $m$, we don't have to add it to $m$ anymore).

If we right-shift the bits of the mantissa, we actually halve the number, because new each mantissa bit contributes half as much to the real number. A mantissa that starts as `001110...` can be deciphered as

$$\mathbf{0} \cdot 4 + \mathbf{0} \cdot 2 + \mathbf{1} \cdot 1 + \mathbf{1} \cdot \frac{1}{2} + \mathbf{1} \cdot \frac{1}{4} + \mathbf{0} \cdot \frac{1}{8} + \dots = 0.75$$

After a bit-shift to the right, it becomes `000111`, thus:

$$\mathbf{0} \cdot 4 + \mathbf{0} \cdot 2 + \mathbf{0} \cdot 1 + \mathbf{1} \cdot \frac{1}{2} + \mathbf{1} \cdot \frac{1}{4} + \mathbf{1} \cdot \frac{1}{8} + \dots = 0.375$$
