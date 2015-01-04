function y = pwlsig(x)
%PWLSIG	piecewise linear sigmoid characteristic.
%	Y = PWLSIG(X) = 0.5 * ABS(X + 1) - 0.5 * ABS(X - 1)

y = abs(x+1)/2 - abs(x-1)/2;

  

