function dx = cnnderiv(t,x)
%CNNDERIV derivative of 2D CNN
% takes and returns current state as
% a column vector.
%       requires global variables A Bu I m n 
 
global A Bu I m n 

x = reshape(x,m,n);

dx = -x + conv2(pwlsig(x),A,'same') + Bu + I ;

dx = dx(:);









