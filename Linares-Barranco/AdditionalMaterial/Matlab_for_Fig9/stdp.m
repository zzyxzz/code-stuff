clear
th=1.0;
dx=0.01;
x=[-80:dx:80];
delta_t=[-80:0.5:80];
alp=7;

for i= 1 : length(delta_t)
   delta_t(i);
   vdiff = 1.0*f_actP(x)-0.9*f_actP(x+delta_t(i));
   lern(i) = area_th(vdiff,th,dx,alp);
end

figure(1)
plot(delta_t,100*lern/max(abs(lern)),'LineWidth',3)
h=gca;
set(h,'FontSize',16)
set(h,'FontName','Times')
 axis([-80 80 -70 120])
set(h,'XTick',[-80 -40 0 40 80])
xlabel('\it \DeltaT (ms)')
set(h,'YTick',[-40 -20 0 20 40 60 80 100])
ylabel('\xi (%)')
print -depsc2 stdp_matlab.eps

figure(2)
%plot(x,f_actP(x+delta_t(1)),'LineWidth',3)
plot(x,f_actP(x+delta_t(180)),'LineWidth',3)
h=gca;
set(h,'FontSize',16)
set(h,'FontName','Times')
axis([-25 80 -0.5 1.1])
set(h,'XTick',[-20 -10 0 10 20 30 40 50 60 70 80])
xlabel('\it time (ms)')
set(h,'YTick',[-0.5 0 0.5 1])
ylabel('V_{mem}')
print -depsc2 spk.eps

figure(3)
plot(x,vdiff)

