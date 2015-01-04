function out = f_actP_rectTr2(x)
n=length(x);
x1=-6.5;
x2=60;
amp_p=-1;
amp_n=-1.0;

out=zeros(n,1);
if x1>0
    exit(0);
elseif x2<0
    exit(0);
end
i1=find(x>x1&x<0);
out(i1)=-amp_n;
i2=find(x>=0&x<x2);
out(i2)=amp_p - (amp_p/x2)*x(i2);