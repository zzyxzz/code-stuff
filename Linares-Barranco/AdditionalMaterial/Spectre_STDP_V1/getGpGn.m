plottime=600; %600 is maximum time

for ip=0:783
    ip
    [a w]=system(sprintf('cat RPSfiles/x%03d',ip));
    DD=str2num(w(105:end));
    D0=DD(1:100:end,:);
    if ip==0
        DRp=D0;
    else
        DRp=[DRp D0(:,2)];
    end
end
save DRp DRp

for in=0:783
    in
    [a w]=system(sprintf('cat RNSfiles/x%03d',in));
    DD=str2num(w(105:end));
    D0=DD(1:100:end,:);
    if in==0
        DRn=D0;
    else
        DRn=[DRn D0(:,2)];
    end
end
save DRn DRn

[m iip]=min(abs(DRp(:,1)-plottime));
mrp=reshape(DRp(iip,2:end),7,7,16);
[m iin]=min(abs(DRn(:,1)-plottime));
mrn=reshape(DRn(iin,2:end),7,7,16);
mm=1./mrp-1./mrn;
mm=mm-min(min(min(mm)));
for i=1:16
    ww1=1./squeeze(mm(:,:,i));
    iy=floor((i-1)/8);
    ix=i-iy*8-1;
    dd=0.12;
    dddy=0.03;
    dddx=0.00;
    ofsy=0.04;
    ofsx=0.02;
    subplot('Position',[ix*dd+(ix-1)*dddx+ofsx iy*dd+(iy-1)*dddy+ofsy dd dd])
    imagesc(ww1+1)
    axis equal
    axis off
    h=line([0.5 0.5 7.5 7.5 0.5],[0.5 7.5 7.5 0.5 0.5]);
    set(h,'Color',[0 0 0])
    colormap gray
end

print -depsc2 V1spectre.eps