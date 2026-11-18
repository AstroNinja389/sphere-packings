"""A priori index cap in dimension 17 (interval arithmetic): B exp(11/100)/c < 80, c = V_17 2^(-19/2), B = 0.013875579669877."""
from mpmath import iv
iv.dps = 40
B = iv.mpf('0.013875579669877'); c = iv.pi**(iv.mpf(17)/2)/iv.gamma(iv.mpf(17)/2+1)/iv.mpf(2)**(iv.mpf(19)/2)
x = B*iv.exp(iv.mpf(11)/100)/c; assert x.b < 80 and x.a > 79, x
print('A PRIORI INDEX CAP 79: B exp(11/100)/c in', x, '; 64 c <=', (64*c).b)
