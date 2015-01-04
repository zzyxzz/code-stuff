% Parameters. The current configuration corresponds to the main simulation in:
% Camunas-Mesa L, Zamarreno-Ramos C, Perez-Carrasco JA, Masquelier T,Serrano-Gotarredona T, and Linares-Barranco B (in press). On Spike-Timing-Dependent-Plasticity, Memristive Devices, and building a Self-Learning Visual Cortex. Frontiers in Neuromorphic Engineering
% timothee.masquelier@alum.mit.edu

global PARAM

clear all
global PARAM

PARAM.dump=false; %if true the mex file STDPContinuous will dump potential as a function of time in a file called dump.txt
PARAM.beSmart=true; % save time by not computing the potential when it is estimated that the threshold cannot be reached. Rigorous only when no inhibition, and no PSP Kernel. Otherwise use at your own risks...

% not used anymore
PARAM.fixedFiringMode = false;
PARAM.fixedFiringLatency = 10e-3;
PARAM.fixedFiringPeriod = 150e-3;

% Random generators
PARAM.randomState = 0;

PARAM.useSavedWeight = true; % if true the code will look for previously dumped weights in ../mat/weight.t=*.txt and used the latest dumped weights as initial values

%********
%* STDP *
%********
PARAM.stdp_t_pos = 13.6e-3; % memristor value
PARAM.stdp_t_neg = 15.2e-3; %memristor value
PARAM.stdp_a_pos = 1e-2; % avoid > 2^-5
PARAM.stdp_a_neg = - 1.25 * PARAM.stdp_t_pos/PARAM.stdp_t_neg * PARAM.stdp_a_pos; %
PARAM.stdp_cut = 7;
PARAM.minWeight = 0.1; % minimal normalized weight. Memristors have a ~10 fold resistance range so minWeight ~ 0.1*maxWeight

%***************
%* EPSP Kernel *
%***************
PARAM.tm = 10e-3; % membrane time constant (typically 10-30ms)
PARAM.ts = PARAM.tm/4; % synapse time constant
PARAM.epspCut = 5;% specifies after how many ms we neglect the epsp
PARAM.tmpResolution = 1e-3;

PARAM.memristor = true; % use memristor based quadratic STDP
PARAM.t_op = .0005; % end of linear region for LDP
PARAM.t_on = .0005; % end of linear region for LTD
if PARAM.memristor     % EPSP suitable for STDP with memristors (see paper)
    tn = 3e-3;
    tp = 40e-3;
    t1 = 5e-3;
    t2 = 75e-3;
    An = 1;
    Ap = An/4;
    current = [ -An/(exp(t1/tn)-1)*(exp([PARAM.tmpResolution:PARAM.tmpResolution:t1]/tn)-1) Ap/(exp(t2/tp)-1)*(exp((t1+t2-[t1+PARAM.tmpResolution:PARAM.tmpResolution:t1+t2])/tp)-1) zeros(1,(PARAM.epspCut*PARAM.tm)/PARAM.tmpResolution) ];
    %     figure; plot(PARAM.tmpResolution*(1:length(current)),current)
    f = exp(-[0:PARAM.tmpResolution:(t1+PARAM.epspCut*PARAM.tm)]/PARAM.tm); % filter it (~LIF)
    PARAM.epspKernel=filter(f,sum(f),current);
    PARAM.refractoryPeriod = t1+t2;
else
    % Double exp (Gerstner 2002)
    PARAM.epspKernel = pspKernel(0:PARAM.tmpResolution:PARAM.epspCut*PARAM.tm,PARAM.ts,PARAM.tm);
    PARAM.refractoryPeriod = 1e-3;
end

[m idx] = max(PARAM.epspKernel);
PARAM.epspKernel = PARAM.epspKernel/m;
%     figure; plot(PARAM.tmpResolution*(1:length(PARAM.epspKernel)),PARAM.epspKernel)
PARAM.epspMaxTime = (idx-1)*PARAM.tmpResolution;

% post synaptic spike kernel
PARAM.usePssKernel = false;
PARAM.pssKernel = [];

% inhibitory postsynaptic potential (positive by convention, scaled so that max is 1)
PARAM.ipspKernel = pspKernel(0:PARAM.tmpResolution:PARAM.epspCut*PARAM.tm,2*PARAM.ts,PARAM.tm);
PARAM.ipspKernel = PARAM.ipspKernel / (max(PARAM.ipspKernel));
PARAM.inhibStrength = 0.5; % inhibition strength (in fraction of threshold)

%***************
%* Spike Train *
%***************
PARAM.nAfferent = 2*7^2; % Number of afferents (number of polarities x width x height)

%**********
%* Neuron *
%**********

PARAM.nNeuron = 32; % number of neurons

% The threshold corresponds roughly to the number of coincindent spikes we want to detect
% Then initial weights should be tuned so as to reach threshold.
PARAM.threshold = 20;

% not used
PARAM.nuThr = Inf;
