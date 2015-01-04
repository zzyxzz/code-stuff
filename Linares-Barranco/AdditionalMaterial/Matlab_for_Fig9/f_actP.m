function out = f_actP(x)
n=length(x);
x1=-5;
x2=75;
amp_p=-0.25;
amp_n=-1;
xop=40;
xon=3;
out=zeros(n,1);
if x1>0
    exit(0);
elseif x2<0
    exit(0);
end
i1=find(x>x1&x<0);
out(i1)=-amp_n*(exp(x(i1)/xon)-exp(x1/xon))/(1-exp(x1/xon));
i2=find(x>0&x<x2);
out(i2)=amp_p*(exp(-x(i2)/xop)-exp(-x2/xop))/(1-exp(-x2/xop));
