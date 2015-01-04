% This file contains a very simple illustration of STDP with intergate-and-fire neurons
% (of instant dynamics) using as input patterns the spikes produced by an AER temporal
% contrast retina.
% It illustrates a very simplified version of the simulations shown in the paper
%
%Camunas-Mesa L, Zamarreno-Ramos C, Perez-Carrasco JA, Masquelier T,Serrano-Gotarredona T, and Linares-Barranco B.
% On Spike-Timing-Dependent-Plasticity, Memristive Devices, and building a Self-Learning Visual Cortex. Frontiers in Neuromorphic Engineering.




clear
clf

taum=100e-3; %leakage rate in sec
vt=1; %membrane threshold voltage
vr=0.625; %refractory voltage;
dmax=vt/8; %membrane voltage increment of single spike through max synapse
dinh=vt/2; %membrane voltage inhibitory decrement
tau_plus=17e-3; %tau of positive stdp
tau_minus=34e-3; %tau of negative stdp
a_plus=0.05*dmax; %max inc of pos stdp
a_neg=1.42*(tau_plus/tau_minus)*a_plus; %max decr of neg stdp
NN=16; %number of neurons
stdpM=1; %additive stdp (stdpM=0), mult. stdp (stdpM=1)
start=1; %start random (start=0), start max (start=1)

hystnn=zeros(NN,1); %keep track of spikes for each neuron
ns=zeros(NN,2); %for each neuron store present state and time of last spike

if start==0
    wp=dmax*rand(7,7,NN);
    wn=dmax*rand(7,7,NN);
end
if start==1
    wp=dmax*ones(7,7,NN);
    wn=dmax*ones(7,7,NN);
end
wwp=zeros(7,7,NN,324);
wwn=zeros(7,7,NN,324);

