clear
clf
VA=1;
t1=1e-3;
gain_pre=0.9;
gain_pos=1.0;
sw=80e-3; %half stdp time window
pw=1e-3; %spike width
NN=10000;
Delta_t=zeros(NN,1);
Delta_w=zeros(NN,1);
k=1;

load -ascii stdp.dat
save stdp stdp
% load stdp
time=stdp(:,1);
pos=stdp(:,2);
pre=stdp(:,3);
w=stdp(:,4);
t_pos=-10*sw;
t_pre=-10*sw;

imax=length(time);
for i=2:imax;
    if pre(i)>pre(i-1)&&pre(i)>=gain_pre*VA/2&&pre(i-1)<gain_pre*VA/2
        t_pre_new=time(i-1);
        dt=t_pre_new-t_pos;
        if dt<sw
            w1=w(i-1);
            [a ii]=min(abs(time(i-1:min(i+1000,imax))-(time(i-1)+2*pw)));
            w2=w(i-1+ii);
            Delta_w(k)=(1/w2-1/w1)/(((1/w1+1/w2)/2)^2);%for R memristor
            Delta_t(k)=-dt;
            if floor(k/NN)*NN==k
                Delta_t=[Delta_t;zeros(NN,1)];
                Delta_w=[Delta_w;zeros(NN,1)];
            end
            k=k+1;
        end
        t_pre=t_pre_new;
    end
    if pos(i)>pos(i-1)&&pos(i)>=gain_pos*VA/2&&pos(i-1)<gain_pos*VA/2
        t_pos_new=time(i-1);
        dt=t_pos_new-t_pre;
        if dt<sw
            w1=w(i-1);
            [a ii]=min(abs(time(i-1:min(i+1000,imax))-(time(i-1)+2*pw)));
            w2=w(i-1+ii);
            Delta_w(k)=(1/w2-1/w1)/(((1/w1+1/w2)/2)^2);%for R memristor
            Delta_t(k)=dt;
            if floor(k/NN)*NN==k
                Delta_t=[Delta_t;zeros(NN,1)];
                Delta_w=[Delta_w;zeros(NN,1)];
            end
            k=k+1;
        end
        t_pos=t_pos_new;
    end
end
Delta_t=Delta_t(1:k-1);
Delta_w=Delta_w(1:k-1);
plot(Delta_t*1000,Delta_w,'.')

f=[Delta_t,Delta_w];
[fs,gs]=sort(f,1);
fs(:,2)=f(gs(:,1),2);
fsd=diff(fs);
in=find(fs(:,1)<0);
n1=length(in);
An=sum(fsd(1:n1,1).*fs(2:n1+1,2));
Ap=sum(fsd(n1+1:end,1).*fs(n1+2:end,2));
An/Ap

hold on
xn=[-80e-3:4e-3:0];
xp=[0:4e-3:80e-3];
taup=13.6e-3;
taun=15.2e-3;
ap=max(Delta_w);
an=1.12*ap;
yp=ap*exp(-xp/taup);
yn=-an*exp(xn/taun);
plot(xp*1000,yp,'ro-','MarkerSize',10)
plot(xn*1000,yn,'ro-','MarkerSize',10)
hold off
set(gca,'FontSize',15,'FontName','Times')
xlabel('\it \DeltaT (ms)')
ylabel('\it \DeltaG/G^2 (M\Omega)')
axis([-80 80 -1.5 1.5])
