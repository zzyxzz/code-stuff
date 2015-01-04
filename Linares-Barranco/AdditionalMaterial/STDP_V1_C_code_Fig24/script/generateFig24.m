delete('../mat/*.txt')
main

load ../mat/weight.t=0000000.000s.txt
weight=weight_t_0000000_000s';
clear weight_t_0000000_000s;
save weight_0.mat weight

load ../mat/weight.t=0085171.135s.txt
weight=weight_t_0085171_135s';
clear weight_t_0085171_135s
save weight_0.5.mat weight

load ../mat/weight.t=0168315.457s.txt
weight=weight_t_0168315_457s';
clear weight_t_0168315_457s;
save weight_1.mat weight

main
main
main
main

load ../mat/weight.t=0168315.457s.txt
weight=weight_t_0168315_457s';
clear weight_t_0168315_457s;
save weight_5.mat weight

names=cell(1,4);
names{1}='weight_0.mat';
names{2}='weight_0.5.mat';
names{3}='weight_1.mat';
names{4}='weight_5.mat';

nfigs=length(get(0,'Children'));
for nn=1:4
load(names{nn})
N=7; % RF size
for i=1:size(weight,2)
    ww1=reshape(weight(1:N*N,i),N,N);
    ww2=reshape(weight(N*N+1:2*N*N,i),N,N);
   figure(nfigs+nn)
    iy=floor((i-1)/8);
    ix=i-iy*8-1;
    dd=0.12;
    dddy=0.03;
    dddx=0.00;
    ofsy=0.04;
    ofsx=0.02;
    subplot('Position',[ix*dd+(ix-1)*dddx+ofsx iy*dd+(iy-1)*dddy+ofsy dd dd])
    image((ww1-ww2+1)*32)
    axis equal
    axis off
    h=line([0.5 0.5 7.5 7.5 0.5],[0.5 7.5 7.5 0.5 0.5]);
    set(h,'Color',[0 0 0])
    colormap gray
    s=sprintf('recfields%d.eps',nn);
    print('-depsc2',s);
end
end
