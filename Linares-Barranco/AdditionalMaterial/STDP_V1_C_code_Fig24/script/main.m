% Main script. 
% The main function is the mex file STDPContinuous (see its header for comments)
% timothee.masquelier@alum.mit.edu

param

rand('state',PARAM.randomState);


% load input spike trains
load(['../mat/afferent.rand' sprintf('%03d',PARAM.randomState) '.mat'])

% init neuron
N = round(2^6.5*length(PARAM.epspKernel)*PARAM.tmpResolution*length(spikeList)/spikeList(end));
for nn=1:PARAM.nNeuron %neuron loop
    neuron(nn) = createNewNeuron(PARAM,N);
end %neuron loop

% use previously dumped weight as initial values
if PARAM.useSavedWeight
    filepath = '../mat/';
    dirlist = dir([filepath 'weight.t=*s.txt']);
    if ~isempty(dirlist)
        disp(['Used weights saved in ' filepath dirlist(end).name ])
        weight = load([filepath dirlist(end).name]);
        for nn=1:PARAM.nNeuron
            neuron(nn).weight = weight(nn,:);
        end
    end
end


timedLogLn(['Running (' int2str(length(spikeList)) ' iterations ~ ' int2str(2e-9*length(spikeList)*length(neuron)*(ceil( PARAM.epspMaxTime / PARAM.tmpResolution )+1)) ' min )'])

tic
neuron=STDPContinuous(neuron,spikeList,afferentList,false,PARAM.beSmart,PARAM);
disp(' ');
toc

if sum([neuron.nFiring]) == 0
    warning('Neurons do not fire')
    return;
end

if max([neuron.nFiring])>length(neuron(1).firingTime)
    warning('Increase firingTime array size')
end

% save all
c = clock;
timeTag = [sprintf('%02.0f',c(2)) '.' sprintf('%02.0f',c(3)) '.' sprintf('%02.0f',c(4)) '.' sprintf('%02.0f',c(5)) '.' sprintf('%02.0f',c(6)) ];


clear spikeList
clear afferentList

disp(['Saving results in ../mat/matlab.rand' sprintf('%03d',PARAM.randomState) '.' timeTag '.mat']);
save(['../mat/matlab.rand' sprintf('%03d',PARAM.randomState) '.' timeTag '.mat']);

% display results
plots
