function write_po7x7_files()

VA=1; %peak voltage of square part
VB=-0.5; %peak voltage of triangular part
Vrest=0.0; %resting voltage
t1=0.5e-3; %width of square part
t2=67.48e-3; %width of triangle part
tr=1e-5; %rise time of first square part
tf=1e-5; %transition time from square to triangle
Ttot=tr+t1+tf+t2; % total spike time
Tdelta=Ttot; %minimum inter-spike time for the same pixel and sign
Tstart=0; %start time

load po7x7/po7x7_145
% po7x7(:,4)=po7x7(:,4)-60;
% po7x7(:,5)=po7x7(:,5)-60;
po7x7(:,1)=po7x7(:,1)/1e6;
jj=find(po7x7(:,1)>=3.7);
po7x7=po7x7(jj,:);
po7x7(:,1)=po7x7(:,1)-po7x7(1,1)+1e-3;
Tmax=max(po7x7(:,1))+Ttot+Tdelta;
np=zeros(1,49);
nn=zeros(1,49);
for i=1:49
    sp=sprintf('stims/p%d',i);
    fp=fopen(sp,'w');
    fprintf(fp,'%15.10e %15.10e\n',Tstart,Vrest);
    sn=sprintf('stims/n%d',i);
    fn=fopen(sn,'w');
    fprintf(fn,'%15.10e %15.10e\n',Tstart,Vrest);
    yi=floor((i-1)/7)+1;
    xi=i-(yi-1)*7;
    jjp=find(po7x7(:,4)==xi&po7x7(:,5)==yi&po7x7(:,6)==-1);
    jjn=find(po7x7(:,4)==xi&po7x7(:,5)==yi&po7x7(:,6)==1);
    np(i)=length(jjp);
    nn(i)=length(jjn);
    Tp=-1;
    for j=1:length(jjp)
        Tev=po7x7(jjp(j),1);
        if Tev>Tp
            fprintf(fp,'%15.10e %15.10e\n',Tev,Vrest);
            fprintf(fp,'%15.10e %15.10e\n',Tev+tr,VA);
            fprintf(fp,'%15.10e %15.10e\n',Tev+tr+t1,VA);
            fprintf(fp,'%15.10e %15.10e\n',Tev+tr+t1+tf,VB);
            fprintf(fp,'%15.10e %15.10e\n',Tev+tr+t1+tf+t2,Vrest);
            Tp=Tev+Ttot+Tdelta;
        end
    end
    fprintf(fp,'%15.10e %15.10e\n',max(Tmax,Tp),Vrest);
    fclose(fp);
    Tn=-1;
    for j=1:length(jjn)
        Tev=po7x7(jjn(j),1);
        if Tev>Tn
            fprintf(fn,'%15.10e %15.10e\n',Tev,Vrest);
            fprintf(fn,'%15.10e %15.10e\n',Tev+tr,VA);
            fprintf(fn,'%15.10e %15.10e\n',Tev+tr+t1,VA);
            fprintf(fn,'%15.10e %15.10e\n',Tev+tr+t1+tf,VB);
            fprintf(fn,'%15.10e %15.10e\n',Tev+tr+t1+tf+t2,Vrest);
            Tn=Tev+Ttot+Tdelta;
        end
    end
    fprintf(fn,'%15.10e %15.10e\n',max(Tmax,Tn),Vrest);
    fclose(fn);
end
plot([np;nn]')
xlabel('neuron number')
ylabel('number of spikes per neuron')
display(sprintf('Total spikes = %d',sum(np)+sum(nn)));
    