for alliter=1:5
    for iter=1:324
        told=0;
        iold=1;
        ns(:,2)=-4*max(tau_plus,tau_minus);
        s=sprintf('po7x7/po7x7_%d',iter);
        load(s);
        po7x7(:,1)=po7x7(:,1)/1e6;%put event times in sec
        nev=size(po7x7,1);
        for i=1:nev
            time=po7x7(i,1);
            jj=find(ns(:,2)>time-4*tau_minus); %look for negative stdp
            mm=ones(NN,1);
            mm(jj)=0;
            ns(:,1)=ns(:,1)*exp(-(time-told)/taum); %compute leakage since last event
            if po7x7(i,6)==1
                if ~isempty(jj) %do negative stdp of pos input spike
                    for j=1:length(jj)
                        if stdpM==1
                            SS=wp(po7x7(i,4),po7x7(i,5),jj(j))*wp(po7x7(i,4),po7x7(i,5),jj(j));%mult stdp
                        else
                            SS=1;%additive STDP
                        end
                        wp(po7x7(i,4),po7x7(i,5),jj(j))=wp(po7x7(i,4),po7x7(i,5),jj(j))-a_neg*SS*exp(-(time-ns(jj(j),2))/tau_minus);
                        if wp(po7x7(i,4),po7x7(i,5),jj(j))<0
                            wp(po7x7(i,4),po7x7(i,5),jj(j))=0;%clip wp to 0
                        end
                        if wp(po7x7(i,4),po7x7(i,5),jj(j))>dmax
                            error('wp above dmax!!')
                        end
                    end
        %                 trackweights
        %                 i

                end
                ns(:,1)=ns(:,1)+squeeze(wp(po7x7(i,4),po7x7(i,5),:)).*mm; %update membrane voltage, except for those just updated through neg stdp (refr.)
            else
                if ~isempty(jj) %do negative stdp of neg input spike
                    for j=1:length(jj)
                        if stdpM==1
                            SS=wn(po7x7(i,4),po7x7(i,5),jj(j))*wn(po7x7(i,4),po7x7(i,5),jj(j));%mult stdp
                        else
                            SS=1;%additive stdp
                        end
                        wn(po7x7(i,4),po7x7(i,5),jj(j))=wn(po7x7(i,4),po7x7(i,5),jj(j))-a_neg*SS*exp(-(time-ns(jj(j),2))/tau_minus);
                        if wn(po7x7(i,4),po7x7(i,5),jj(j))<0
                            wn(po7x7(i,4),po7x7(i,5),jj(j))=0;% clip wn to 0
                        end
                        if wn(po7x7(i,4),po7x7(i,5),jj(j))>dmax
                            error('wn above dmax!!')
                        end 
                    end
        %                 trackweights
        %                 i
                end
                ns(:,1)=ns(:,1)+squeeze(wn(po7x7(i,4),po7x7(i,5),:)).*mm; %update membrane voltage, except for those just updated through neg stdp (refr.)
            end
            jj=find(ns(:,1)>vt);% check neurons that reached vt
            if ~isempty(jj)
        %         if length(jj)>2
        %             s=sprintf('%d neurons fired simultaneously',length(jj))
        %         end
                ns(jj(1),1)=vr; %only first neuron fires
                hystnn(jj(1))=hystnn(jj(1))+1;
                ns(jj(1),2)=time;
                pp=ones(NN,1);
                pp(jj(1))=0;
                ns(:,1)=ns(:,1)-pp*dinh; %inhibit all other neurons
                if i>1
                    kk=find(po7x7(iold:i,1)>time-4*tau_plus); %do positive stdp
                    for k=1:length(kk)
                        ik=iold+kk(k)-1;
                        if po7x7(ik,6)==1
                            if stdpM==1
                                SS=wp(po7x7(ik,4),po7x7(ik,5),jj(1))*wp(po7x7(ik,4),po7x7(ik,5),jj(1));%mult stdp
                            else
                                SS=1;%additive STDP
                            end
                            wp(po7x7(ik,4),po7x7(ik,5),jj(1))=wp(po7x7(ik,4),po7x7(ik,5),jj(1))+a_plus*SS*exp(-(time-po7x7(ik,1))/tau_plus);
                            if wp(po7x7(ik,4),po7x7(ik,5),jj(1))>dmax
                                wp(po7x7(ik,4),po7x7(ik,5),jj(1))=dmax; %clip wp to dmax
                            end
                            if wp(po7x7(ik,4),po7x7(ik,5),jj(1))<0
                                error('wp below 0!!')
                            end
                        else
                            if stdpM==1
                                SS=wn(po7x7(ik,4),po7x7(ik,5),jj(1))*wn(po7x7(ik,4),po7x7(ik,5),jj(1));%mult stdp
                            else
                                SS=1;%additive stdp
                            end
                            wn(po7x7(ik,4),po7x7(ik,5),jj(1))=wn(po7x7(ik,4),po7x7(ik,5),jj(1))+a_plus*SS*exp(-(time-po7x7(ik,1))/tau_plus);
                            if wn(po7x7(ik,4),po7x7(ik,5),jj(1))>dmax %clip wn to dmax
                                wn(po7x7(ik,4),po7x7(ik,5),jj(1))=dmax;
                            end
                            if wn(po7x7(ik,4),po7x7(ik,5),jj(1))<0
                                error('wn below 0!!')
                            end
                        end
                    end
                    iold=i-length(kk)+1;
                end
            end
            told=time;
        end
        for h=1:NN
            subplot(NN/4,8,2*h-1) %plot of positive weights
            image(wp(:,:,h)/dmax*64)
            axis equal
            axis off
            colormap gray
            subplot(NN/4,8,2*h) %plot of negative weights
            image(wn(:,:,h)/dmax*64)
            axis equal
            axis off
            colormap gray
        end
        drawnow
        iter
        hh=hystnn'
        nev
        wwp(:,:,:,iter)=wp;
        wwn(:,:,:,iter)=wn;
    %     display('Another iter?')
    %     pause
    end
end
save whistory wwp wwn taum vt vr dmax dinh tau_plus tau_minus a_plus a_neg NN stdpM start
        
