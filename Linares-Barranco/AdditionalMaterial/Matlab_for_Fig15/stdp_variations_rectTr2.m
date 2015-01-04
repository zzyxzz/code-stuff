clear
th=1.0;
dx=0.01;
x=[-80:dx:80];
delta_t=[-80:0.5:80];
alp=7;
for i=1:length(delta_t)
    delta_t(i);
    lern(i) = area_th(+1.0*f_actP_rectTr2(x)+1.0*f_actP_rectTr2(x+delta_t(i)),th,dx,alp);
end
figure(1)
plot(delta_t,100*lern/max(abs(lern)),'LineWidth',3)
h=gca;
set(h,'FontSize',25)
set(h,'FontName','Times')
axis([-80 80 -100 120])
set(h,'XTick',[-80 -40 0 40 80])
xlabel('\it \DeltaT (ms)')
set(h,'YTick',[-80 -60 -40 -20 0 20 40 60 80 100])
ylabel('\xi (%)')
print -depsc2 stdp_matlab_rectTr2.eps

figure(2)
plot(x,f_actP_rectTr2(x),'LineWidth',3)
h=gca;
set(h,'FontSize',25)
set(h,'FontName','Times')
axis([-80 80 -1.1 1.1])
set(h,'XTick',[-80 -40 0 40 80])
xlabel('\it time (ms)')
ylabel('V_{mem}')
print -depsc2 spk_rectTr2.eps

figure(1)