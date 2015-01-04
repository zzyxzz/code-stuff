randState = 0;

N = round(sqrt((max(spikeList(:,1))+1)/2));
disp(['Estimated N = ' int2str(N)])

n = 7;
% n = N;

    i=mod(spikeList(:,1),N);
    j=mod(floor(spikeList(:,1)/N),N);
    k=floor(spikeList(:,1)/N^2);

delta = n;%round(n/2);
K = floor((N-n)/delta);

cursor=1;
SL = zeros(length(spikeList),2);

IJ = zeros(2,(K+1)^2);
IJ(1,:)=floor( (0:length(IJ)-1)/(K+1) );
IJ(2,:)=mod( (0:length(IJ)-1), (K+1) );

rand('state',randState)
IJ = IJ(:,randperm((K+1)^2)); % concatenate the crops in a random order

for r=1:length(IJ)

    timedLog(['RF = [' int2str(IJ(1,r)*delta) ',' int2str(IJ(1,r)*delta+n) '[ , [' int2str(IJ(2,r)*delta) ',' int2str(IJ(2,r)*delta+n) '['])
    % crop
    idx = i>=IJ(1,r)*delta & i<IJ(1,r)*delta+n & j>=IJ(2,r)*delta & j<IJ(2,r)*delta+n;
    data = spikeList(idx,:);

    % new ref
    data(:,1) = (i(idx)-IJ(1,r)*delta) + n*(j(idx)-IJ(2,r)*delta) + n^2 * k(idx);

    %         return

    d = size(data,1);
    if d>0
        if cursor==1
            SL(cursor:cursor+d-1,:) = [ data(:,1), data(:,2)-data(1,2)];
        else
            SL(cursor:cursor+d-1,:) = [ data(:,1), data(:,2)-data(1,2)+SL(cursor-1,2)];
        end
        cursor = cursor+d;
    end

end

clear spikeList

% trunc unused
if cursor == length(SL)+1
    warning('Increase initial SL array size for better performance')
end
SL(cursor:end,:) = [];


% save in appropriate format for mex file STDPContinuous
spikeList = SL(:,2)';
afferentList = uint16(SL(:,1))';
clear SL
disp(['Saving in ../mat/afferent.rand' sprintf('%03d',randState) '.mat'])
save(['../mat/afferent.rand' sprintf('%03d',randState) '.mat'],'spikeList','afferentList')
