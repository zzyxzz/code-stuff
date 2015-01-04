function out = f_actP_P7(x)
x=abs(x);
n=length(x);
x1=-20;
x2=-1;
x3=1;
x4=20;
x5=40;
amp1=-0.6;
amp2=1.0;
amp3=0.0;

out=zeros(n,1);
if x1>0
    exit(0);
elseif x5<0
    exit(0);
end
i1=find(x>=x1&x<x2);
out(i1)=(amp1/(x2-x1))*(x(i1)-x1);
i2=find(x>=x2&x<0);
out(i2)=((amp2-amp1)/(-x2))*(x(i2)-x2)+amp1;
i3=find(x>=0&x<x3);
out(i3)=((amp1-amp2)/x3)*x(i3)+amp2;
i4=find(x>=x3&x<x4);
out(i4)=((amp3-amp1)/(x4-x3))*(x(i4)-x3)+amp1;
i5=find(x>=x4&x<=x5);
out(i5)=((-amp3)/(x5-x4))*(x(i5)-x5);