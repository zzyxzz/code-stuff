function iz_delaynet
% function iz_delaynet
%   Simulates an izhikevich network with delays

N = 6;      % Number of neurons (neuron #1 is actually input current)
D = 10;     % Max delay time ms

% Neuron types (neuron #1 is actually input current so has no type)
ntype = [0   4   1   1   1   1];
% Synapse weights (row = presynaptic, column = postsynaptic)
wghts = [0   1   1   1   0   0;...
         0   0   0   -20 -0  -0;...
         0   0   0   0   12  12;...
         0   0   0   0   12  12;...
         0   0   0   0   0   0;...
         0   0   0   0   0   0];
wghts = [0   1   1   1   0   0;...
         0   0   0   -20 -0  -0;...
         0   0   0   0   12  12;...
         0   0   0   0   12  12;...
         0   0   0   0   0   0;...
         0   0   0   0   0   0];     
% Transmission delays
delays= [1   1   1   1   1   1;...
         1   1   1   1   1   1;...
         1   1   1   1   1   1;...
         1   1   1   1   1   10;...
         1   1   1   1   1   1;...
         1   1   1   1   1   1];
% Synaptic efficacy loss after a spike, and recovery each timestep
SYNLOSS = 0.0; %0.1
SYNRECOV = 0.001;

% Simulation of 1000 ms 
TOTTIM = 1000;

% Loop until user quits
while true
    
i = menu('Select Input','None','Block','Ramp','+ sin()');
if i < 1
    return
end

% Input current for 1000ms
icurrent = zeros(TOTTIM,1);
for t=1:TOTTIM          % simulation of 1000 ms 
    switch i
        case 2
            if t > 250 && t < 750; icurrent(t) = 20; end;
        case 3
            icurrent(t) = max((t-100)/30,0);
        case 4    
            icurrent(t) = max(25*sin(t/20),0);
    end
    %if t > 200 && t < 700; icurrent(t) = .2; end
    %if t > 270 && t < 280; icurrent(t) = .6; end
    %if t > 510 && t < 520; icurrent(t) = 0; end
end

% Current weights (allowing for loss/recovery)
curwghts = wghts;

% Inputs to all neurons with all delays
inputs = zeros(D,N);

% Parameters a,b,c,d for each neuron type
pars=[0.02      0.2     -65     8        ;...     % 1 RS regular spiking
      0.02      0.2     -55     4        ;...     % 2 IB intrinsically bursting
      0.02      0.2     -50     2        ;...     % 3 CH chattering
      0.1       0.2     -65     2        ;...     % 4 FS fast spiking
      0.02      0.25    -65     2        ;...     % 5 LTS low threshold spiking
      0.02      0.25    -65     0.05     ;...     % 6 TC thalamo-cortical
      0.1       0.26    -65     2        ;...     % 7 RZ Resonator
      0.02      0.2     -65      6       ;...     % 8 tonic spiking
      0.02      0.25    -65      6       ;...     % 9 phasic spiking
      0.02      0.2     -50      2       ;...     % 10 tonic bursting
      0.02      0.25    -55     0.05     ;...     % 11 phasic bursting
      0.02      0.2     -55     4        ;...     % 12 mixed mode
      0.01      0.2     -65     8        ;...     % 13 spike frequency adaptation
      0.02      -0.1    -55     6        ;...     % 14 Class 1
      0.2       0.26    -65     0        ;...     % 15 Class 2
      0.02      0.2     -65     6        ;...     % 16 spike latency
      0.05      0.26    -60     0        ;...     % 17 subthreshold oscillations
      0.1       0.26    -60     -1       ;...     % 18 resonator
      0.02      -0.1    -55     6        ;...     % 19 integrator
      0.03      0.25    -60     4        ;...     % 20 rebound spike
      0.03      0.25    -52     0        ;...     % 21 rebound burst
      0.03      0.25    -60     4        ;...     % 22 threshold variability
      1         1.5     -60     0        ;...     % 23 bistability
      1         0.2     -60     -21      ;...     % 24 DAP
      0.02      1       -55     4        ;...     % 25 accomodation
     -0.02      -1      -60     8        ;...     % 26 inhibition-induced spiking
     -0.026     -1      -45     0        ;...     % 27 inhibition-induced bursting
      0.01      0.3     -65     20       ];       % 28 pattern generator
  
% Start sim
neurons = 2:N;              % all neurons (not including input)
v(neurons) = -65*ones(N-1,1);                       % Initial values of v
u(neurons) = pars(ntype(neurons),2)'.*v(neurons);   % Initial values of u
firings = [];               % Spike timings
vgraph = zeros(TOTTIM,N);   % Plots of all membrane potentials

for t = 1:TOTTIM         % simulation of 1000 ms 
    v(1) = icurrent(t);  % input current
    % Below line doesn't work because separate colons loop separately, not same
    % number together, so need a for loop
    %inputs(delays(1,:),:) = inputs(delays(1,:),:) + curwghts(1,:)*v(1);
    for d = 1:D
        post = find(delays(1,:)==d);
        inputs(d,post) = inputs(d,post) + curwghts(1,post)*v(1);
    end
    fired = find(v(neurons)>=30)+1; % indices of spikes
    if ~isempty(fired)
        firings = [firings; t+0*fired', fired'];     
        v(fired) = pars(ntype(fired),3)';
        u(fired) = u(fired) + pars(ntype(fired),4)';
        % For each fired neuron
        for f = 1:length(fired)
            % For each possible delay
            for d = 1:D
                % Find the postsynaptic neuron/s
                post = find(delays(fired(f),:)==d);
                % Add the spike to the neuron/s input
                inputs(d,post) = inputs(d,post) + sum(curwghts(fired(f),post),1);
                % Synaptic efficacy is reduced
                curwghts(fired(f),post) = curwghts(fired(f),post)*(1-SYNLOSS);
            end
        end
     end;
     v(neurons) = v(neurons)+0.5*(0.04*v(neurons).^2+5*v(neurons)+140-u(neurons)+inputs(1,neurons));
     v(neurons) = v(neurons)+0.5*(0.04*v(neurons).^2+5*v(neurons)+140-u(neurons)+inputs(1,neurons));
     v(v>=30) = 30;
     u(neurons) = u(neurons)+pars(ntype(neurons),1)'.*(pars(ntype(neurons),2)'.*v(neurons)-u(neurons));

     v(1) = icurrent(t);  % input current
     vgraph(t,:)=v';  % Remember all membrane potentials for graphing later
     
     % Synaptic efficacy slowly recovers
     curwghts = curwghts + (wghts - curwghts)*SYNRECOV;
     
     % Update inputs for next time step
     for d = 1:D-1
         inputs(d,:) = inputs(d+1,:);
     end
     inputs(D,:) = 0;
end;

% Plot all membrane potentials
for p = 1:N
    subplot(N,1,p);
    if p == 1
        % Input trace is green
        plot(vgraph(:,p),'Color','Green');
    else
        plot(vgraph(:,p));
        hold on;
        %plot(vgraph(:,p),'.');        
        hold off;
        ylabel(num2str(length(find(vgraph(:,p)>=30))));
    end
end

end
