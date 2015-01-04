global A B Bu I m n;
global Im1;
Im1 = imread('lena.bmp');

if (isrgb(Im1))
 Im1=rgb2gray(Im1);  
end    
%imshow(Im1);

Ta=zeros(3,3);
Ta(1,1)=0;
Ta(1,2)=0;
Ta(1,3)=0;
Ta(2,1)=1;
Ta(2,2)=2;
Ta(2,3)=1;
Ta(3,1)=0;
Ta(3,2)=0;
Ta(3,3)=0;

Tb=zeros(3,3);
Tb(1,1)=0;
Tb(1,2)=0;
Tb(1,3)=0;
Tb(2,1)=0;
Tb(2,2)=0;
Tb(2,3)=0;
Tb(3,1)=0;
Tb(3,2)=0;
Tb(3,3)=0;

I=0;

A=Ta
B=Tb
u = im2double(Im1);
uu = im2double(max(max(u)));
ul = im2double(min(min(u)));
%figure, imshow(uu)
u = (u-ul)/(uu-ul)*2-1;
%figure,imshow(u)
x0 = u;

colormap(gray(64))

t = 0;
Xt = x0;
tf = 1;
dtime = 0.1;
m=0;
n=0;
global Im2;

%----------------- Start Calculation CNN ------------------------
while(t<tf)
 Im2=image((pwlsig(Xt)+1)*32); 
 %axis('image');
 %drawnow
 %figure, imshow(Im2);
 tnext = min([tf,t+dtime]);

 Atem = A;
 Bu = conv2(u,B,'same');
 [m,n] = size(x0);
 x0 = x0(:);
 [t,y] = ode23('cnnderiv', [0, tf/2, tf], x0);
 ly = size(y,1);
 x0 = reshape(y(ly,:),m,n);
 Xt=x0;
 
 t = tnext;
 %pause(0.01);

end;