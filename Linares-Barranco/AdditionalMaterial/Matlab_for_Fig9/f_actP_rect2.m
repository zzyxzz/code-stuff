function out = f_actP_rect2(x)
n=length(x);
x1=-2.5;
x2=38;
amp_p=-0.3;
amp_n=-1;
if x1>0
    exit(0);
elseif x2<0
    exit(0);
end

out=zeros(n,1);
i1=find(x>x1&x<0);
out(i1)=-amp_n;
i2=find(x>=0&x<x2);
out(i2)=amp_p;