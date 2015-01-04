function out = f_actP_lin(x)
n=length(x);
x1=-30;
x2=60;
amp1=1;
amp2=0.5;
if x1>0
    exit(0);
elseif x2<0
    exit(0);
end

out=zeros(n,1);
i1=find(x>x1&x<0);
out(i1)=(amp1/abs(x1))*(-x1+x(i1));
i2=find(x>=0&x<x2);
out(i2)=(amp2/x2)*(-x2+x(i2));