function postoffice()

po=dat2mat('postoffice.dat');
for i=1:18
    ymin=2+(i-1)*7;
    ymax=1+i*7;
    for j=1:18
        xmin=2+(j-1)*7;
        xmax=1+j*7;
        k=j+(i-1)*18;
        s=sprintf('po7x7/po7x7_%d',k);
        jj=find(po(:,4)>=xmin&po(:,4)<=xmax&po(:,5)>=ymin&po(:,5)<=ymax);
        po7x7=po(jj,:);
        po7x7(:,4)=po7x7(:,4)-xmin+1;
        po7x7(:,5)=po7x7(:,5)-ymin+1;
        save(s,'po7x7')
    end
end