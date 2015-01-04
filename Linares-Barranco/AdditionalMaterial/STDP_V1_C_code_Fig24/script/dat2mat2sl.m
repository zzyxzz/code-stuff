% spikeList=dat2mat('../data/jAER/Tmpdiff128-2006-02-14T07-45-15-0800-0 walk to kripa.dat');
% spikeList=dat2mat('../data/jAER/events-2005-12-28T11-14-28-0800 drive SC postoffice.dat');
% spikeList=dat2mat('../data/jAER/Tmpdiff128-2006-02-10T14-22-35-0800-0 hand for orientation.dat');
spikeList=dat2mat([path filename]);

spikeList(:,[2 3])=[]; % unuseful columns
% spikeList(1:2.5e6,:)=[]; % something weird in front of the video (enormous number of events)

spikeList(:,1)=spikeList(:,1)/1e6; % micro s -> s
spikeList(:,1)=spikeList(:,1)-spikeList(1,1); % substract offset


N = max(spikeList(:,2));
disp(['Estimated N = ' int2str(N)])
disp(['Avg firing rate = ' num2str(size(spikeList,1)/N/N/2/(spikeList(end,1)-spikeList(1,1))) ' Hz'])

% compute integrated coordinate
spikeList(:,5)=spikeList(:,3)-1+(spikeList(:,2)-1)*N+((spikeList(:,4)+1))/2*N^2; 
spikeList(:,[2 3 4])=[]; % now redundant columns

% swap col 1 and 2
tmp=spikeList(:,2);
spikeList(:,2)=spikeList(:,1);
spikeList(:,1)=tmp;

% tests
disp('issorted(spikeList(:,2))')
issorted(spikeList(:,2))

% figure
% hist(spikeList(:,2),100)

N = round(sqrt((max(spikeList(:,1))+1)/2));
disp(['Estimated N = ' int2str(N)])


% disp('saving spikeList')
% save spikeList spikeList
